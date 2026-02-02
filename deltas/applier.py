from __future__ import annotations
from typing import List
from dataclasses import dataclass, field
from .types import WorldDelta
from .validator import DeltaValidator, ValidationError
from domains.world import World

class DeltaApplier:
    
    def __init__(self, validator: DeltaValidator):
        self.validator = validator
    
    def apply(
        self, delta: WorldDelta, world: World, validate: bool = True
    ) -> ApplyResult:
        errors = []
        
        if validate:
            errors = self.validator.validate(delta, world)
            if any(e.severity == "error" for e in errors):
                return ApplyResult(success=False, errors=errors)
        
        try:
            self._apply_faction_deltas(delta, world)
            self._apply_region_deltas(delta, world)
            self._apply_creations(delta, world)
            self._apply_deletions(delta, world)
            
            return ApplyResult(success=True, errors=errors)
        
        except Exception as e:
            errors.append(ValidationError(
                severity="error",
                message=f"Erreur lors de l'application: {str(e)}",
                entity_id="",
                field="",
                value=None
            ))
            return ApplyResult(success=False, errors=errors)
    
    def _apply_faction_deltas(self, delta: WorldDelta, world: World):
        for faction_id, faction_delta in delta.faction_deltas.items():
            faction = world.get_faction(faction_id)
            if not faction:
                continue
            
            faction.apply_delta(faction_delta)
            
            for region_id in faction_delta.add_regions:
                region = world.get_region(region_id)
                if region:
                    region.owner = faction_id
            
            for region_id in faction_delta.remove_regions:
                region = world.get_region(region_id)
                if region and region.owner == faction_id:
                    region.owner = None
            

    def _apply_region_deltas(self, delta: WorldDelta, world: World):
        for region_id, region_delta in delta.region_deltas.items():
            region = world.get_region(region_id)
            if region:
                region.apply_delta(region_delta)

    def _apply_creations(self, delta: WorldDelta, world: World):
        from domains.faction import Faction
        from domains.region import Region
        
        for fid, data in delta.create_factions.items():
            if fid not in world.factions:
                faction = Faction(
                    id=data.id,
                    name=data.name,
                    power=data.power,
                    legitimacy=data.legitimacy,
                    resources=data.resources,
                    color=data.color
                )
                faction.regions = set(data.regions)
                faction.alliances = set(data.alliances)
                faction.traits = set(data.traits)
                world.factions[fid] = faction
                
                for rid in data.regions:
                    region = world.get_region(rid)
                    if region:
                        region.owner = fid
        
        for rid, data in delta.create_regions.items():
            if rid not in world.regions:
                region = Region(
                    id=data.id,
                    name=data.name,
                    population=data.population,
                    stability=data.stability,
                    owner=data.owner
                )
                world.regions[rid] = region

    def _apply_deletions(self, delta: WorldDelta, world: World):
        for faction_id in delta.delete_factions:
            if faction_id in world.factions:
                del world.factions[faction_id]
        
        for region_id in delta.delete_regions:
            if region_id in world.regions:
                del world.regions[region_id]


@dataclass
class ApplyResult:
    success: bool
    errors: List[ValidationError] = field(default_factory=list)