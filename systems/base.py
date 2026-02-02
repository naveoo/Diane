from abc import ABC, abstractmethod
from typing import Optional
from domains.world import World
from deltas.types import WorldDelta
from deltas.builder import DeltaBuilder
from core.defaults import Defaults

class BaseSystem(ABC):
    def __init__(self, config: Optional[Defaults] = None):
        self.config = config or Defaults()
        
    @abstractmethod
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        pass