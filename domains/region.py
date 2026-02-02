from dataclasses import dataclass, field
from .region_meta import EnvironmentType, RegionSocioEconomic

@dataclass(slots=True)
class Region:

    id: str
    name: str
    population: int
    owner: str
    environment: EnvironmentType = EnvironmentType.RURAL
    socio_economic: RegionSocioEconomic = field(default_factory=RegionSocioEconomic)

    @property
    def stability(self) -> float:
        """Alias for social cohesion to maintain compatibility with existing systems."""
        return self.socio_economic.cohesion

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if self.socio_economic.cohesion < 0 or self.socio_economic.cohesion > 100:
            raise ValueError(f"Cohesion must be between 0 and 100: {self.socio_economic.cohesion}")
        if self.population < 0:
            raise ValueError(f"Population cannot be negative: {self.population}")
    
    def apply_delta(self, delta: 'RegionDelta') -> None:
        if delta.socio_economic is not None:
            # Merge fields to avoid resetting unmentioned fields
            self.socio_economic.infrastructure = delta.socio_economic.infrastructure
            self.socio_economic.cohesion = delta.socio_economic.cohesion

        if delta.stability is not None:
            # Shortcut to update cohesion (for backward compatibility)
            self.socio_economic.cohesion = delta.stability
            
        if delta.population is not None:
            self.population = delta.population
        if delta.owner is not None:
            self.owner = delta.owner