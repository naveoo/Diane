from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class TradeSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        factions = list(world.factions.values())
        
        for i in range(len(factions)):
            for j in range(i + 1, len(factions)):
                f1 = factions[i]
                f2 = factions[j]
                
                if not f1.is_active or not f2.is_active:
                    continue
                    
                if f1.id in f2.alliances:
                    self._process_trade(f1, f2, builder)
                    
    def _process_trade(self, f1, f2, builder):
        cfg = self.config.alliance
        
        res1 = f1.resources
        res2 = f2.resources
        
        trade_occurred = False
        
        if res1.energy > cfg.trade_threshold and res2.energy < cfg.trade_shortage_threshold:
            amount = cfg.trade_amount
            res1.energy -= amount
            res2.energy += amount
            trade_occurred = True
            
        if res2.food > cfg.trade_threshold and res1.food < cfg.trade_shortage_threshold:
            amount = cfg.trade_amount
            res2.food -= amount
            res1.food += amount
            trade_occurred = True
            
        if trade_occurred:
            res1.credits += cfg.trade_credit_bonus
            res2.credits += cfg.trade_credit_bonus
            
            builder.for_faction(f1.id).set_resources(res1).set_legitimacy(min(100.0, f1.legitimacy + cfg.trade_legitimacy_bonus))
            builder.for_faction(f2.id).set_resources(res2).set_legitimacy(min(100.0, f2.legitimacy + cfg.trade_legitimacy_bonus))
            
            builder.add_event(f"🟡 Trade agreement between {f1.name} and {f2.name} is active.")
