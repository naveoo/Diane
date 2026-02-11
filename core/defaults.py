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
    base_credits_income: float = 10.0
    base_materials_income: float = 2.0
    base_influence_income: float = 0.5
    
    region_credits_factor: float = 0.5 
    region_materials_factor: float = 0.8
    
    upkeep_power_factor: float = 0.2
    
    corruption_factor: float = 0.02
    resource_starvation_threshold: float = 5.0
    
    # Consumption
    food_per_population: float = 0.005
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
    revolt_stability_threshold: float = 20.0
    revolution_legitimacy_threshold: float = 15.0
    insurrection_chance: float = 0.05
    
    revolt_power_loss: float = 10.0
    revolt_stability_loss: float = 20.0
    
    revolt_chance: float = 0.30
    civil_war_chance: float = 0.005
    coup_d_etat_chance: float = 0.01

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
    war_declaration_chance: float = 0.05
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

# =========================
# RULES (MERGED FROM rules.py)
# =========================
@dataclass(frozen=True)
class PowerRules:
    REGION_ARMY_FACTOR = 0.6
    REGION_NAVY_FACTOR = 0.3
    REGION_AIR_FACTOR = 0.1

@dataclass(frozen=True)
class EconomyRules:
    POPULATION_DIVISOR = 100.0
    INFRASTRUCTURE_DIVISOR = 50.0
    COHESION_DIVISOR = 100.0
    
    URBAN_CREDITS_MULT = 2.0
    
    COASTAL_CREDITS_MULT = 1.25
    COASTAL_MATERIALS_MULT = 0.5
    
    INDUSTRIAL_MATERIALS_YIELD = 1.0
    INDUSTRIAL_CREDITS_MULT = 0.5
    
    RURAL_MATERIALS_MULT = 0.5
    
    OTHER_MATERIALS_MULT = 0.3
    
    STARVATION_LEGITIMACY_PENALTY_MULT = 5.0
    
    FOOD_DECAY = 0.98
    ENERGY_DECAY = 0.98
    
    MIN_RESOURCE_OFFSET = 100.0
    MAX_RESOURCE_MULT = 20.0
    
    @dataclass(frozen=True)
    class Detailed:
        # Energetic
        FOSSIL_YIELD_INDUSTRIAL = 20.0
        FOSSIL_YIELD_URBAN = 5.0
        RENEWABLE_YIELD_COASTAL = 15.0
        RENEWABLE_YIELD_RURAL = 10.0
        NUCLEAR_YIELD_TECH = 50.0
        
        # Human
        POP_ACTIVE_RATIO = 0.6
        POP_QUALIFIED_RATIO = 0.2
        
        # Material
        METALS_YIELD_INDUSTRIAL = 15.0
        METALS_RARE_YIELD_INDUSTRIAL = 2.0
        BIOMASS_YIELD_RURAL = 20.0
        BIOMASS_YIELD_COASTAL = 10.0
        CONSTRUCTION_YIELD_URBAN = 10.0
        
        # Vital
        FOOD_YIELD_RURAL = 100.0
        FOOD_YIELD_COASTAL = 60.0
        WATER_YIELD_COASTAL = 30.0
        WATER_YIELD_RURAL = 10.0
        
        # Intangible
        TECH_GROWTH_URBAN = 0.1
        TRUST_GROWTH_STABLE = 0.05

@dataclass(frozen=True)
class LegitimacyRules:
    GINI_PENALTY_SCALE = 100.0

@dataclass(frozen=True)
class ConflictRules:
    # Insurrection
    INSURRECTION_STABILITY_BONUS = 20.0
    INSURRECTION_ARMY = 15.0
    INSURRECTION_LEGITIMACY = 60.0
    INSURRECTION_CREDITS = 10.0
    
    # Revolt
    REVOLT_POWER_LOSS_ARMY_FACTOR = 0.6
    REVOLT_POWER_LOSS_NAVY_FACTOR = 0.3
    REVOLT_POWER_LOSS_AIR_FACTOR = 0.1
    
    # Revolution
    REVOLUTION_STABILITY_PENALTY = 20.0
    REVOLUTION_POWER_REMAINING = 0.8
    
    # Civil War
    CIVIL_WAR_RISK_LEGITIMACY_FACTOR = 0.1
    CIVIL_WAR_REBEL_POWER_RATIO = 0.4
    CIVIL_WAR_PARENT_POWER_RATIO = 0.6
    CIVIL_WAR_REBEL_RESOURCE_RATIO = 0.5
    CIVIL_WAR_REBEL_LEGITIMACY = 50.0
    
    # Coup
    COUP_ARMY_GAIN = 10.0
    COUP_NAVY_GAIN = 5.0
    COUP_AIR_GAIN = 5.0
    COUP_LEGITIMACY_LOSS = 30.0
    COUP_STABILITY_LOSS = 15.0

@dataclass(frozen=True)
class WarRules:
    VICTORY_CHANCE_FACTOR = 1.5
    VICTORY_CAP = 0.9
    
    # Conquest
    CONQUEST_COST_DIVISOR = 2.0
    CONQUEST_ATTACKER_POWER_REMAINING = 0.95
    
    # Failed Attack
    FAILED_ATTACK_ATTACKER_POWER_REMAINING = 0.8
    FAILED_ATTACK_DEFENDER_POWER_REMAINING = 0.9
    
    # Colonization
    COLONIZATION_STABILITY = 80.0
    COLONIZATION_COST_DIVISOR = 2.0

@dataclass(frozen=True)
class AllianceRules:
    pass

@dataclass(frozen=True)
class WeatherRules:
    WEATHER_CHANGE_CHANCE = 0.15
    
    DROUGHT_FOOD_MULT = 0.6
    DROUGHT_WATER_MULT = 0.5
    RAIN_FOOD_MULT = 1.2
    RAIN_WATER_MULT = 1.5
    STORM_FOOD_MULT = 0.85
    STORM_ENERGY_MULT = 0.7
    SNOW_FOOD_MULT = 0.5
    SNOW_LOGISTICS_MULT = 0.6
    HEATWAVE_ENERGY_DEMAND_MULT = 1.5
    HEATWAVE_WATER_MULT = 0.7
    CLOUDY_SOLAR_MULT = 0.6

@dataclass(frozen=True)
class DemographicsRules:
    # Happiness calculation weights
    HAPPINESS_FOOD_WEIGHT = 0.3
    HAPPINESS_STABILITY_WEIGHT = 0.25
    HAPPINESS_INFRASTRUCTURE_WEIGHT = 0.2
    HAPPINESS_ENERGY_WEIGHT = 0.15
    HAPPINESS_WATER_WEIGHT = 0.1
    
    MIGRATION_THRESHOLD = 30.0
    MIGRATION_RATE = 0.02
    
    GROWTH_BASE_RATE = 0.002
    GROWTH_HAPPINESS_MULT = 0.005
    GROWTH_FOOD_REQUIREMENT = 2.0

@dataclass(frozen=True)
class MarketRules:
    PRICE_ADJUSTMENT_RATE = 0.05
    MIN_PRICE = 0.1
    MAX_PRICE = 10.0
    
    SURPLUS_THRESHOLD = 1.5
    SHORTAGE_THRESHOLD = 0.7

@dataclass(frozen=True)
class EventsRules:
    EVENT_BASE_CHANCE = 0.01
    TECH_BREAKTHROUGH_CHANCE = 0.005
    PANDEMIC_CHANCE = 0.001
    ECONOMIC_BOOM_CHANCE = 0.03
    SCANDAL_CHANCE = 0.02

@dataclass(frozen=True)
class TraitsRules:
    TRAIT_POOL = ["Militarist", "Pacifist", "Industrialist", "Technocrat", "Populist", "Diplomat", "Imperialist", "Autocrat"]

@dataclass(frozen=True)
class Rules:
    Power = PowerRules
    Economy = EconomyRules
    Legitimacy = LegitimacyRules
    Conflict = ConflictRules
    War = WarRules
    Alliance = AllianceRules
    Weather = WeatherRules
    Demographics = DemographicsRules
    Market = MarketRules
    Events = EventsRules
    Traits = TraitsRules
