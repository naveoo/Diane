import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class WarSystem(BaseSystem):
    """
    Manages inter-faction wars and conquest.
    """
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.war
        t_cfg = self.config.traits
        active_factions = [f for f in world.factions.values() if f.is_active]
        
        for attacker in active_factions:
            # Chance to declare war or colonize
            declaration_chance = cfg.war_declaration_chance
            if "Pacifist" in attacker.traits:
                declaration_chance *= t_cfg.pacifist_war_declaration_mod
            
            if random.random() < declaration_chance:
                # Find targets: Owned by others (not allies) OR Neutral
                potential_owned = []
                potential_neutral = []
                
                for region in world.regions.values():
                    if region.owner:
                        if region.owner != attacker.id and region.owner not in attacker.alliances:
                            potential_owned.append(region)
                    else:
                        potential_neutral.append(region)
                
                # Prioritize normal war if possible, or colonize if neutral exists
                if potential_owned and random.random() > cfg.colonization_chance:
                    target_region = random.choice(potential_owned)
                    target_owner = world.get_faction(target_region.owner)
                    
                    if not target_owner:
                        continue
                    
                    # War Resolution
                    power_ratio = attacker.power.total / max(target_owner.power.total, 1.0)
                    victory_chance = min(power_ratio / (cfg.victory_power_ratio_threshold * 1.5), 0.9)
                    
                    # Trait modifiers for victory
                    if "Militarist" in attacker.traits:
                        victory_chance *= t_cfg.militarist_victory_mod
                    
                    if random.random() < victory_chance:
                        # Conquest Success
                        builder.for_region(target_region.id).set_owner(attacker.id).set_stability(cfg.conquest_stability_penalty).done()
                        builder.for_faction(target_owner.id).remove_region(target_region.id).done()
                        builder.for_faction(attacker.id).add_region(target_region.id).done()
                        
                        # Cost of war (materials)
                        from domains.economy import Resources
                        cost = cfg.conquest_power_cost / 2
                        if "Imperialist" in attacker.traits:
                            cost *= t_cfg.imperialist_conquest_cost_mod
                        
                        new_attacker_res = attacker.resources - Resources(materials=cost)
                        builder.for_faction(attacker.id).set_resources(new_attacker_res).done()
                        
                        # Victory Legitimacy Bonus
                        leg_bonus = self.config.legitimacy.military_victory_bonus
                        if "Imperialist" in attacker.traits:
                            leg_bonus *= t_cfg.imperialist_victory_legitimacy_bonus
                        
                        new_attacker_leg = min(self.config.faction.max_legitimacy, attacker.legitimacy + leg_bonus)
                        builder.for_faction(attacker.id).set_legitimacy(new_attacker_leg).done()
                        
                        # Partial casualties for winner
                        new_attacker_power = attacker.power * 0.95
                        builder.for_faction(attacker.id).set_power(new_attacker_power).done()
                        
                        builder.add_event(f"WAR: {attacker.name} conquered {target_region.name} from {target_owner.name}!")
                    else:
                        # Failure (Heavy casualties)
                        new_attacker_power = attacker.power * 0.8
                        new_defender_power = target_owner.power * 0.9
                        
                        builder.for_faction(attacker.id).set_power(new_attacker_power).done()
                        builder.for_faction(target_owner.id).set_power(new_defender_power).done()
                        
                        builder.add_event(f"WAR: {attacker.name} failed to conquer {target_region.name} from {target_owner.name}.")
                
                elif potential_neutral:
                    # Colonization (Automatic)
                    from domains.power import Power
                    target_region = random.choice(potential_neutral)
                    builder.for_region(target_region.id).set_owner(attacker.id).set_stability(80.0).done()
                    builder.for_faction(attacker.id).add_region(target_region.id).done()
                    
                    # Cost of colonization
                    cost = cfg.colonization_power_cost/2
                    if "Imperialist" in attacker.traits:
                        cost *= t_cfg.imperialist_conquest_cost_mod # Using same logic for simplicity
                        
                    new_attacker_power = attacker.power - Power(army=cost)
                    builder.for_faction(attacker.id).set_power(new_attacker_power).done()
                    
                    builder.add_event(f"EXPANSION: {attacker.name} colonized the neutral region of {target_region.name}.")
