from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class LegitimacySystem(BaseSystem):
    """
    Manages faction legitimacy.
    - Decay over time
    - Stability impact
    - Inequality penalties (Gini Coefficient)
    """
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.legitimacy
        
        # Calculate Gini Coefficient
        active_factions = [f for f in world.factions.values() if f.power.total > 0]
        gini = 0.0
        if active_factions:
            powers = sorted([f.power.total for f in active_factions])
            n = len(powers)
            total_sum = sum(powers)
            if n > 0 and total_sum > 0:
                mean_power = total_sum / n
                sum_diffs = sum(abs(x - y) for x in powers for y in powers)
                gini = sum_diffs / (2 * n**2 * mean_power)
        
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
                
            current_legitimacy = faction.legitimacy
            
            # 1. Decay
            step1 = current_legitimacy * (1 - cfg.base_legitimacy_decay)
            
            # 2. Stability Bonus
            stability_bonus = 0.0
            t_cfg = self.config.traits
            if faction.regions:
                total_cohesion = 0.0
                count = 0
                for rid in faction.regions:
                    region = world.get_region(rid)
                    if region:
                        total_cohesion += region.socio_economic.cohesion
                        count += 1
                if count > 0:
                    avg_cohesion = total_cohesion / count
                    impact = cfg.stability_legitimacy_factor
                    if "Autocrat" in faction.traits:
                        impact *= t_cfg.autocrat_stability_impact_mod
                    stability_bonus = avg_cohesion * impact
            
            # 3. Gini Penalty
            gini_penalty = gini * cfg.inequality_penalty * 100.0
            if "Populist" in faction.traits:
                gini_penalty *= t_cfg.populist_inequality_penalty_mod
            
            # 4. Starvation Penalty
            starvation_penalty = 0.0
            if faction.resources.credits < self.config.economy.resource_starvation_threshold or \
               faction.resources.materials < self.config.economy.resource_starvation_threshold:
                 starvation_penalty = cfg.starvation_legitimacy_loss
            
            # 5. Alliance Bonus
            alliance_bonus = len(faction.alliances) * cfg.alliance_legitimacy_bonus
            if "Diplomat" in faction.traits:
                alliance_bonus *= t_cfg.diplomat_alliance_legitimacy_mod
 
            # 6. Expansion & Stagnation Penalties
            expansion_penalty = len(faction.regions) * cfg.expansion_penalty_factor
            if "Imperialist" in faction.traits:
                expansion_penalty *= t_cfg.imperialist_expansion_penalty_mod
            
            stagnation = 0.0
            if len(faction.regions) <= 1:
                stagnation = cfg.stagnation_penalty
 
            new_val = step1 + stability_bonus - gini_penalty - starvation_penalty + alliance_bonus - expansion_penalty - stagnation
            
            # Trait Final Multipliers
            if "Pacifist" in faction.traits:
                new_val *= t_cfg.pacifist_legitimacy_mod
            
            # Apply bounds
            f_cfg = self.config.faction
            new_val = max(f_cfg.min_legitimacy, min(f_cfg.max_legitimacy, new_val))
            
            # The guide mentioned a bug: "if f.legitimacy < ceiling: set to ceiling". 
            # We are recalculating new_val completely, so we just clamp final result.
            # If the user meant "active correction" logic in the code, we should ensure we don't accidentally do that.
            # Our logic here `min(max_legitimacy, ...)` is correct.
            
            if new_val != current_legitimacy:
                builder.for_faction(faction_id).set_legitimacy(new_val)
