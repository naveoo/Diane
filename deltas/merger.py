from enum import Enum
from .types import WorldDelta, FactionDelta

class MergeStrategy(Enum):
    LAST_WINS = "last_wins"
    FIRST_WINS = "first_wins"
    MAX = "max"
    MIN = "min"
    AVERAGE = "average"
    SUM = "sum"
    CUSTOM = "custom"


class DeltaMerger:
    
    def __init__(self, strategy: MergeStrategy = MergeStrategy.LAST_WINS):
        self.strategy = strategy
    
    def merge(self, deltas: list[WorldDelta]) -> WorldDelta:
        if not deltas:
            return WorldDelta()
        
        result = WorldDelta()
        
        for delta in deltas:
            self._merge_into(result, delta)
        
        return result
    
    def _merge_into(self, target: WorldDelta, source: WorldDelta):
        for faction_id, faction_delta in source.faction_deltas.items():
            if faction_id not in target.faction_deltas:
                target.faction_deltas[faction_id] = faction_delta
            else:
                self._merge_faction_delta(
                    target.faction_deltas[faction_id],
                    faction_delta
                )
    
    def _merge_faction_delta(self, target: FactionDelta, source: FactionDelta):
        if self.strategy == MergeStrategy.LAST_WINS:
            if source.power is not None:
                target.power = source.power
            if source.legitimacy is not None:
                target.legitimacy = source.legitimacy
        
        elif self.strategy == MergeStrategy.AVERAGE:
            if source.power is not None and target.power is not None:
                target.power = (target.power + source.power) / 2
        
        
        target.add_regions.update(source.add_regions)
        target.remove_regions.update(source.remove_regions)