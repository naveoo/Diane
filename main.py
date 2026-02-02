import logging
import random
import uuid
from engine import SimulationEngine
from domains.world import World
from domains.faction import Faction
from domains.region import Region

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from scenarios import create_demo_scenario

def main():
    setup_logger()
    
    engine = SimulationEngine("diane_simulation.db")
    engine.create_session(f"Demo Run {str(uuid.uuid4())[:8]}")
    
    print("Initializing World...")
    initial_world = create_demo_scenario()
    engine.initialize_world(initial_world)
    
    print("Starting Simulation...")
    try:
        events = engine.step(100)
        for event in events:
            print(event)
        
        print("\nSimulation Finished.")
        final_world = engine.world
        print("\nFinal Status:")
        for f in final_world.factions.values():
            if f.is_active:
                print(f" - {f.name}: Power={f.power.total:.1f}, Legit={f.legitimacy:.1f}, Credits={f.resources.credits:.1f}, Regions={len(f.regions)}")
            else:
                print(f" - {f.name}: COLLAPSED/INACTIVE")
                
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    main()
