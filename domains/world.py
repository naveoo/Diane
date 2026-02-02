from dataclasses import dataclass
from typing import Dict, Optional
from .faction import Faction
from .region import Region

@dataclass(slots=True)
class World:

    factions: Dict[str, Faction]
    regions: Dict[str, Region]

    def get_faction(self, faction_id: str) -> Optional[Faction]:
        return self.factions.get(faction_id)
    
    def get_region(self, region_id: str) -> Optional[Region]:
        return self.regions.get(region_id)