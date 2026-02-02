import json
from domains.world import World
from domains.faction import Faction
from domains.region import Region
from domains.economy import Resources

def create_demo_scenario() -> World:
    from domains.power import Power
    from domains.region_meta import EnvironmentType, RegionSocioEconomic

    f1 = Faction(
        id="f_hegemony", 
        name="Solar Hegemony", 
        power=Power(army=60.0, navy=30.0, air=20.0), 
        legitimacy=45.0, 
        resources=Resources(credits=40.0, materials=150.0),
        color="#E74C3C"
    )
    f1.traits = {"Militarist", "Industrialist"}
    
    f2 = Faction(
        id="f_republic", 
        name="United Republic", 
        power=Power(army=25.0, navy=35.0, air=30.0), 
        legitimacy=85.0, 
        resources=Resources(credits=200.0, materials=40.0),
        color="#3498DB"
    )
    f2.traits = {"Diplomat", "Pacifist"}

    f3 = Faction(
        id="f_syndicate", 
        name="Iron Syndicate", 
        power=Power(army=30.0, navy=15.0, air=45.0), 
        legitimacy=60.0, 
        resources=Resources(credits=80.0, materials=90.0),
        color="#F1C40F"
    )
    f3.traits = {"Technocrat", "Militarist"}
    
    r1 = Region(id="r_capital", name="Hegemon City", population=8000, owner="f_hegemony", 
                environment=EnvironmentType.URBAN, socio_economic=RegionSocioEconomic(infrastructure=85.0, cohesion=90.0))
    r2 = Region(id="r_foundries", name="Iron Foundries", population=1500, owner="f_hegemony", 
                environment=EnvironmentType.INDUSTRIAL, socio_economic=RegionSocioEconomic(infrastructure=60.0, cohesion=40.0))
    
    r3 = Region(id="r_liberty", name="Liberty Port", population=3000, owner="f_republic", 
                environment=EnvironmentType.COASTAL, socio_economic=RegionSocioEconomic(infrastructure=70.0, cohesion=95.0))
    r4 = Region(id="r_breadbasket", name="Verdant Valleys", population=2000, owner="f_republic", 
                environment=EnvironmentType.RURAL, socio_economic=RegionSocioEconomic(infrastructure=40.0, cohesion=100.0))
    
    r5 = Region(id="r_citadel", name="Syndicate Citadel", population=1200, owner="f_syndicate", 
                environment=EnvironmentType.INDUSTRIAL, socio_economic=RegionSocioEconomic(infrastructure=90.0, cohesion=70.0))
    r6 = Region(id="r_outreach", name="Sky Station", population=600, owner="f_syndicate", 
                environment=EnvironmentType.URBAN, socio_economic=RegionSocioEconomic(infrastructure=75.0, cohesion=80.0))
    
    r7 = Region(id="r_deadzone", name="The Badlands", population=150, owner=None, 
                environment=EnvironmentType.WILDERNESS, socio_economic=RegionSocioEconomic(infrastructure=10.0, cohesion=30.0))
    r8 = Region(id="r_coast_pass", name="Indigo Coast", population=900, owner=None, 
                environment=EnvironmentType.COASTAL, socio_economic=RegionSocioEconomic(infrastructure=30.0, cohesion=60.0))

    f1.regions = {"r_capital", "r_foundries"}
    f2.regions = {"r_liberty", "r_breadbasket"}
    f3.regions = {"r_citadel", "r_outreach"}
    
    return World(
        factions={f.id: f for f in [f1, f2, f3]},
        regions={r.id: r for r in [r1, r2, r3, r4, r5, r6, r7, r8]}
    )

def world_from_dict(data: dict) -> World:
    world = World(factions={}, regions={})
    
    factions_data = data.get("factions", [])
    if isinstance(factions_data, dict):
        fitems = factions_data.items()
    else:
        fitems = [(f["id"], f) for f in factions_data]

    for fid, f_data in fitems:
        res_data = f_data.get("resources", 50.0)
        if isinstance(res_data, (int, float)):
            resources = Resources(credits=float(res_data))
        else:
            resources = Resources.from_dict(res_data)

        pow_data = f_data.get("power", 50.0)
        from domains.power import Power
        if isinstance(pow_data, (int, float)):
            power = Power(army=float(pow_data))
        else:
            power = Power.from_dict(pow_data)

        faction = Faction(
            id=fid,
            name=f_data["name"],
            power=power,
            legitimacy=float(f_data.get("legitimacy", 50.0)),
            resources=resources,
            knowledge=float(f_data.get("knowledge", 0.0)),
            color=f_data.get("color", "#808080")
        )
        faction.traits = set(f_data.get("traits", []))
        faction.regions = set(f_data.get("regions", []))
        faction.alliances = set(f_data.get("alliances", []))
        faction.is_active = f_data.get("is_active", True)
        world.factions[fid] = faction
        
    regions_data = data.get("regions", [])
    if isinstance(regions_data, dict):
        ritems = regions_data.items()
    else:
        ritems = [(r["id"], r) for r in regions_data]

    for rid, r_data in ritems:
        from domains.region_meta import EnvironmentType, RegionSocioEconomic
        se_data = r_data.get("socio_economic")
        if not se_data:
            cohesion = float(r_data.get("stability", 100.0))
            socio_economic = RegionSocioEconomic(cohesion=cohesion)
        else:
            socio_economic = RegionSocioEconomic.from_dict(se_data)
            
        environment = EnvironmentType.from_str(r_data.get("environment", "RURAL"))

        region = Region(
            id=rid,
            name=r_data["name"],
            population=int(r_data.get("population", 1000)),
            owner=r_data.get("owner"),
            environment=environment,
            socio_economic=socio_economic
        )
        world.regions[rid] = region
        
        if region.owner and region.owner in world.factions:
            world.factions[region.owner].regions.add(rid)
            
    return world

def world_to_dict(world: World) -> dict:
    data = {"factions": [], "regions": []}
    
    for f in world.factions.values():
        data["factions"].append({
            "id": f.id,
            "name": f.name,
            "power": f.power.to_dict(),
            "legitimacy": f.legitimacy,
            "resources": f.resources.to_dict(),
            "knowledge": f.knowledge,
            "traits": list(f.traits),
            "regions": list(f.regions),
            "alliances": list(f.alliances),
            "is_active": f.is_active,
            "color": getattr(f, "color", "#808080")
        })
        
    for r in world.regions.values():
        data["regions"].append({
            "id": r.id,
            "name": r.name,
            "population": r.population,
            "owner": r.owner,
            "environment": r.environment.value,
            "socio_economic": r.socio_economic.to_dict()
        })
        
    return data

def load_scenario_json(json_str: str) -> World:
    data = json.loads(json_str)
    return world_from_dict(data)
