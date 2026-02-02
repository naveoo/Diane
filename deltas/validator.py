"""
Validation des deltas avant application.
Détecte les incohérences et violations de règles.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Any
from .types import WorldDelta, FactionDelta, RegionDelta
if False: # TYPE_CHECKING
    from domains.world import World
    from domains.faction import Faction
    from domains.region import Region

@dataclass
class ValidationError:
    """Erreur de validation."""
    severity: str  # "error", "warning", "info"
    message: str
    entity_id: str
    field: str
    value: any


class DeltaValidator:
    """Valide les deltas avant application."""
    
    def __init__(self, config):
        self.config = config
    
    def validate(self, delta: WorldDelta, world: World) -> List[ValidationError]:
        """
        Valide un delta contre l'état actuel du monde.
        
        Returns:
            Liste des erreurs trouvées (vide si tout est OK)
        """
        errors = []
        
        # Valider les factions
        for faction_id, faction_delta in delta.faction_deltas.items():
            errors.extend(self._validate_faction_delta(
                faction_id, faction_delta, world
            ))
        
        # Valider les régions
        for region_id, region_delta in delta.region_deltas.items():
            errors.extend(self._validate_region_delta(
                region_id, region_delta, world, delta
            ))
        
        # Valider la cohérence globale
        errors.extend(self._validate_coherence(delta, world))
        
        return errors
    
    def _validate_faction_delta(
        self, faction_id: str, delta: FactionDelta, world: World
    ) -> List[ValidationError]:
        """Valide un delta de faction."""
        errors = []
        faction = world.get_faction(faction_id)
        
        if not faction:
            errors.append(ValidationError(
                severity="error",
                message=f"Faction {faction_id} n'existe pas",
                entity_id=faction_id,
                field="",
                value=None
            ))
            return errors
        
        # Valider les bornes
        if delta.power is not None:
            power_val = delta.power.total
            if power_val < self.config.faction.min_power:
                errors.append(ValidationError(
                    severity="error",
                    message="Puissance sous le minimum",
                    entity_id=faction_id,
                    field="power",
                    value=power_val
                ))
            elif power_val > self.config.faction.max_power:
                errors.append(ValidationError(
                    severity="warning",
                    message="Puissance au-dessus du maximum (sera plafonnée)",
                    entity_id=faction_id,
                    field="power",
                    value=power_val
                ))
        
        # Valider les régions
        for region_id in delta.add_regions:
            if not world.get_region(region_id):
                errors.append(ValidationError(
                    severity="error",
                    message=f"Région {region_id} n'existe pas",
                    entity_id=faction_id,
                    field="add_regions",
                    value=region_id
                ))
        
        return errors
    
    def _validate_region_delta(
        self, region_id: str, delta: RegionDelta, world: World, builder_delta: WorldDelta = None
    ) -> List[ValidationError]:
        """Valide un delta de région."""
        errors = []
        region = world.get_region(region_id)
        
        if not region:
            errors.append(ValidationError(
                severity="error",
                message=f"Région {region_id} n'existe pas",
                entity_id=region_id,
                field="",
                value=None
            ))
            return errors
            
        if delta.stability is not None:
            if not (self.config.region.min_stability <= delta.stability <= self.config.region.max_stability):
                errors.append(ValidationError(
                    severity="warning",
                    message="Stabilité hors bornes",
                    entity_id=region_id,
                    field="stability",
                    value=delta.stability
                ))
        
        if delta.owner:
            # Check world AND the current delta for newly created factions
            exists_in_world = delta.owner in world.factions
            exists_in_delta = builder_delta and delta.owner in builder_delta.create_factions
            
            if not (exists_in_world or exists_in_delta or delta.owner == ""):
                errors.append(ValidationError(
                    severity="error",
                    message=f"Propriétaire {delta.owner} n'existe pas",
                    entity_id=region_id,
                    field="owner",
                    value=delta.owner
                ))
                
        return errors
    
    def _validate_coherence(
        self, delta: WorldDelta, world: World
    ) -> List[ValidationError]:
        """Valide la cohérence globale du delta."""
        errors = []
        
        # Vérifier les conflits de propriété de régions
        region_owners = {}
        for faction_id, faction_delta in delta.faction_deltas.items():
            for region_id in faction_delta.add_regions:
                if region_id in region_owners:
                    errors.append(ValidationError(
                        severity="error",
                        message=f"Conflit: {faction_id} et {region_owners[region_id]} "
                                f"veulent tous deux la région {region_id}",
                        entity_id=faction_id,
                        field="add_regions",
                        value=region_id
                    ))
                else:
                    region_owners[region_id] = faction_id
        
        return errors