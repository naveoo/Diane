from domains.world import World
from domains.region_meta import EnvironmentType, RegionSocioEconomic
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class RegionSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.region
        
        for region_id, region in world.regions.items():
            se = region.socio_economic
            env = region.environment
            
            new_se = RegionSocioEconomic(
                infrastructure=se.infrastructure,
                cohesion=se.cohesion
            )
            
            if se.cohesion > 70:
                infra_growth = 0.1
                if env == EnvironmentType.URBAN: infra_growth *= 1.5
                elif env == EnvironmentType.WILDERNESS: infra_growth *= 0.5
                new_se.infrastructure = min(100.0, se.infrastructure + infra_growth)
            
            if se.cohesion < 100:
                recovery = 0.2 + (se.infrastructure / 200.0)
                new_se.cohesion = min(100.0, se.cohesion + recovery)
            
            new_pop = region.population
            if region.population < cfg.max_population:
                rates = {
                    EnvironmentType.URBAN: 0.005,
                    EnvironmentType.RURAL: 0.003,
                    EnvironmentType.INDUSTRIAL: 0.002,
                    EnvironmentType.COASTAL: 0.004,
                    EnvironmentType.WILDERNESS: 0.001
                }
                base_rate = rates.get(env, 0.002)
                actual_growth = int(region.population * base_rate * (1 + se.infrastructure / 100.0))
                actual_growth = max(actual_growth, 1)
                new_pop = min(cfg.max_population, region.population + actual_growth)

            if new_se != se or new_pop != region.population:
                rb = builder.for_region(region_id)
                if new_se != se:
                    rb.set_socio_economic(new_se)
                if new_pop != region.population:
                    rb.set_population(new_pop)
                rb.done()
