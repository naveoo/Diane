from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class ResearchSystem(BaseSystem):
    """
    Manages technological progress:
    - Factions spend Influence to gain Knowledge.
    - Knowledge provides global bonuses (calculated in other systems).
    - Higher Knowledge levels cost more Influence.
    """
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        t_cfg = self.config.traits
        
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
                
            # Base research rate
            research_rate = 1.0
            if "Technocrat" in faction.traits:
                research_rate *= t_cfg.technocrat_investment_efficiency
                
            if faction.resources.influence > 10.0:
                cost = 2.0
                knowledge_gain = 1.0 * research_rate
                
                new_resources = faction.resources
                new_resources.influence -= cost
                
                new_knowledge = faction.knowledge + knowledge_gain
                
                builder.for_faction(faction_id)\
                    .set_resources(new_resources)\
                    .set_knowledge(new_knowledge)
