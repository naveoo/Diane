import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class ConflictSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        cfg = self.config.conflict
        t_cfg = self.config.traits
        
        for region_id, region in world.regions.items():
            if not region.owner:
                if builder.has_pending_owner_change(region_id):
                    continue
                    
                if random.random() < cfg.insurrection_chance:
                    import uuid
                    from deltas.types import FactionCreationData
                    from core.defaults import Rules
                    
                    new_id = f"nascent_{str(uuid.uuid4())[:8]}"
                    new_name = f"Commonalty of {region.name}"
                    
                    builder.for_region(region_id).set_owner(new_id).set_stability(cfg.revolt_stability_threshold + Rules.Conflict.INSURRECTION_STABILITY_BONUS)
                    
                    from domains.power import Power
                    from domains.economy import Resources
                    
                    trait_pool = Rules.Traits.TRAIT_POOL
                    selected_traits = set(random.sample(trait_pool, random.randint(1, 2)))
                    
                    creation_data = FactionCreationData(
                        id=new_id,
                        name=new_name,
                        power=Power(army=Rules.Conflict.INSURRECTION_ARMY),
                        legitimacy=Rules.Conflict.INSURRECTION_LEGITIMACY,
                        resources=Resources(credits=Rules.Conflict.INSURRECTION_CREDITS),
                        regions={region_id},
                        alliances=set(),
                        traits=selected_traits,
                        color="#00FF00" 
                    )
                    builder.create_faction(creation_data)
                    builder.add_event(f"🔴 INSURRECTION: {new_name} ({new_id}) with traits {selected_traits} established independence in {region.name}!")
                continue
                
            if region.socio_economic.cohesion < cfg.revolt_stability_threshold:
                if random.random() < cfg.revolt_chance:
                    builder.for_region(region_id).set_owner("")
                    builder.add_event(f"🔴 REVOLT: Region {region.name} ({region_id}) declared independence from {region.owner}")
                    
                    new_cohesion = max(0.0, region.socio_economic.cohesion - cfg.revolt_stability_loss)
                    builder.for_region(region_id).set_stability(new_cohesion)
                    
                    fb = builder.for_faction(region.owner)
                    fb.remove_region(region_id)
                    
                    faction = world.get_faction(region.owner)
                    if faction:
                        from domains.power import Power
                        from core.defaults import Rules
                        loss = Power(
                            army=cfg.revolt_power_loss * Rules.Conflict.REVOLT_POWER_LOSS_ARMY_FACTOR, 
                            navy=cfg.revolt_power_loss * Rules.Conflict.REVOLT_POWER_LOSS_NAVY_FACTOR, 
                            air=cfg.revolt_power_loss * Rules.Conflict.REVOLT_POWER_LOSS_AIR_FACTOR
                        )
                        new_power = faction.power - loss
                        fb.set_power(new_power)
        
        for faction_id, faction in world.factions.items():
            if not faction.is_active:
                continue
            
            col_cfg = self.config.collapse
            if (faction.power.total < col_cfg.faction_power_floor) or \
               (faction.legitimacy < col_cfg.faction_legitimacy_floor):
                builder.for_faction(faction_id).delta.deactivate = True
                builder.add_event(f"🔴 COLLAPSE: Faction {faction.name} ({faction_id}) has collapsed!")
                
                for rid in faction.regions:
                    builder.for_region(rid).set_owner("")
                    
                continue
            
            leg_cfg = self.config.legitimacy
            threshold = leg_cfg.revolution_threshold
            if "Populist" in faction.traits:
                threshold *= t_cfg.populist_revolution_threshold_mod
            
            if faction.legitimacy < threshold:
                if random.random() < leg_cfg.revolution_chance:
                    builder.add_event(f"🔴 REVOLUTION: Revolution erupted in {faction.name} ({faction_id})!")
                    
                    from core.defaults import Rules
                    new_power = faction.power * Rules.Conflict.REVOLUTION_POWER_REMAINING
                    builder.for_faction(faction_id).set_power(new_power)
                    
                    for rid in faction.regions:
                        rb = builder.for_region(rid)
                        region = world.get_region(rid)
                        if region:
                            new_stab = max(0.0, region.socio_economic.cohesion - Rules.Conflict.REVOLUTION_STABILITY_PENALTY)
                            rb.set_stability(new_stab)
            
            from core.defaults import Rules
            cw_risk = cfg.civil_war_chance + (1.0 - (faction.legitimacy / 100.0)) * Rules.Conflict.CIVIL_WAR_RISK_LEGITIMACY_FACTOR
            
            if random.random() < cw_risk:
                if len(faction.regions) >= 2:
                    builder.add_event(f"🔴 CIVIL WAR: Civil war broke out in {faction.name} ({faction_id})!")
                    
                    regions_list = list(faction.regions)
                    random.shuffle(regions_list)
                    split_idx = len(regions_list) // 2
                    rebel_regions = regions_list[:split_idx]
                    
                    import uuid
                    from deltas.types import FactionCreationData
                    
                    rebel_id = f"rebels_{str(uuid.uuid4())[:8]}"
                    rebel_name = f"Rebels of {faction.name}"
                    
                    rebel_power = faction.power * Rules.Conflict.CIVIL_WAR_REBEL_POWER_RATIO
                    parent_power = faction.power * Rules.Conflict.CIVIL_WAR_PARENT_POWER_RATIO
                    
                    builder.for_faction(faction_id).set_power(parent_power)
                    for rid in rebel_regions:
                        builder.for_faction(faction_id).remove_region(rid)
                        builder.for_region(rid).set_owner(rebel_id)
                        
                    rebel_res = faction.resources * Rules.Conflict.CIVIL_WAR_REBEL_RESOURCE_RATIO
                    
                    trait_pool = Rules.Traits.TRAIT_POOL
                    selected_traits = set(random.sample(trait_pool, random.randint(1, 2)))

                    creation_data = FactionCreationData(
                        id=rebel_id,
                        name=rebel_name,
                        power=rebel_power,
                        legitimacy=Rules.Conflict.CIVIL_WAR_REBEL_LEGITIMACY,
                        resources=rebel_res,
                        regions=set(rebel_regions),
                        alliances=set(),
                        traits=selected_traits,
                        color="#FF0000"
                    )
                    builder.create_faction(creation_data)
                    builder.add_event(f"NEW FACTION: {rebel_name} ({rebel_id}) with traits {selected_traits} formed from civil war.")
 
            coup_chance = cfg.coup_d_etat_chance
            if "Autocrat" in faction.traits:
                coup_chance *= t_cfg.autocrat_coup_chance_mod
            
            if random.random() < coup_chance:
                builder.add_event(f"🔴 COUP: Military coup in {faction.name} ({faction_id})!")
                
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

