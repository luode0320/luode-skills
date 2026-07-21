"""事件日志和基线的原子持久化。"""

from __future__ import annotations

import json
import os
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

try:
    import yaml
except ImportError:  # pragma: no cover - 可通过 JSON 兼容子集运行
    yaml = None

from .events import BaselineEvent, EventValidationError


class StorageError(RuntimeError):
    """持久化或校验失败。"""


def _load(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream) if yaml is not None else json.load(stream)
    except (OSError, ValueError) as exc:
        raise StorageError(f"unable to read {path}: {exc}") from exc


def _dump(value: Any) -> str:
    if yaml is not None:
        return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, default_flow_style=False)
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


class BaselineStore:
    """以 append-only 事件为事实源，以原子替换投影基线。

    ``project`` 在临时文件完整写入并 fsync 后才调用 ``os.replace``，因此进程或磁盘
    写失败不会留下半份基线；旧文件在任何失败路径保持不变。
    """

    def __init__(self, baseline_path: str | os.PathLike[str], events_path: str | os.PathLike[str] | None = None):
        self.baseline_path = Path(baseline_path)
        self.events_path = Path(events_path) if events_path else self.baseline_path.with_suffix(".events.jsonl")
        self.lock_path = self.events_path.with_suffix(self.events_path.suffix + ".lock")

    @contextmanager
    def _lock(self):
        """以独占 lock 文件串行化事件追加和基线投影，避免多进程交错写入。"""

        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        descriptor: int | None = None
        deadline = time.monotonic() + 10
        while descriptor is None:
            try:
                descriptor = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise StorageError(f"baseline lock timeout: {self.lock_path}")
                time.sleep(0.05)
            except OSError as exc:
                raise StorageError(f"unable to acquire baseline lock: {exc}") from exc
        try:
            yield
        finally:
            try:
                os.close(descriptor)
            finally:
                try:
                    self.lock_path.unlink()
                except OSError:
                    pass

    def read_baseline(self) -> dict[str, Any]:
        value = _load(self.baseline_path)
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise StorageError("baseline root must be an object")
        return value

    def read_events(self) -> list[BaselineEvent]:
        if not self.events_path.exists():
            return []
        result: list[BaselineEvent] = []
        try:
            with self.events_path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    try:
                        result.append(BaselineEvent.from_dict(json.loads(line)))
                    except (ValueError, TypeError, EventValidationError) as exc:
                        raise StorageError(f"invalid event at line {line_number}: {exc}") from exc
        except OSError as exc:
            raise StorageError(f"unable to read {self.events_path}: {exc}") from exc
        return result

    def append_event(self, event: BaselineEvent | Mapping[str, Any]) -> BaselineEvent:
        item = event if isinstance(event, BaselineEvent) else BaselineEvent.from_dict(event)
        encoded = json.dumps(item.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
        with self._lock():
            try:
                with self.events_path.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(encoded)
                    stream.flush()
                    os.fsync(stream.fileno())
            except OSError as exc:
                raise StorageError(f"unable to append event: {exc}") from exc
        return item

    def write_atomic(self, document: Mapping[str, Any]) -> None:
        self.baseline_path.parent.mkdir(parents=True, exist_ok=True)
        encoded = _dump(dict(document))
        temp_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n", dir=self.baseline_path.parent,
                prefix=f".{self.baseline_path.name}.", suffix=".tmp", delete=False,
            ) as stream:
                temp_name = stream.name
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.baseline_path)
            temp_name = None
            try:
                directory_fd = os.open(self.baseline_path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                # Windows 目录句柄不支持 fsync；文件本身已完成原子替换。
                pass
        except OSError as exc:
            raise StorageError(f"unable to atomically write {self.baseline_path}: {exc}") from exc
        finally:
            if temp_name:
                try:
                    os.unlink(temp_name)
                except OSError:
                    pass

    def project(
        self,
        projector: Callable[[dict[str, Any], BaselineEvent], Mapping[str, Any]] | None = None,
        events: Iterable[BaselineEvent] | None = None,
    ) -> dict[str, Any]:
        """把事件投影到新对象并一次性替换基线。"""

        with self._lock():
            document = self.read_baseline()
            selected = list(events) if events is not None else self.read_events()
            if projector is None:
                projected: Mapping[str, Any] = document
                for event in selected:
                    projected = _default_projector(dict(projected), event)
            else:
                projected = document
                for event in selected:
                    projected = projector(dict(projected), event)
            if not isinstance(projected, Mapping):
                raise StorageError("projector must return an object")
            self.write_atomic(projected)
            return dict(projected)


def _default_projector(document: dict[str, Any], event: BaselineEvent) -> dict[str, Any]:
    """默认仅追加历史事件，业务 adapter 可提供更具体的投影函数。"""

    history = document.setdefault("events", [])
    if not isinstance(history, list):
        raise StorageError("baseline events field must be a list")
    if not any(item.get("event_id") == event.event_id for item in history if isinstance(item, dict)):
        history.append(event.to_dict())
    document["schema_version"] = "2.0"
    return document
