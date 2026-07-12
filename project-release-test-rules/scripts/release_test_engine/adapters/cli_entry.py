"""CLI 命令声明发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR, ParameterIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_COMMAND = re.compile(r"(?:add_parser|@(?:click|typer)\.(?:command|callback)|@command)\s*(?:\(\s*['\"](?P<name>[A-Za-z0-9_.-]+)|\(\s*name\s*=\s*['\"](?P<named>[A-Za-z0-9_.-]+))", re.I)


class CliAdapter:
    """发现 argparse/click/typer 命令入口。"""

    protocol = "cli"
    name = "builtin.cli"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: CLI 源码上下文；[返回] 命令 IR；最近修改时间: 2026-07-12 19:20:00 归一化命令名。"""

        for match in _COMMAND.finditer(context.content):
            name = match.group("name") or match.group("named")
            if not name:
                continue
            yield make_interface(context, "cli", name, {"command_ref": "local_config", "command_name": name}, parameters=(ParameterIR(name="args", location="cli", required=False, schema={"type": "array"}),), evidence_items=evidence(context, f"CLI command {name}", line=line_number(context.content, match.start()), kind="cli"), completeness="partial", confidence=0.82)


ADAPTER = CliAdapter()
