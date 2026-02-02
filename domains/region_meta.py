from dataclasses import dataclass
from enum import Enum, auto

class EnvironmentType(Enum):
    URBAN = "URBAN"           # High credits, high pop capacity
    RURAL = "RURAL"           # Stable credits, medium pop
    INDUSTRIAL = "INDUSTRIAL" # High materials, low stability/growth
    COASTAL = "COASTAL"       # Navy bonus, trade boost
    WILDERNESS = "WILDERNESS" # Low production, difficult to conquer

    @classmethod
    def from_str(cls, name: str) -> 'EnvironmentType':
        try:
            return cls(name.upper())
        except ValueError:
            return cls.RURAL

@dataclass(slots=True)
class RegionSocioEconomic:
    infrastructure: float = 20.0 # 0-100 development level
    cohesion: float = 100.0       # Replaces stability (0-100)
    
    def to_dict(self) -> dict:
        return {
            "infrastructure": self.infrastructure,
            "cohesion": self.cohesion
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RegionSocioEconomic':
        if not data:
            return cls()
        return cls(
            infrastructure=data.get("infrastructure", 20.0),
            cohesion=data.get("cohesion", 100.0)
        )
