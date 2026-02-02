import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class AllianceSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.alliance
        f_cfg = self.config.faction
        
        active_factions = [f for f in world.factions.values() if f.is_active]
        if len(active_factions) < 2:
            return
            
        formation_chance = cfg.alliance_formation_chance
        t_cfg = self.config.traits
        f1_candidate = random.choice(active_factions) if active_factions else None
        if f1_candidate and "Diplomat" in f1_candidate.traits:
            formation_chance *= t_cfg.diplomat_alliance_formation_mod
            
        if random.random() < formation_chance:
            f1 = f1_candidate
            f2 = random.choice(active_factions)
            
            if f1.id != f2.id and f2.id not in f1.alliances:
                if len(f1.alliances) < f_cfg.max_alliances and len(f2.alliances) < f_cfg.max_alliances:
                    builder.for_faction(f1.id).add_alliance(f2.id)
                    builder.for_faction(f2.id).add_alliance(f1.id)
                    builder.add_event(f"🟡 ALLIANCE: {f1.name} and {f2.name} formed an alliance.")

        for faction in active_factions:
            if not faction.alliances:
                continue
                
            for other_id in list(faction.alliances):
                if random.random() < cfg.alliance_break_chance:
                    builder.for_faction(faction.id).remove_alliance(other_id)
                    builder.for_faction(other_id).remove_alliance(faction.id)
                    
                    other = world.get_faction(other_id)
                    other_name = other.name if other else other_id
                    builder.add_event(f"🟡 ALLIANCE BROKEN: {faction.name} and {other_name} are no longer allies.")
