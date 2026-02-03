import logging
from typing import List, Optional, Dict, Any

from core.defaults import Defaults
from domains.world import World
from domains.faction import Faction
from deltas.builder import DeltaBuilder
from deltas.applier import DeltaApplier
from deltas.validator import DeltaValidator
from persistence.manager import PersistenceManager

# Systems
from systems.base import BaseSystem
from systems.power import PowerSystem
from systems.economy import EconomySystem
from systems.legitimacy import LegitimacySystem
from systems.conflict import ConflictSystem
from systems.alliance import AllianceSystem
from systems.region import RegionSystem
from systems.war import WarSystem
from systems.investment import InvestmentSystem
from core.metrics import GeopoliticalMetrics
from systems.research import ResearchSystem
from systems.trade import TradeSystem

logger = logging.getLogger("SimulationEngine")

class SimulationEngine:
    def __init__(self, db_path: str = "simulation.db"):
        self.config = Defaults()
        self.persistence = PersistenceManager(db_path)
        
        self.world: Optional[World] = None
        self.session_id: Optional[str] = None
        self.current_tick: int = 0
        
        self.systems: List[BaseSystem] = [
            RegionSystem(self.config),
            PowerSystem(self.config),
            EconomySystem(self.config),
            LegitimacySystem(self.config),
            AllianceSystem(self.config),
            WarSystem(self.config),
            ResearchSystem(self.config),
            TradeSystem(self.config),
            InvestmentSystem(self.config),
            ConflictSystem(self.config),
        ]
        
    def create_session(self, session_name: str):
        self.session_id = self.persistence.create_session(session_name, self.config)
        self.world = World(factions={}, regions={})
        self.current_tick = 0
        logger.info(f"Created session {self.session_id} - '{session_name}'")
        
    def load_session(self, session_id: str, tick: Optional[int] = None):
        metadata = self.persistence.load_session_metadata(session_id)
        if not metadata:
            raise ValueError(f"Session {session_id} not found.")
            
        target_tick = tick if tick is not None else self.persistence.get_latest_tick(session_id)
        
        snapshot_json = self.persistence.get_snapshot(session_id, target_tick)
        
        if snapshot_json:
            self.world = self._reconstruct_world(snapshot_json)
            self.current_tick = target_tick
        else:
            init_snap = self.persistence.get_snapshot(session_id, 0)
            if not init_snap:
                raise ValueError("No snapshot found to start replay.")
            
            self.world = self._reconstruct_world(init_snap)
            self.current_tick = 0
            
            deltas_json = self.persistence.get_deltas(session_id, 1, target_tick)
            applier = DeltaApplier(DeltaValidator(self.config))
            from persistence.serializer import from_json
            from deltas.types import WorldDelta
            
            for d_json in deltas_json:
                self.current_tick += 1
                d_dict = from_json(d_json)
                pass 
                
        self.session_id = session_id
        logger.info(f"Loaded session {session_id} at tick {self.current_tick}")

    def _reconstruct_world(self, json_str: str) -> World:
        from scenarios import load_scenario_json
        return load_scenario_json(json_str)
    def initialize_world(self, world: World):
        self.world = world
        self.persistence.save_step(self.session_id, 0, None, world_snapshot=self.world)
        
    def step(self, ticks: int = 1) -> List[str]:
        if not self.world or not self.session_id:
            raise ValueError("Session not initialized. Call create_session() and initialize_world() first.")
            
        all_events = []
        for _ in range(ticks):
            self.current_tick += 1
            
            builder = DeltaBuilder()
            
            for system in self.systems:
                system.compute_delta(self.world, builder)
                
            delta = builder.build()
            
            validator = DeltaValidator(self.config)
            applier = DeltaApplier(validator)
            result = applier.apply(delta, self.world, validate=True)
            
            if not result.success:
                for error in result.errors:
                    logger.error(f"[Tick {self.current_tick}] Validation Error: {error.message} (Entity: {error.entity_id})")
            
            snapshot = None
            if self.current_tick % self.config.simulation.snapshot_interval == 0:
                snapshot = self.world
                
            self.persistence.save_step(self.session_id, self.current_tick, delta, world_snapshot=snapshot)
            
            if delta.events:
                for event in delta.events:
                    formatted_event = f"[Tick {self.current_tick}] {event}"
                    logger.info(formatted_event)
                    all_events.append(formatted_event)
        
        return all_events

    def get_metrics(self) -> Dict[str, Any]:
        if not self.world:
            return {}
        return GeopoliticalMetrics.calculate_all(self.world)
