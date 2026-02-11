from dataclasses import dataclass
from enum import Enum

class EnvironmentType(Enum):
    URBAN = "URBAN"
    RURAL = "RURAL"
    INDUSTRIAL = "INDUSTRIAL"
    COASTAL = "COASTAL"
    WILDERNESS = "WILDERNESS"

    @classmethod
    def from_str(cls, name: str) -> 'EnvironmentType':
        try:
            return cls(name.upper())
        except ValueError:
            return cls.RURAL

class WeatherType(Enum):
    SUNNY = "SUNNY"
    CLOUDY = "CLOUDY"
    RAIN = "RAIN"
    STORM = "STORM"
    DROUGHT = "DROUGHT"
    SNOW = "SNOW"
    HEATWAVE = "HEATWAVE"

@dataclass(slots=True)
class WeatherState:
    type: WeatherType = WeatherType.SUNNY
    intensity: float = 1.0
    duration: int = 0

@dataclass(slots=True)
class RegionSocioEconomic:
    infrastructure: float = 20.0
    cohesion: float = 100.0
    happiness: float = 50.0
    
    def to_dict(self) -> dict:
        return {
            "infrastructure": self.infrastructure,
            "cohesion": self.cohesion,
            "happiness": self.happiness
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RegionSocioEconomic':
        if not data:
            return cls()
        return cls(
            infrastructure=data.get("infrastructure", 20.0),
            cohesion=data.get("cohesion", 100.0),
            happiness=data.get("happiness", 50.0)
        )
