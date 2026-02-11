from typing import Optional
from domains.economy import Resources
from domains.power import Power
from domains.region_meta import EnvironmentType, RegionSocioEconomic
from .types import WorldDelta, FactionDelta, RegionDelta, FactionCreationData, RegionCreationData


class DeltaBuilder:
    
    def __init__(self):
        self._world_delta = WorldDelta()
    
    def for_faction(self, faction_id: str) -> 'FactionDeltaBuilder':
        if faction_id not in self._world_delta.faction_deltas:
            self._world_delta.faction_deltas[faction_id] = FactionDelta()
        return FactionDeltaBuilder(self, faction_id, self._world_delta.faction_deltas[faction_id])
    
    def for_region(self, region_id: str) -> 'RegionDeltaBuilder':
        if region_id not in self._world_delta.region_deltas:
            self._world_delta.region_deltas[region_id] = RegionDelta()
        return RegionDeltaBuilder(self, region_id, self._world_delta.region_deltas[region_id])
    
    def add_event(self, message: str) -> 'DeltaBuilder':
        self._world_delta.events.append(message)
        return self
    
    def has_pending_owner_change(self, region_id: str) -> bool:
        if region_id in self._world_delta.region_deltas:
            if self._world_delta.region_deltas[region_id].owner is not None:
                return True
        for f_data in self._world_delta.create_factions.values():
            if region_id in f_data.regions:
                return True
        for f_delta in self._world_delta.faction_deltas.values():
            if region_id in f_delta.add_regions:
                return True
        return False
    
    def create_faction(self, data: FactionCreationData) -> 'DeltaBuilder':
        self._world_delta.create_factions[data.id] = data
        return self

    def create_region(self, id: str, name: str, population: int, environment: EnvironmentType, socio_economic: RegionSocioEconomic, owner: Optional[str] = None) -> 'DeltaBuilder':
        self._world_delta.create_regions[id] = RegionCreationData(
            id=id, name=name, population=population, environment=environment, socio_economic=socio_economic, owner=owner
        )
        return self
        
    def build(self) -> WorldDelta:
        return self._world_delta


class FactionDeltaBuilder:
    def __init__(self, parent: DeltaBuilder, faction_id: str, delta: FactionDelta):
        self.parent = parent
        self.faction_id = faction_id
        self.delta = delta
    
    def set_power(self, power: Power) -> 'FactionDeltaBuilder':
        self.delta.power = power
        return self
    
    def set_legitimacy(self, value: float) -> 'FactionDeltaBuilder':
        self.delta.legitimacy = value
        return self
    
    def set_resources(self, resources: Resources) -> 'FactionDeltaBuilder':
        self.delta.resources = resources
        return self

    def set_detailed_resources(self, resources: 'Ressources') -> 'FactionDeltaBuilder':
        self.delta.detailed_resources = resources
        return self

    def set_knowledge(self, value: float) -> 'FactionDeltaBuilder':
        self.delta.knowledge = value
        return self
    
    def add_region(self, region_id: str) -> 'FactionDeltaBuilder':
        self.delta.add_regions.add(region_id)
        return self
    
    def remove_region(self, region_id: str) -> 'FactionDeltaBuilder':
        self.delta.remove_regions.add(region_id)
        return self
    
    def add_alliance(self, faction_id: str) -> 'FactionDeltaBuilder':
        self.delta.add_alliances.add(faction_id)
        return self
    
    def remove_alliance(self, faction_id: str) -> 'FactionDeltaBuilder':
        self.delta.remove_alliances.add(faction_id)
        return self
    
    def done(self) -> DeltaBuilder:
        return self.parent

class RegionDeltaBuilder:
    def __init__(self, parent: DeltaBuilder, region_id: str, delta: RegionDelta):
        self.parent = parent
        self.region_id = region_id
        self.delta = delta
    
    def set_stability(self, value: float) -> 'RegionDeltaBuilder':
        self.delta.stability = value
        return self

    def set_socio_economic(self, value: 'RegionSocioEconomic') -> 'RegionDeltaBuilder':
        self.delta.socio_economic = value
        return self

    def set_infrastructure(self, value: float) -> 'RegionDeltaBuilder':
        if not self.delta.socio_economic:
            self.delta.socio_economic = RegionSocioEconomic()
        self.delta.socio_economic.infrastructure = value
        return self
    
    def set_population(self, value: int) -> 'RegionDeltaBuilder':
        self.delta.population = value
        return self
    
    def set_owner(self, owner_id: str) -> 'RegionDeltaBuilder':
        self.delta.owner = owner_id
        return self
    
    def done(self) -> DeltaBuilder:
        return self.parent
