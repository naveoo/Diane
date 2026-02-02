from typing import Set
from dataclasses import dataclass, field
from .economy import Resources
from .power import Power

@dataclass(slots=True)
class Faction:
    
    id: str
    name: str
    power: Power = field(default_factory=Power)
    legitimacy: float = 50.0
    resources: Resources = field(default_factory=Resources)
    knowledge: float = 0.0
    regions: Set[str] = field(default_factory=set)
    alliances: Set[str] = field(default_factory=set)
    traits: Set[str] = field(default_factory=set)
    color: str = "#808080"
    is_active: bool = True
    
    def __post_init__(self) -> None:
        self._validate()
    
    def _validate(self) -> None:
        if self.power.total < 0:
            raise ValueError(f"Power cannot be negative: {self.power.total}")
        if self.legitimacy < 0:
            raise ValueError(f"Legitimacy cannot be negative: {self.legitimacy}")
        # Allow negative debt for credits/materials (limited)
        if self.resources.credits < -10000:
             raise ValueError(f"Bankrupt! Credits too low: {self.resources.credits}")
        
        if self.id in self.alliances:
            raise ValueError(f"Faction {self.id} cannot be allied with itself")
    
    def apply_delta(self, delta: 'FactionDelta') -> None:
        if delta.power is not None:
            self.power = delta.power
        if delta.legitimacy is not None:
            self.legitimacy = delta.legitimacy
        if delta.resources is not None:
            self.resources = delta.resources
        if delta.knowledge is not None:
            self.knowledge = delta.knowledge
            
        if delta.add_regions:
            self.regions.update(delta.add_regions)
        if delta.remove_regions:
            self.regions.difference_update(delta.remove_regions)
            
        if delta.add_alliances:
            self.alliances.update(delta.add_alliances)
        if delta.remove_alliances:
            self.alliances.difference_update(delta.remove_alliances)
            
        if delta.deactivate:
            self.is_active = False