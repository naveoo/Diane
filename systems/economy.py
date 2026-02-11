from domains.world import World
from domains.economy import Resources
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class EconomySystem(BaseSystem):
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.economy
        t_cfg = self.config.traits
        l_cfg = self.config.legitimacy
        from core.defaults import Rules
        from domains.ressources import Ressources, Energetic, Human, Material, Production, Intangible, Vital
        from domains.region_meta import EnvironmentType

        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
            
            prod_energetic = Energetic()
            prod_material = Material()
            prod_vital = Vital()
            prod_production = Production()
            prod_intangible = Intangible()
            
            total_pop = 0
            
            for rid in faction.regions:
                region = world.get_region(rid)
                if not region: continue
                
                total_pop += region.population
                pop_ratio = region.population / Rules.Economy.POPULATION_DIVISOR
                dev_mult = 1.0 + (region.socio_economic.infrastructure / Rules.Economy.INFRASTRUCTURE_DIVISOR)
                
                weather_mult_food = 1.0
                weather_mult_energy = 1.0
                weather_mult_water = 1.0
                
                from domains.region_meta import WeatherType
                if region.weather.type == WeatherType.DROUGHT:
                    weather_mult_food *= Rules.Weather.DROUGHT_FOOD_MULT
                    weather_mult_water *= Rules.Weather.DROUGHT_WATER_MULT
                elif region.weather.type == WeatherType.RAIN:
                    weather_mult_food *= Rules.Weather.RAIN_FOOD_MULT
                    weather_mult_water *= Rules.Weather.RAIN_WATER_MULT
                elif region.weather.type == WeatherType.STORM:
                    weather_mult_food *= Rules.Weather.STORM_FOOD_MULT
                    weather_mult_energy *= Rules.Weather.STORM_ENERGY_MULT
                elif region.weather.type == WeatherType.SNOW:
                    weather_mult_food *= Rules.Weather.SNOW_FOOD_MULT
                elif region.weather.type == WeatherType.HEATWAVE:
                    weather_mult_water *= Rules.Weather.HEATWAVE_WATER_MULT
                elif region.weather.type == WeatherType.CLOUDY:
                    weather_mult_energy *= Rules.Weather.CLOUDY_SOLAR_MULT
                
                weather_mult_food = 1.0 + (weather_mult_food - 1.0) * region.weather.intensity
                weather_mult_energy = 1.0 + (weather_mult_energy - 1.0) * region.weather.intensity
                weather_mult_water = 1.0 + (weather_mult_water - 1.0) * region.weather.intensity
                
                if region.environment == EnvironmentType.INDUSTRIAL:
                    prod_energetic = prod_energetic + Energetic(fossils=Rules.Economy.Detailed.FOSSIL_YIELD_INDUSTRIAL * dev_mult * weather_mult_energy)
                    prod_material = prod_material + Material(metals_common=Rules.Economy.Detailed.METALS_YIELD_INDUSTRIAL * dev_mult)
                elif region.environment == EnvironmentType.URBAN:
                    prod_energetic = prod_energetic + Energetic(fossils=Rules.Economy.Detailed.FOSSIL_YIELD_URBAN * dev_mult * weather_mult_energy)
                    prod_material = prod_material + Material(materials_construction=Rules.Economy.Detailed.CONSTRUCTION_YIELD_URBAN * dev_mult)
                    prod_intangible = prod_intangible + Intangible(technology=Rules.Economy.Detailed.TECH_GROWTH_URBAN * dev_mult)
                elif region.environment == EnvironmentType.COASTAL:
                    prod_energetic = prod_energetic + Energetic(
                        renewables=Rules.Economy.Detailed.RENEWABLE_YIELD_COASTAL * dev_mult * weather_mult_energy,
                        biomass=Rules.Economy.Detailed.BIOMASS_YIELD_COASTAL * pop_ratio
                    )
                    prod_vital = prod_vital + Vital(
                        food=Rules.Economy.Detailed.FOOD_YIELD_COASTAL * pop_ratio * weather_mult_food, 
                        water=Rules.Economy.Detailed.WATER_YIELD_COASTAL * weather_mult_water
                    )
                elif region.environment == EnvironmentType.RURAL:
                    prod_energetic = prod_energetic + Energetic(
                        renewables=Rules.Economy.Detailed.RENEWABLE_YIELD_RURAL * weather_mult_energy,
                        biomass=Rules.Economy.Detailed.BIOMASS_YIELD_RURAL * pop_ratio
                    )
                    prod_vital = prod_vital + Vital(
                        food=Rules.Economy.Detailed.FOOD_YIELD_RURAL * pop_ratio * weather_mult_food, 
                        water=Rules.Economy.Detailed.WATER_YIELD_RURAL * weather_mult_water
                    )
            
            active_pop = int(total_pop * Rules.Economy.Detailed.POP_ACTIVE_RATIO)
            qualified_pop = int(total_pop * Rules.Economy.Detailed.POP_QUALIFIED_RATIO)
            
            human_res = Human(
                population=total_pop,
                population_active=active_pop,
                population_qualified=qualified_pop
            )
            
            prev_res = faction.detailed_resources or Ressources()
            
            food_consumption = total_pop * cfg.food_per_population
            energy_consumption = (faction.power.total * cfg.energy_per_power) + (total_pop * 0.001)
            
            new_energetic = prev_res.energetic + prod_energetic
            new_material = prev_res.material + prod_material
            new_vital = prev_res.vital + prod_vital
            new_intangible = prev_res.intangible + prod_intangible
            
            final_food = max(0, new_vital.food - food_consumption)
            final_energy_fossils = max(0, new_energetic.fossils - (energy_consumption * 0.5))
            final_energy_renewables = max(0, new_energetic.renewables - (energy_consumption * 0.5))
            
            
            base_capital_income = cfg.base_credits_income * (1.0 + (prev_res.production.infrastructure / 100.0))
            new_capital = prev_res.production.capital + base_capital_income - ((faction.power.total * cfg.upkeep_power_factor))
            
            final_detailed = Ressources(
                energetic=Energetic(
                    fossils=final_energy_fossils,
                    renewables=final_energy_renewables,
                    nuclear=prev_res.energetic.nuclear,
                    biomass=prev_res.energetic.biomass + prod_energetic.biomass 
                ),
                human=human_res,
                material=new_material,
                production=Production(
                    machinery=prev_res.production.machinery,
                    infrastructure=prev_res.production.infrastructure,
                    logistics=prev_res.production.logistics,
                    capital=new_capital
                ),
                intangible=new_intangible,
                vital=Vital(food=final_food, water=new_vital.water)
            )
            
            simple_resources = final_detailed.to_simple_resources()
            
            builder.for_faction(faction_id).set_detailed_resources(final_detailed)
            builder.for_faction(faction_id).set_resources(simple_resources)
            
            if simple_resources.food <= 0:
                 starvation_ratio = abs(simple_resources.food) / (food_consumption + 1)
                 leg_loss = starvation_ratio * l_cfg.starvation_legitimacy_loss * Rules.Economy.STARVATION_LEGITIMACY_PENALTY_MULT
                 builder.for_faction(faction_id).set_legitimacy(max(0.0, faction.legitimacy - leg_loss))
                 if prev_res.vital.food > 0:
                     builder.add_event(f"🟣 Faction {faction.name} suffers from FOOD SHORTAGE! Legitimacy dropping.")

            if simple_resources.energy <= 0:
                 if prev_res.energetic.fossils > 0 or prev_res.energetic.renewables > 0:
                    builder.add_event(f"🟣 Faction {faction.name} suffers from ENERGY CRISIS!")
            
            f_cfg = self.config.faction
            simple_resources = simple_resources.clamp(
                -2000.0,
                f_cfg.max_resources * Rules.Economy.MAX_RESOURCE_MULT
            )
            builder.for_faction(faction_id).set_resources(simple_resources)
