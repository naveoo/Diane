import json
import dataclasses
from enum import Enum
from typing import Any, Set

class SimulationEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder that handles:
    - Sets (converts to list)
    - Dataclasses (converts to dict)
    - Enums (converts to value)
    """
    def default(self, o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

def to_json(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(obj, cls=SimulationEncoder)

def from_json(json_str: str, cls: Any = None) -> Any:
    """
    Deserialize JSON string.
    Note: Reconstructing exact dataclasses from JSON is complex if nested types aren't explicit.
    For this 'simple' persisted version, we might accept dicts return or use a library like `dacite` or `cattrs`.
    For now, we return dicts/lists structure.
    
    If strict reconstruction is needed, we would need a more robust deserializer.
    Given the requirement "stocker absolument toutes les données", storing raw JSON is fine.
    If we need to LOAD and Resume, we need reconstruction.
    
    We will assume for now that standard dict unpacking is sufficient, 
    but we must handle the Set conversion manually if we want to restore functional objects.
    """
    return json.loads(json_str)
