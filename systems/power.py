from domains.world import World
from domains.power import Power
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class PowerSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.power
        
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
            
            growth = Power(
                army=cfg.base_army_growth,
                navy=cfg.base_navy_growth,
                air=cfg.base_air_growth
            )
            
            t_cfg = self.config.traits
            mod = 1.0
            if "Militarist" in faction.traits:
                mod = t_cfg.militarist_power_growth_mod
            elif "Pacifist" in faction.traits:
                mod = t_cfg.pacifist_power_growth_mod
            
            growth = growth * mod
            
            new_power = Power()
            new_power.army = faction.power.army * (1 + growth.army) * (1 - cfg.army_decay)
            new_power.navy = faction.power.navy * (1 + growth.navy) * (1 - cfg.navy_decay)
            new_power.air = faction.power.air * (1 + growth.air) * (1 - cfg.air_decay)
            
            from core.defaults import Rules
            
            num_regions = len(faction.regions)
            new_power.army += (num_regions * cfg.region_power_factor) * Rules.Power.REGION_ARMY_FACTOR
            new_power.navy += (num_regions * cfg.region_power_factor) * Rules.Power.REGION_NAVY_FACTOR
            new_power.air += (num_regions * cfg.region_power_factor) * Rules.Power.REGION_AIR_FACTOR
            
            from domains.region_meta import EnvironmentType
            for rid in faction.regions:
                r = world.get_region(rid)
                if r and r.environment == EnvironmentType.COASTAL:
                    new_power.navy += cfg.coastal_navy_bonus
            
            new_power = new_power.clamp(0.0, cfg.max_branch_power)
            
            if new_power != faction.power:
                builder.for_faction(faction_id).set_power(new_power)
