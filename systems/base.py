from abc import ABC, abstractmethod
from typing import Optional
from domains.world import World
from deltas.types import WorldDelta
from deltas.builder import DeltaBuilder
from rules.defaults import Defaults

class BaseSystem(ABC):
    """
    Base class for all simulation systems.
    Systems analyze the current world state and produce a delta.
    """
    
    def __init__(self, config: Optional[Defaults] = None):
        self.config = config or Defaults()
        
    @abstractmethod
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        """
        Compute changes for this tick and append to the builder.
        
        Args:
           world: The current state of the world (read-only)
           builder: The builder to accumulate changes
        """
        pass
