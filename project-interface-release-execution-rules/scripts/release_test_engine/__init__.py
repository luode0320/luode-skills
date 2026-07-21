"""可插拔上线测试引擎的契约内核。"""

from .events import BaselineEvent, EventValidationError
from .model import IRValidationError, InterfaceIR, ParameterIR, validate_ir
from .safety import SafetyDecision, SafetyViolation, assert_safe, check_operation
from .storage import BaselineStore, StorageError
from .discovery import DiscoveryResult, discover_project
from .graph import DependencyGraphError, build_dependency_graph, topological_order, validate_dependency_graph
from .judge import aggregate, judge
from .runner import ExecutionResult, execute
from .resolver import resolve_parameters
from .adapters import ADAPTER_MATRIX, adapter_status, supported_protocols

__all__ = [
    "BaselineEvent",
    "BaselineStore",
    "EventValidationError",
    "IRValidationError",
    "InterfaceIR",
    "ParameterIR",
    "SafetyDecision",
    "SafetyViolation",
    "StorageError",
    "assert_safe",
    "check_operation",
    "validate_ir",
    "DiscoveryResult",
    "discover_project",
    "DependencyGraphError",
    "build_dependency_graph",
    "topological_order",
    "validate_dependency_graph",
    "aggregate",
    "judge",
    "ExecutionResult",
    "execute",
    "resolve_parameters",
    "ADAPTER_MATRIX",
    "adapter_status",
    "supported_protocols",
]
