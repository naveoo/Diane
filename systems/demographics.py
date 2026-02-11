import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class DemographicsSystem(BaseSystem):
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        from core.defaults import Rules
        
        happiness_map = {}
        for region_id, region in world.regions.items():
            happiness = self._calculate_happiness(world, region)
            happiness_map[region_id] = happiness
            
            new_socio = region.socio_economic
            builder.for_region(region_id).delta.socio_economic = type(new_socio)(
                infrastructure=new_socio.infrastructure,
                cohesion=new_socio.cohesion,
                happiness=happiness
            )
        
        migration_deltas = {}
        for region_id, region in world.regions.items():
            if not region.owner:
                continue
                
            faction = world.get_faction(region.owner)
            if not faction:
                continue
            
            for other_id in faction.regions:
                if other_id == region_id:
                    continue
                    
                other_region = world.get_region(other_id)
                if not other_region:
                    continue
                
                happiness_diff = happiness_map.get(other_id, 50) - happiness_map.get(region_id, 50)
                
                if happiness_diff > Rules.Demographics.MIGRATION_THRESHOLD:
                    migrants = int(region.population * Rules.Demographics.MIGRATION_RATE)
                    if migrants > 0:
                        migration_deltas[region_id] = migration_deltas.get(region_id, 0) - migrants
                        migration_deltas[other_id] = migration_deltas.get(other_id, 0) + migrants
                        
                        builder.add_event(f"👥 {migrants} people migrated from {region.name} to {other_region.name} (happiness: {happiness_map[region_id]:.1f} → {happiness_map[other_id]:.1f})")
        
        for region_id, region in world.regions.items():
            current_pop = region.population
            
            happiness = happiness_map.get(region_id, 50)
            growth_rate = Rules.Demographics.GROWTH_BASE_RATE
            
            if happiness > 60:
                growth_rate += Rules.Demographics.GROWTH_HAPPINESS_MULT * ((happiness - 60) / 40.0)
            elif happiness < 40:
                growth_rate -= Rules.Demographics.GROWTH_HAPPINESS_MULT * ((40 - happiness) / 40.0)
            
            if region.owner:
                faction = world.get_faction(region.owner)
                if faction and faction.detailed_resources:
                    food_per_capita = faction.detailed_resources.vital.food / max(1, current_pop)
                    if food_per_capita < Rules.Demographics.GROWTH_FOOD_REQUIREMENT:
                        growth_rate *= 0.5
            
            natural_growth = int(current_pop * growth_rate)
            
            migration_change = migration_deltas.get(region_id, 0)
            
            new_population = max(0, current_pop + natural_growth + migration_change)
            
            if new_population != current_pop:
                builder.for_region(region_id).set_population(new_population)
    
    def _calculate_happiness(self, world: World, region) -> float:
        from core.defaults import Rules
        
        happiness = 0.0
        
        if region.owner:
            faction = world.get_faction(region.owner)
            if faction and faction.detailed_resources:
                food_per_capita = faction.detailed_resources.vital.food / max(1, region.population)
                food_score = min(100, food_per_capita * 50)
                happiness += food_score * Rules.Demographics.HAPPINESS_FOOD_WEIGHT
                
                total_energy = (faction.detailed_resources.energetic.fossils + 
                               faction.detailed_resources.energetic.renewables +
                               faction.detailed_resources.energetic.nuclear)
                energy_per_capita = total_energy / max(1, region.population)
                energy_score = min(100, energy_per_capita * 1000)
                happiness += energy_score * Rules.Demographics.HAPPINESS_ENERGY_WEIGHT
                
                water_per_capita = faction.detailed_resources.vital.water / max(1, region.population)
                water_score = min(100, water_per_capita * 50)
                happiness += water_score * Rules.Demographics.HAPPINESS_WATER_WEIGHT
        
        stability_score = region.socio_economic.cohesion
        happiness += stability_score * Rules.Demographics.HAPPINESS_STABILITY_WEIGHT
        
        infrastructure_score = min(100, region.socio_economic.infrastructure)
        happiness += infrastructure_score * Rules.Demographics.HAPPINESS_INFRASTRUCTURE_WEIGHT
        
        return max(0.0, min(100.0, happiness))
