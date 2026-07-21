"""定时任务声明发现适配器。"""

from __future__ import annotations

import re
from typing import Iterable

from ..model import InterfaceIR
from .base import DiscoveryContext, evidence, line_number, make_interface


_SCHEDULE = re.compile(r"(?:@(?:Scheduled|schedule|cron)\s*\([^)]*(?:cron\s*=\s*)?['\"](?P<cron>[^'\"\r\n,)]+)|(?:add_job|schedule|cron\.schedule)\s*\([^,]+,\s*['\"](?P<expr>[^'\"\r\n,)]+))", re.I)


class SchedulerAdapter:
    """发现 cron/@Scheduled/add_job 任务。"""

    protocol = "scheduler"
    name = "builtin.scheduler"
    version = "2.0"

    def discover(self, context: DiscoveryContext) -> Iterable[InterfaceIR]:
        """[参数] context: 调度声明上下文；[返回] scheduler IR；最近修改时间: 2026-07-12 19:20:00 保留 cron 表达式。"""

        for index, match in enumerate(_SCHEDULE.finditer(context.content), 1):
            expression = match.group("cron") or match.group("expr")
            yield make_interface(context, "scheduler", f"schedule_{index}_{expression}", {"trigger_ref": "local_config", "schedule": expression}, evidence_items=evidence(context, f"schedule {expression}", line=line_number(context.content, match.start()), kind="scheduler"), completeness="partial", confidence=0.8, risk="P1")


ADAPTER = SchedulerAdapter()
