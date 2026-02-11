from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class MarketSystem(BaseSystem):
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        from core.defaults import Rules
        
        supply = {
            "food": 0.0,
            "energy": 0.0,
            "materials": 0.0,
            "metals_common": 0.0,
            "metals_rare": 0.0,
            "water": 0.0
        }
        
        demand = {
            "food": 0.0,
            "energy": 0.0,
            "materials": 0.0,
            "metals_common": 0.0,
            "metals_rare": 0.0,
            "water": 0.0
        }
        
        for faction in world.factions.values():
            if not faction.is_active or not faction.detailed_resources:
                continue
            
            supply["food"] += faction.detailed_resources.vital.food
            supply["water"] += faction.detailed_resources.vital.water
            supply["energy"] += (faction.detailed_resources.energetic.fossils +
                                faction.detailed_resources.energetic.renewables +
                                faction.detailed_resources.energetic.nuclear)
            supply["materials"] += faction.detailed_resources.material.materials_construction
            supply["metals_common"] += faction.detailed_resources.material.metals_common
            supply["metals_rare"] += faction.detailed_resources.material.metals_rare
            
            total_pop = sum(world.get_region(rid).population for rid in faction.regions if world.get_region(rid))
            
            demand["food"] += total_pop * self.config.economy.food_per_population
            demand["energy"] += faction.power.total * self.config.economy.energy_per_power
            demand["water"] += total_pop * 0.01
            demand["materials"] += faction.power.total * 0.1
            demand["metals_common"] += total_pop * 0.001
            demand["metals_rare"] += faction.power.total * 0.01
        
        new_prices = {}
        for resource in supply.keys():
            current_price = world.market.get(resource, 1.0)
            
            supply_val = supply[resource]
            demand_val = max(1.0, demand[resource])
            
            ratio = supply_val / demand_val
            
            if ratio > Rules.Market.SURPLUS_THRESHOLD:
                price_change = -Rules.Market.PRICE_ADJUSTMENT_RATE * (ratio - 1.0)
            elif ratio < Rules.Market.SHORTAGE_THRESHOLD:
                price_change = Rules.Market.PRICE_ADJUSTMENT_RATE * (1.0 - ratio)
            else:
                price_change = 0.0
            
            new_price = current_price * (1.0 + price_change)
            new_price = max(Rules.Market.MIN_PRICE, min(Rules.Market.MAX_PRICE, new_price))
            
            new_prices[resource] = new_price
            
            if abs(new_price - current_price) > 0.1:
                builder.add_event(f"💰 Market: {resource} price changed from {current_price:.2f} to {new_price:.2f} (supply: {supply_val:.1f}, demand: {demand_val:.1f})")
        
        world.market.update(new_prices)
