import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class ConflictSystem(BaseSystem):
    """
    Manages revolts and civil wars.
    """
    
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.conflict
        t_cfg = self.config.traits
        
        # 1. Region revolts & Insurrections
        for region_id, region in world.regions.items():
            if not region.owner:
                # Check if region is already being claimed
                if builder.has_pending_owner_change(region_id):
                    continue
                    
                # Insurrection chance for neutral regions
                if random.random() < cfg.insurrection_chance:
                    import uuid
                    from deltas.types import FactionCreationData
                    
                    new_id = f"nascent_{str(uuid.uuid4())[:8]}"
                    new_name = f"Commonalty of {region.name}"
                    
                    builder.for_region(region_id).set_owner(new_id).set_stability(cfg.revolt_stability_threshold + 20.0)
                    
                    from domains.power import Power
                    from domains.economy import Resources
                    
                    # Random traits for insurrection
                    trait_pool = ["Militarist", "Pacifist", "Industrialist", "Technocrat", "Populist", "Diplomat", "Imperialist", "Autocrat"]
                    selected_traits = set(random.sample(trait_pool, random.randint(1, 2)))
                    
                    creation_data = FactionCreationData(
                        id=new_id,
                        name=new_name,
                        power=Power(army=15.0),
                        legitimacy=60.0,
                        resources=Resources(credits=10.0),
                        regions={region_id},
                        alliances=set(),
                        traits=selected_traits,
                        color="#00FF00" 
                    )
                    builder.create_faction(creation_data)
                    builder.add_event(f"INSURRECTION: {new_name} ({new_id}) with traits {selected_traits} established independence in {region.name}!")
                continue
                
            # If cohesion is low verify chance of revolt
            if region.socio_economic.cohesion < cfg.revolt_stability_threshold:
                if random.random() < cfg.revolt_chance:
                    # Revolt! 
                    builder.for_region(region_id).set_owner("")
                    builder.add_event(f"REVOLT: Region {region.name} ({region_id}) declared independence from {region.owner}")
                    
                    new_cohesion = max(0.0, region.socio_economic.cohesion - cfg.revolt_stability_loss)
                    builder.for_region(region_id).set_stability(new_cohesion)
                    
                    # Faction loses region and power
                    fb = builder.for_faction(region.owner)
                    fb.remove_region(region_id)
                    
                    faction = world.get_faction(region.owner)
                    if faction:
                        from domains.power import Power
                        loss = Power(army=cfg.revolt_power_loss * 0.6, navy=cfg.revolt_power_loss * 0.3, air=cfg.revolt_power_loss * 0.1)
                        new_power = faction.power - loss
                        fb.set_power(new_power)
        
        # 2. Faction-level conflicts
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
            
            # 1. Collapse Check
            col_cfg = self.config.collapse
            if (faction.power.total < col_cfg.faction_power_floor) or \
               (faction.legitimacy < col_cfg.faction_legitimacy_floor):
                   
                builder.for_faction(faction_id).delta.deactivate = True
                builder.add_event(f"COLLAPSE: Faction {faction.name} ({faction_id}) has collapsed!")
                
                # Liberate all regions
                for rid in faction.regions:
                    builder.for_region(rid).set_owner("")
                    
                continue
            
            # 2. Revolution Check
            leg_cfg = self.config.legitimacy
            threshold = leg_cfg.revolution_threshold
            if "Populist" in faction.traits:
                threshold *= t_cfg.populist_revolution_threshold_mod
            
            if faction.legitimacy < threshold:
                if random.random() < leg_cfg.revolution_chance:
                    builder.add_event(f"REVOLUTION: Revolution erupted in {faction.name} ({faction_id})!")
                    
                    new_power = faction.power * 0.8
                    builder.for_faction(faction_id).set_power(new_power)
                    
                    for rid in faction.regions:
                        rb = builder.for_region(rid)
                        region = world.get_region(rid)
                        if region:
                            new_stab = max(0.0, region.socio_economic.cohesion - 20.0)
                            rb.set_stability(new_stab)
            
            # 3. Dynamic Civil War Check
            cw_risk = cfg.civil_war_chance + (1.0 - (faction.legitimacy / 100.0)) * 0.1
            
            if random.random() < cw_risk:
                if len(faction.regions) >= 2:
                    builder.add_event(f"CIVIL WAR: Civil war broke out in {faction.name} ({faction_id})!")
                    
                    regions_list = list(faction.regions)
                    random.shuffle(regions_list)
                    split_idx = len(regions_list) // 2
                    rebel_regions = regions_list[:split_idx]
                    
                    import uuid
                    from deltas.types import FactionCreationData
                    
                    rebel_id = f"rebels_{str(uuid.uuid4())[:8]}"
                    rebel_name = f"Rebels of {faction.name}"
                    
                    rebel_power = faction.power * 0.4
                    parent_power = faction.power * 0.6
                    
                    builder.for_faction(faction_id).set_power(parent_power)
                    for rid in rebel_regions:
                        builder.for_faction(faction_id).remove_region(rid)
                        builder.for_region(rid).set_owner(rebel_id)
                        
                    rebel_res = faction.resources * 0.5
                    
                    # Random traits for rebels
                    trait_pool = ["Militarist", "Pacifist", "Industrialist", "Technocrat", "Populist", "Diplomat", "Imperialist", "Autocrat"]
                    selected_traits = set(random.sample(trait_pool, random.randint(1, 2)))

                    creation_data = FactionCreationData(
                        id=rebel_id,
                        name=rebel_name,
                        power=rebel_power,
                        legitimacy=50.0,
                        resources=rebel_res,
                        regions=set(rebel_regions),
                        alliances=set(),
                        traits=selected_traits,
                        color="#FF0000"
                    )
                    builder.create_faction(creation_data)
                    builder.add_event(f"NEW FACTION: {rebel_name} ({rebel_id}) with traits {selected_traits} formed from civil war.")
 
            # 4. Coup d'Etat Check
            coup_chance = cfg.coup_d_etat_chance
            if "Autocrat" in faction.traits:
                coup_chance *= t_cfg.autocrat_coup_chance_mod
            
            if random.random() < coup_chance:
                builder.add_event(f"COUP: Military coup in {faction.name} ({faction_id})!")
                
                # Military size increases during a coup
                from domains.power import Power
                new_power = faction.power + Power(army=10.0, navy=5.0, air=5.0)
                builder.for_faction(faction_id).set_power(new_power)
                
                new_legitimacy = max(0.0, faction.legitimacy - 30.0)
                builder.for_faction(faction_id).set_legitimacy(new_legitimacy)
                
                for rid in faction.regions:
                    region = world.get_region(rid)
                    if region:
                        new_stab = max(0.0, region.socio_economic.cohesion - 15.0)
                        builder.for_region(rid).set_stability(new_stab)

