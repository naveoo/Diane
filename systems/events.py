import random
from domains.world import World
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class EventSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        from core.defaults import Rules
        from domains.power import Power
        
        if random.random() < Rules.Events.EVENT_BASE_CHANCE:
            event_type = random.choice([
                "tech_breakthrough",
                "pandemic",
                "economic_boom",
                "scandal",
                "natural_disaster",
                "cultural_renaissance",
                "trade_disruption"
            ])
            
            if event_type == "tech_breakthrough":
                active_factions = [f for f in world.factions.values() if f.is_active]
                if active_factions:
                    faction = random.choice(active_factions)
                    if faction.detailed_resources:
                        new_res = faction.detailed_resources
                        from domains.ressources import Intangible
                        new_intangible = Intangible(
                            technology=new_res.intangible.technology + 10.0,
                            know_how=new_res.intangible.know_how + 5.0,
                            data=new_res.intangible.data,
                            trust=new_res.intangible.trust
                        )
                        updated_res = type(new_res)(
                            energetic=new_res.energetic,
                            human=new_res.human,
                            material=new_res.material,
                            production=new_res.production,
                            intangible=new_intangible,
                            vital=new_res.vital
                        )
                        builder.for_faction(faction.id).set_detailed_resources(updated_res)
                        builder.add_event(f"🔬 BREAKTHROUGH: {faction.name} achieved a major technological breakthrough!")
            
            elif event_type == "pandemic":
                for faction in world.factions.values():
                    if not faction.is_active:
                        continue
                    for region_id in faction.regions:
                        region = world.get_region(region_id)
                        if region:
                            loss_rate = random.uniform(0.05, 0.15)
                            new_pop = int(region.population * (1.0 - loss_rate))
                            builder.for_region(region_id).set_population(new_pop)
                            
                            new_happiness = max(0, region.socio_economic.happiness - 20.0)
                            new_socio = type(region.socio_economic)(
                                infrastructure=region.socio_economic.infrastructure,
                                cohesion=region.socio_economic.cohesion,
                                happiness=new_happiness
                            )
                            builder.for_region(region_id).delta.socio_economic = new_socio
                
                builder.add_event(f"☣️ PANDEMIC: A deadly disease swept across the world, devastating populations!")
            
            elif event_type == "economic_boom":
                active_factions = [f for f in world.factions.values() if f.is_active]
                if active_factions:
                    faction = random.choice(active_factions)
                    if faction.detailed_resources:
                        new_res = faction.detailed_resources
                        from domains.ressources import Production
                        new_production = Production(
                            machinery=new_res.production.machinery,
                            infrastructure=new_res.production.infrastructure + 10.0,
                            logistics=new_res.production.logistics + 5.0,
                            capital=new_res.production.capital + 500.0
                        )
                        updated_res = type(new_res)(
                            energetic=new_res.energetic,
                            human=new_res.human,
                            material=new_res.material,
                            production=new_production,
                            intangible=new_res.intangible,
                            vital=new_res.vital
                        )
                        builder.for_faction(faction.id).set_detailed_resources(updated_res)
                        builder.add_event(f"📈 BOOM: {faction.name} experienced an economic boom!")
            
            elif event_type == "scandal":
                active_factions = [f for f in world.factions.values() if f.is_active]
                if active_factions:
                    faction = random.choice(active_factions)
                    new_legitimacy = max(0.0, faction.legitimacy - random.uniform(10.0, 30.0))
                    builder.for_faction(faction.id).set_legitimacy(new_legitimacy)
                    builder.add_event(f"📰 SCANDAL: A major political scandal rocked {faction.name}!")
            
            elif event_type == "natural_disaster":
                regions_list = [r for r in world.regions.values() if r.owner]
                if regions_list:
                    region = random.choice(regions_list)
                    new_infrastructure = max(0.0, region.socio_economic.infrastructure - random.uniform(10.0, 30.0))
                    new_socio = type(region.socio_economic)(
                        infrastructure=new_infrastructure,
                        cohesion=region.socio_economic.cohesion - 10.0,
                        happiness=region.socio_economic.happiness - 15.0
                    )
                    builder.for_region(region.id).delta.socio_economic = new_socio
                    builder.add_event(f"🌋 DISASTER: Natural disaster struck {region.name}, devastating infrastructure!")
            
            elif event_type == "cultural_renaissance":
                active_factions = [f for f in world.factions.values() if f.is_active]
                if active_factions:
                    faction = random.choice(active_factions)
                    if faction.detailed_resources:
                        new_res = faction.detailed_resources
                        from domains.ressources import Intangible
                        new_intangible = Intangible(
                            technology=new_res.intangible.technology,
                            know_how=new_res.intangible.know_how + 8.0,
                            data=new_res.intangible.data + 5.0,
                            trust=new_res.intangible.trust + 10.0
                        )
                        updated_res = type(new_res)(
                            energetic=new_res.energetic,
                            human=new_res.human,
                            material=new_res.material,
                            production=new_res.production,
                            intangible=new_intangible,
                            vital=new_res.vital
                        )
                        builder.for_faction(faction.id).set_detailed_resources(updated_res)
                        builder.add_event(f"🎨 RENAISSANCE: {faction.name} experienced a cultural renaissance!")
            
            elif event_type == "trade_disruption":
                for resource in world.market.keys():
                    world.market[resource] *= random.uniform(1.2, 1.8)
                builder.add_event(f"🚢 DISRUPTION: Global trade routes disrupted, prices spiked!")
