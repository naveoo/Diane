from domains.world import World
from domains.economy import Resources
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class EconomySystem(BaseSystem):
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.economy
        t_cfg = self.config.traits
        l_cfg = self.config.legitimacy
        
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
                
            income = Resources()
            inc_mod = 1.0
            if "Industrialist" in faction.traits:
                inc_mod = t_cfg.industrialist_income_mod
            
            income.credits = cfg.base_credits_income * inc_mod
            income.materials = cfg.base_materials_income * inc_mod
            income.food = 1.0
            income.energy = 0.5
            income.influence = cfg.base_influence_income
            
            total_pop = 0
            for rid in faction.regions:
                region = world.get_region(rid)
                if not region: continue
                
                total_pop += region.population
                pop_factor = region.population / 1000.0
                dev_mult = 1.0 + (region.socio_economic.infrastructure / 100.0)
                efficiency = region.socio_economic.cohesion / 100.0
                
                from domains.region_meta import EnvironmentType
                if region.environment == EnvironmentType.URBAN:
                    income.credits += (cfg.region_credits_factor * pop_factor * 2.0) * dev_mult * efficiency
                    income.energy -= cfg.urban_energy_drain
                elif region.environment == EnvironmentType.COASTAL:
                    income.credits += (cfg.region_credits_factor * pop_factor * 1.25) * dev_mult * efficiency
                    income.materials += (cfg.region_materials_factor * 0.5) * dev_mult
                    income.food += (cfg.coastal_food_yield * pop_factor) * dev_mult
                elif region.environment == EnvironmentType.INDUSTRIAL:
                    income.materials += (cfg.industrial_materials_yield) * dev_mult * efficiency
                    income.energy += (cfg.industrial_energy_yield * dev_mult) * efficiency
                    income.credits += (cfg.region_credits_factor * 0.5) * dev_mult
                elif region.environment == EnvironmentType.RURAL:
                    income.food += (cfg.rural_food_yield * pop_factor) * dev_mult * efficiency
                    income.materials += (cfg.region_materials_factor * 0.5) * dev_mult
                else:
                    income.materials += (cfg.region_materials_factor * 0.3)
            
            food_req = total_pop * cfg.food_per_population
            energy_req = (faction.power.total * cfg.energy_per_power)
            
            income.food -= food_req
            income.energy -= energy_req
            
            upkeep_mod = 1.0
            if "Militarist" in faction.traits:
                upkeep_mod = t_cfg.militarist_upkeep_mod
            upkeep_credits = (faction.power.total * cfg.upkeep_power_factor) * upkeep_mod
            income.credits -= upkeep_credits
            
            new_res = (faction.resources + income)
            
            if new_res.food < 0:
                starvation_ratio = abs(new_res.food) / (food_req + 1)
                leg_loss = starvation_ratio * l_cfg.starvation_legitimacy_loss * 5.0
                builder.for_faction(faction_id).set_legitimacy(max(0.0, faction.legitimacy - leg_loss))
                builder.add_event(f"🟣 Faction {faction.name} suffers from FOOD SHORTAGE! Legitimacy dropping.")
                new_res.food = 0
            
            if new_res.energy < 0:
                builder.add_event(f"🟣 Faction {faction.name} suffers from ENERGY CRISIS!")
                new_res.energy = 0
                
            corruption_mod = 1.0
            if "Technocrat" in faction.traits:
                corruption_mod = t_cfg.technocrat_corruption_mod
            tax_rate = cfg.corruption_factor * corruption_mod
            
            new_res.credits *= (1.0 - tax_rate)
            new_res.materials *= (1.0 - tax_rate)
            new_res.food *= 0.98
            new_res.energy *= 0.98
            
            f_cfg = self.config.faction
            new_res = new_res.clamp(f_cfg.min_resources - 100, f_cfg.max_resources * 20)
            
            if new_res != faction.resources:
                builder.for_faction(faction_id).set_resources(new_res)
