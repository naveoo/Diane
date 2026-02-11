from dataclasses import dataclass, field
from typing import Dict, Optional
from .faction import Faction
from .region import Region

@dataclass(slots=True)
class World:

    factions: Dict[str, Faction]
    regions: Dict[str, Region]
    market: Dict[str, float] = field(default_factory=lambda: {
        "food": 1.0,
        "energy": 1.0,
        "materials": 1.0,
        "metals_common": 1.0,
        "metals_rare": 1.0,
        "water": 1.0
    })

    def get_faction(self, faction_id: str) -> Optional[Faction]:
        return self.factions.get(faction_id)
    
    def get_region(self, region_id: str) -> Optional[Region]:
        return self.regions.get(region_id)