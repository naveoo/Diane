import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class InvestmentSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.investment
        active_factions = [f for f in world.factions.values() if f.is_active]
        
        for faction in active_factions:
            if not faction.regions:
                continue
                
            if random.random() < cfg.investment_chance:
                target_region_id = random.choice(list(faction.regions))
                region = world.get_region(target_region_id)
                
                if not region:
                    continue
                
                if random.random() < 0.6:
                    if faction.resources.credits >= cfg.stability_investment_cost:
                        new_stability = min(region.stability + cfg.stability_gain, 100.0)
                        from domains.economy import Resources
                        builder.for_region(region.id).set_stability(new_stability).done()
                        builder.for_faction(faction.id).set_resources(faction.resources - Resources(credits=cfg.stability_investment_cost)).done()
                        builder.add_event(f"🟣 INVESTMENT: {faction.name} invested in {region.name} stability.")
                else:
                    if faction.resources.credits >= cfg.population_investment_cost:
                        new_infra = min(region.socio_economic.infrastructure + 5.0, 100.0)
                        from domains.economy import Resources
                        builder.for_region(region.id).set_infrastructure(new_infra).done()
                        builder.for_faction(faction.id).set_resources(faction.resources - Resources(credits=cfg.population_investment_cost)).done()
                        builder.add_event(f"🟣 INVESTMENT: {faction.name} expanded infrastructure in {region.name} ({new_infra:.0f}%).")
