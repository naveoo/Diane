import math
from typing import Dict, List, Any
from domains.world import World
from domains.faction import Faction

class GeopoliticalMetrics:
    """
    Advanced statistical and geopolitical metrics calculator for Diane.
    Provides world-level and faction-level indicators.
    """

    @staticmethod
    def calculate_all(world: World) -> Dict[str, Any]:
        """Calculates a full report of world and faction metrics."""
        report = {
            "world": GeopoliticalMetrics.calculate_world_metrics(world),
            "factions": {}
        }
        
        for fid, faction in world.factions.items():
            if faction.is_active:
                report["factions"][fid] = GeopoliticalMetrics.calculate_faction_metrics(world, faction)
                
        return report

    @staticmethod
    def calculate_world_metrics(world: World) -> Dict[str, Any]:
        """Global indicators of world state."""
        factions = [f for f in world.factions.values() if f.is_active]
        if not factions:
            return {}

        total_power = sum(f.power.total for f in factions)
        power_shares = [f.power.total / (total_power + 0.1) for f in factions]
        
        # 1. Hegemony Index (HHI - Herfindahl-Hirschman Index)
        # Sum of squares of shares (0.0 to 1.0). 1.0 = Total Hegemony, 0 = Perfect competition.
        hhi = sum(s**2 for s in power_shares)
        
        # 2. Power Gini (Inequality)
        sorted_powers = sorted([f.power.total for f in factions])
        n = len(sorted_powers)
        gini = 0
        if n > 1:
            diff_sum = sum(abs(x - y) for x in sorted_powers for y in sorted_powers)
            gini = diff_sum / (2 * n * sum(sorted_powers))
            
        # 3. Global Tension Index
        # Combination of low legitimacy and high military power
        avg_legitimacy = sum(f.legitimacy for f in factions) / n
        tension = (100 - avg_legitimacy) * (hhi * 10) # High hegemony + low legitimacy = high tension
        
        # 4. Global Development
        regions = list(world.regions.values())
        avg_infra = sum(r.socio_economic.infrastructure for r in regions) / (len(regions) + 0.1)
        avg_knowledge = sum(f.knowledge for f in factions) / n
        
        # 5. Polarization Index
        # Number of major alliances clusters (simplified)
        alliances_count = sum(len(f.alliances) for f in factions) / 2
        
        # 6. Resource Security Index (global)
        total_food = sum(f.resources.food for f in factions)
        total_energy = sum(f.resources.energy for f in factions)
        total_pop = sum(sum(world.get_region(rid).population for rid in f.regions if world.get_region(rid)) for f in factions)
        
        food_security = (total_food / (total_pop * 0.01 + 1)) * 10  # Ratio to requirement
        energy_security = (total_energy / (total_power * 0.1 + 1)) * 10
        
        # 7. Diplomatic Fragmentation
        # How many isolated factions vs connected ones
        isolated_count = sum(1 for f in factions if len(f.alliances) == 0)
        fragmentation = isolated_count / n
        
        return {
            "total_power": round(total_power, 1),
            "hegemony_hhi": round(hhi, 3),
            "power_gini": round(gini, 3),
            "global_tension": round(tension, 2),
            "avg_legitimacy": round(avg_legitimacy, 1),
            "avg_infrastructure": round(avg_infra, 1),
            "global_knowledge": round(avg_knowledge, 1),
            "polarization_score": round(alliances_count / (n + 0.1), 2),
            "food_security_index": round(food_security, 2),
            "energy_security_index": round(energy_security, 2),
            "diplomatic_fragmentation": round(fragmentation, 2)
        }

    @staticmethod
    def calculate_faction_metrics(world: World, faction: Faction) -> Dict[str, Any]:
        """Detailed metrics for a specific faction."""
        res = faction.resources
        p = faction.power
        
        # 1. Composite Power Index (Knowledge-weighted military)
        cpi = p.total * (1 + (faction.knowledge / 100))
        
        # 2. Strategic Depth
        # Ratio of population in secondary regions vs capital (simplified as pop diversity)
        total_pop = 0
        region_pops = []
        for rid in faction.regions:
            r = world.get_region(rid)
            if r:
                total_pop += r.population
                region_pops.append(r.population)
        
        strategic_depth = 0
        if len(region_pops) > 1:
            # Entropy-like measure of population distribution
            strategic_depth = sum(-(p/total_pop) * math.log(p/total_pop) for p in region_pops)

        # 3. Economic Complexity
        # Ability to produce credits/materials per capita
        income_potential = (res.credits + res.materials + res.food + res.energy)
        econ_intensity = income_potential / (total_pop + 1)
        
        # 4. Support Gap
        # Legitimacy vs Average regional cohesion
        avg_cohesion = 0
        for rid in faction.regions:
            r = world.get_region(rid)
            if r: avg_cohesion += r.socio_economic.cohesion
        avg_cohesion /= (len(faction.regions) + 0.1)
        
        support_gap = faction.legitimacy - avg_cohesion

        # 5. Military Balance Ratio
        # Faction's power vs average of all others
        other_factions = [f for f in world.factions.values() if f.is_active and f.id != faction.id]
        avg_other_power = sum(f.power.total for f in other_factions) / (len(other_factions) + 0.1)
        military_balance = p.total / (avg_other_power + 0.1)
        
        # 6. Resource Security
        food_req = total_pop * 0.01
        energy_req = p.total * 0.1
        food_security = (res.food / (food_req + 1)) * 100
        energy_security = (res.energy / (energy_req + 1)) * 100
        
        # 7. Diplomatic Influence Score
        # Based on alliances and relative power
        alliance_strength = sum(world.factions[aid].power.total for aid in faction.alliances if aid in world.factions and world.factions[aid].is_active)
        diplomatic_influence = (len(faction.alliances) * 10) + (alliance_strength / 10)
        
        # 8. Threat Assessment
        # How threatened is this faction by neighbors
        threat_level = 0
        for other in other_factions:
            if faction.id not in other.alliances:  # Not allied
                if other.power.total > p.total:
                    threat_level += (other.power.total - p.total) / 10
        
        # 9. Technological Advantage
        avg_knowledge = sum(f.knowledge for f in world.factions.values() if f.is_active) / len([f for f in world.factions.values() if f.is_active])
        tech_advantage = faction.knowledge - avg_knowledge
        
        return {
            "composite_power_index": round(cpi, 2),
            "strategic_depth_index": round(strategic_depth, 2),
            "economic_intensity": round(econ_intensity, 3),
            "support_gap": round(support_gap, 1),
            "total_population": total_pop,
            "urbanization_rate": GeopoliticalMetrics._calc_urbanization(world, faction),
            "military_balance_ratio": round(military_balance, 2),
            "food_security_pct": round(food_security, 1),
            "energy_security_pct": round(energy_security, 1),
            "diplomatic_influence": round(diplomatic_influence, 1),
            "threat_level": round(threat_level, 1),
            "tech_advantage": round(tech_advantage, 1)
        }

    @staticmethod
    def _calc_urbanization(world: World, faction: Faction) -> float:
        from domains.region_meta import EnvironmentType
        urban_pop = 0
        total_pop = 0
        for rid in faction.regions:
            r = world.get_region(rid)
            if r:
                total_pop += r.population
                if r.environment == EnvironmentType.URBAN:
                    urban_pop += r.population
        return round((urban_pop / (total_pop + 0.1)) * 100, 1)

    @staticmethod
    def get_power_rankings(world: World) -> List[Dict[str, Any]]:
        """Returns factions ranked by composite power."""
        factions = [f for f in world.factions.values() if f.is_active]
        rankings = []
        
        for f in factions:
            cpi = f.power.total * (1 + (f.knowledge / 100))
            rankings.append({
                "id": f.id,
                "name": f.name,
                "composite_power": round(cpi, 2),
                "raw_power": round(f.power.total, 1),
                "knowledge": round(f.knowledge, 1)
            })
        
        return sorted(rankings, key=lambda x: x["composite_power"], reverse=True)
    
    @staticmethod
    def get_economic_rankings(world: World) -> List[Dict[str, Any]]:
        """Returns factions ranked by total economic resources."""
        factions = [f for f in world.factions.values() if f.is_active]
        rankings = []
        
        for f in factions:
            total_wealth = f.resources.credits + f.resources.materials + f.resources.food + f.resources.energy
            rankings.append({
                "id": f.id,
                "name": f.name,
                "total_wealth": round(total_wealth, 1),
                "credits": round(f.resources.credits, 1),
                "materials": round(f.resources.materials, 1)
            })
        
        return sorted(rankings, key=lambda x: x["total_wealth"], reverse=True)
    
    @staticmethod
    def get_stability_rankings(world: World) -> List[Dict[str, Any]]:
        """Returns factions ranked by legitimacy and cohesion."""
        factions = [f for f in world.factions.values() if f.is_active]
        rankings = []
        
        for f in factions:
            avg_cohesion = 0
            for rid in f.regions:
                r = world.get_region(rid)
                if r: avg_cohesion += r.socio_economic.cohesion
            avg_cohesion /= (len(f.regions) + 0.1)
            
            stability_score = (f.legitimacy + avg_cohesion) / 2
            rankings.append({
                "id": f.id,
                "name": f.name,
                "stability_score": round(stability_score, 1),
                "legitimacy": round(f.legitimacy, 1),
                "avg_cohesion": round(avg_cohesion, 1)
            })
        
        return sorted(rankings, key=lambda x: x["stability_score"], reverse=True)
    
    @staticmethod
    def compare_factions(world: World, fid1: str, fid2: str) -> Dict[str, Any]:
        """Detailed comparison between two factions."""
        f1 = world.factions.get(fid1)
        f2 = world.factions.get(fid2)
        
        if not f1 or not f2:
            return {"error": "One or both factions not found"}
        
        metrics1 = GeopoliticalMetrics.calculate_faction_metrics(world, f1)
        metrics2 = GeopoliticalMetrics.calculate_faction_metrics(world, f2)
        
        return {
            "faction_1": {"id": f1.id, "name": f1.name, "metrics": metrics1},
            "faction_2": {"id": f2.id, "name": f2.name, "metrics": metrics2},
            "power_ratio": round(f1.power.total / (f2.power.total + 0.1), 2),
            "wealth_ratio": round(
                (f1.resources.credits + f1.resources.materials) / 
                (f2.resources.credits + f2.resources.materials + 0.1), 2
            ),
            "are_allied": f1.id in f2.alliances
        }
