from dataclasses import dataclass, field
from typing import Optional, Dict, Set, List
from domains.economy import Resources
from domains.power import Power
from domains.region_meta import EnvironmentType, RegionSocioEconomic

@dataclass
class FactionDelta:
    power: Optional[Power] = None
    legitimacy: Optional[float] = None
    resources: Optional[Resources] = None
    knowledge: Optional[float] = None
    
    add_regions: Set[str] = field(default_factory=set)
    remove_regions: Set[str] = field(default_factory=set)
    add_alliances: Set[str] = field(default_factory=set)
    remove_alliances: Set[str] = field(default_factory=set)
    
    deactivate: bool = False


@dataclass
class RegionDelta:
    socio_economic: Optional[RegionSocioEconomic] = None
    stability: Optional[float] = None
    population: Optional[int] = None
    owner: Optional[str] = None
    
    is_conquered: bool = False
    is_liberated: bool = False

@dataclass
class FactionCreationData:
    id: str
    name: str
    power: Power
    legitimacy: float
    resources: Resources
    regions: Set[str]
    alliances: Set[str]
    knowledge: float = 0.0
    traits: Set[str] = field(default_factory=set)
    color: str = "#808080"

@dataclass
class RegionCreationData:
    id: str
    name: str
    population: int
    environment: EnvironmentType
    socio_economic: RegionSocioEconomic
    owner: Optional[str]

@dataclass
class WorldDelta:
    faction_deltas: Dict[str, FactionDelta] = field(default_factory=dict)
    region_deltas: Dict[str, RegionDelta] = field(default_factory=dict)
    
    create_factions: Dict[str, FactionCreationData] = field(default_factory=dict)
    create_regions: Dict[str, RegionCreationData] = field(default_factory=dict)
    delete_factions: Set[str] = field(default_factory=set)
    delete_regions: Set[str] = field(default_factory=set)
    
    events: List[str] = field(default_factory=list)
    delete_regions: Set[str] = field(default_factory=set)
    
    events: List[str] = field(default_factory=list)


@dataclass
class DeltaBatch:
    source_system: str
    deltas: WorldDelta
    timestamp: float
    priority: int = 0