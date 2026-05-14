from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class FlowStartResult:
    flow_name: str
    current_step: str
    data: dict[str, Any]


class Flow(Protocol):
    name: str
    initial_step: str

