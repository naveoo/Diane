import json
import dataclasses
from enum import Enum
from typing import Any, Set

class SimulationEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

def to_json(obj: Any) -> str:
    return json.dumps(obj, cls=SimulationEncoder)

def from_json(json_str: str, cls: Any = None) -> Any:
    return json.loads(json_str)