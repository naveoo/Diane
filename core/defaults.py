from dataclasses import dataclass

# =========================
# SIMULATION DEFAULTS
# =========================
@dataclass(frozen=True)
class SimulationConfig:
    max_ticks: int = 1_000_000
    snapshot_interval: int = 100
    base_tick_duration: float = 1.0

# =========================
# FACTION DEFAULTS
# =========================
@dataclass(frozen=True)
class FactionConfig:
    default_name: str = "FactionX"
    max_name_size: int = 99
    
    default_power: float = 50.0
    min_power: float = 0.0
    max_power: float = 100.0
    
    default_legitimacy: float = 50.0
    min_legitimacy: float = 0.0
    max_legitimacy: float = 100.0
    
    default_resources: float = 50.0
    min_resources: float = 0.0
    max_resources: float = 100.0
    
    max_alliances: int = 3

# =========================
# REGION DEFAULTS
# =========================
@dataclass(frozen=True)
class RegionConfig:
    default_name: str = "RegionX"
    max_name_size: int = 99
    
    default_population: int = 1000
    min_population: int = 10
    max_population: int = 10_000
    
    default_stability: float = 100.0
    default_stability_insurrection: float = 50.0
    min_stability: float = 0.0
    max_stability: float = 100.0

# =========================
# POWER SYSTEM
# =========================
@dataclass(frozen=True)
class PowerConfig:
    # Base Growth
    base_army_growth: float = 0.02
    base_navy_growth: float = 0.015
    base_air_growth: float = 0.01
    
    # Decay
    army_decay: float = 0.005
    navy_decay: float = 0.003
    air_decay: float = 0.008
    
    # Region Multipliers
    region_power_factor: float = 0.2
    coastal_navy_bonus: float = 0.5
    
    max_branch_power: float = 100.0

# =========================
# LEGITIMACY SYSTEM
# =========================
@dataclass(frozen=True)
class LegitimacyConfig:
    base_legitimacy_decay: float = 0.01
    stability_legitimacy_factor: float = 0.3
    inequality_penalty: float = 0.4
    
    revolution_threshold: float = 25.0
    revolution_chance: float = 0.15
    expansion_penalty_factor: float = 0.5
    stagnation_penalty: float = 1.0
    
    legitimacy_floor: float = 0.0
    legitimacy_ceiling: float = 100.0
    
    military_victory_bonus: float = 5.0
    starvation_legitimacy_loss: float = 0.5
    alliance_legitimacy_bonus: float = 2.0

# =========================
# ECONOMY SYSTEM
# =========================
@dataclass(frozen=True)
class EconomyConfig:
    base_credits_income: float = 2.0
    base_materials_income: float = 1.0
    base_influence_income: float = 0.5
    
    region_credits_factor: float = 0.5 
    region_materials_factor: float = 0.8
    
    upkeep_power_factor: float = 0.05
    
    corruption_factor: float = 0.02
    resource_starvation_threshold: float = 5.0
    
    # Consumption
    food_per_population: float = 0.01
    energy_per_power: float = 0.1
    urban_energy_drain: float = 0.5
    
    # Regional Multipliers
    rural_food_yield: float = 3.0
    coastal_food_yield: float = 1.0
    industrial_energy_yield: float = 2.0
    industrial_materials_yield: float = 2.5

# =========================
# CONFLICT SYSTEM
# =========================
@dataclass(frozen=True)
class ConflictConfig:
    revolt_stability_threshold: float = 30.0
    revolution_legitimacy_threshold: float = 20.0
    insurrection_chance: float = 0.05
    
    revolt_power_loss: float = 10.0
    revolt_stability_loss: float = 20.0
    
    revolt_chance: float = 0.30
    civil_war_chance: float = 0.01
    coup_d_etat_chance: float = 0.02

# =========================
# ALLIANCES SYSTEM
# =========================
@dataclass(frozen=True)
class AllianceConfig:
    alliance_power_ratio_limit: float = 1.5
    betrayal_cost: float = 15.0
    alliance_formation_chance: float = 0.05
    alliance_break_chance: float = 0.02
    
    # Trade
    trade_threshold: float = 50.0
    trade_shortage_threshold: float = 10.0
    trade_amount: float = 10.0
    trade_credit_bonus: float = 2.0
    trade_legitimacy_bonus: float = 0.5

# =========================
# COLLAPSE SYSTEM
# =========================
@dataclass(frozen=True)
class CollapseConfig:
    faction_power_floor: float = 5.0
    faction_legitimacy_floor: float = 10.0
    collapse_power_transfer_ratio: float = 0.3

# =========================
# WAR SYSTEM
# =========================
@dataclass(frozen=True)
class WarConfig:
    war_declaration_chance: float = 0.15
    victory_power_ratio_threshold: float = 1.1
    conquest_power_cost: float = 10.0
    conquest_stability_penalty: float = 30.0
    colonization_power_cost: float = 5.0
    colonization_chance: float = 0.2

# =========================
# INVESTMENT SYSTEM
# =========================
@dataclass(frozen=True)
class InvestmentConfig:
    investment_chance: float = 0.1
    stability_investment_cost: float = 10.0
    stability_gain: float = 15.0
    population_investment_cost: float = 15.0
    population_gain: int = 200

# =========================
# TRAIT MODIFIERS
# =========================
@dataclass(frozen=True)
class TraitConfig:
    # Militarist
    militarist_power_growth_mod: float = 1.2
    militarist_victory_mod: float = 1.15
    militarist_upkeep_mod: float = 0.9
    
    # Pacifist
    pacifist_power_growth_mod: float = 0.8
    pacifist_legitimacy_mod: float = 1.1
    pacifist_war_declaration_mod: float = 0.5
    
    # Industrialist
    industrialist_income_mod: float = 1.2
    industrialist_materials_mod: float = 1.25
    
    # Technocrat
    technocrat_corruption_mod: float = 0.5
    technocrat_investment_efficiency: float = 1.25
    
    # Populist
    populist_inequality_penalty_mod: float = 0.5
    populist_revolution_threshold_mod: float = 0.7
    
    # Diplomat
    diplomat_alliance_formation_mod: float = 1.5
    diplomat_alliance_legitimacy_mod: float = 1.5
    
    # Imperialist
    imperialist_conquest_cost_mod: float = 0.7
    imperialist_expansion_penalty_mod: float = 0.8
    imperialist_victory_legitimacy_bonus: float = 2.0

    # Autocrat
    autocrat_stability_impact_mod: float = 0.5
    autocrat_coup_chance_mod: float = 2.0

# =========================
# AGGREGATE CONFIGURATION
# =========================
@dataclass(frozen=True)
class Defaults:
    simulation: SimulationConfig = SimulationConfig()
    faction: FactionConfig = FactionConfig()
    region: RegionConfig = RegionConfig()
    power: PowerConfig = PowerConfig()
    legitimacy: LegitimacyConfig = LegitimacyConfig()
    economy: EconomyConfig = EconomyConfig()
    conflict: ConflictConfig = ConflictConfig()
    alliance: AllianceConfig = AllianceConfig()
    collapse: CollapseConfig = CollapseConfig()
    war: WarConfig = WarConfig()
    investment: InvestmentConfig = InvestmentConfig()
    traits: TraitConfig = TraitConfig()