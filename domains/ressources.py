from dataclasses import dataclass, field
from typing import Optional
from .economy import Resources as SimpleResources

@dataclass(frozen=True)
class ResourceCategory:
    def __add__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        kwargs = {}
        for field_name in self.__annotations__:
            val = getattr(self, field_name) + getattr(other, field_name)
            kwargs[field_name] = max(0, val) # Prevent negatives for safety
        return type(self)(**kwargs)
        
    def __sub__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        kwargs = {}
        for field_name in self.__annotations__:
            val = getattr(self, field_name) - getattr(other, field_name)
            kwargs[field_name] = max(0, val)
        return type(self)(**kwargs)

@dataclass(frozen=True)
class Energetic(ResourceCategory):
    fossils: float = 0.0
    renewables: float = 0.0
    nuclear: float = 0.0
    biomass: float = 0.0

@dataclass(frozen=True)
class Human(ResourceCategory):
    population: int = 0
    population_active: int = 0
    population_qualified: int = 0

@dataclass(frozen=True)
class Material(ResourceCategory):
    metals_common: float = 0.0
    metals_rare: float = 0.0
    materials_construction: float = 0.0
    products_chemicals: float = 0.0

@dataclass(frozen=True)
class Production(ResourceCategory):
    machinery: float = 0.0
    infrastructure: float = 0.0
    logistics: float = 0.0
    capital: float = 0.0

@dataclass(frozen=True)
class Intangible(ResourceCategory):
    technology: float = 0.0
    know_how: float = 0.0
    data: float = 0.0
    trust: float = 0.0

@dataclass(frozen=True)
class Vital(ResourceCategory):
    food: float = 0.0
    water: float = 0.0

@dataclass(frozen=True)
class Ressources:
    energetic: Energetic = field(default_factory=Energetic)
    human: Human = field(default_factory=Human)
    material: Material = field(default_factory=Material)
    production: Production = field(default_factory=Production)
    intangible: Intangible = field(default_factory=Intangible)
    vital: Vital = field(default_factory=Vital)
    
    def __add__(self, other: 'Ressources') -> 'Ressources':
        return Ressources(
            energetic=self.energetic + other.energetic,
            human=self.human + other.human,
            material=self.material + other.material,
            production=self.production + other.production,
            intangible=self.intangible + other.intangible,
            vital=self.vital + other.vital
        )

    def to_simple_resources(self) -> SimpleResources:
        """
        Maps detailed resources to the simple legacy Resources model.
        """
        total_energy = (self.energetic.fossils + 
                        self.energetic.renewables + 
                        self.energetic.nuclear + 
                        self.energetic.biomass)
                        
        total_materials = (self.material.metals_common + 
                           self.material.metals_rare * 5.0 + 
                           self.material.materials_construction + 
                           self.material.products_chemicals)
                           
        total_food = self.vital.food
        
        total_credits = self.production.capital + (self.intangible.trust * 10.0)
        
        total_influence = self.intangible.trust + (self.intangible.know_how * 0.5)
        
        return SimpleResources(
            credits=total_credits,
            materials=total_materials,
            food=total_food,
            energy=total_energy,
            influence=total_influence
        )