# Configuration Guide - Political Faction Simulation

**Version:** 1.0  
**Last Updated:** February 2, 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Power System](#3-power-system)
4. [Legitimacy System](#4-legitimacy-system)
5. [Economic System](#5-economic-system)
6. [Global Analysis & Calibration](#6-global-analysis--calibration)
7. [Other System Configurations](#7-other-system-configurations)
8. [Conclusions & Recommendations](#8-conclusions--recommendations)

---

## 1. Introduction

This document provides comprehensive documentation for the `defaults.py` configuration file of the political faction simulation. It details each parameter, mathematical formulas, and provides guidance for analysis and calibration.

### 1.1 File Structure

The configuration file is organized into **nine main sections**, each grouping parameters for a specific system:

- `SimulationConfig`: General simulation parameters
- `FactionConfig`: Faction limits and default values
- `RegionConfig`: Region configuration
- `PowerConfig`: Power dynamics system
- `LegitimacyConfig`: Legitimacy system
- `EconomyConfig`: Economic system
- `ConflictConfig`: Conflict management
- `AllianceConfig`: Alliance management
- `TraitConfig`: Faction trait modifiers
- `CollapseConfig`: Faction collapse conditions

This modular organization enables easy maintenance and clear understanding of interdependencies.

### 1.2 Naming Conventions

| Prefix/Suffix | Meaning | Example |
|---------------|---------|---------|
| `default_*` | Initial values assigned to new entities | `default_power = 50.0` |
| `min_* / max_*` | Strict limits (bounds) for values | `min_power = 0.0` |
| `*_threshold` | Thresholds triggering events | `revolution_threshold = 25.0` |
| `*_chance` | Occurrence probabilities (0.0 to 1.0) | `revolution_chance = 0.15` |
| `*_factor / *_weight` | Multiplicative coefficients in formulas | `stability_legitimacy_factor = 0.3` |
| `*_bonus / *_penalty` | Additive modifiers | `alliance_power_bonus = 0.1` |

---

## 2. System Overview

The simulation relies on **three interdependent pillars** that evolve each tick:

### 2.1 The Three Main Systems

| System | Description | Primary Impact |
|--------|-------------|----------------|
| **Power** | Military and political strength of a faction | Increases with regions and alliances, naturally declines |
| **Legitimacy** | Popular acceptance and support | Influenced by stability, economic equality, and resources |
| **Economy** | Available resources for maintaining order | Grows with income, decreases through corruption |

### 2.2 Update Cycle

Each tick, the engine executes **in order**:

1. **Region Update** (`RegionSystem`)
2. **Power Update** (`PowerSystem`)
3. **Economy Update** (`EconomySystem`)
4. **Legitimacy Update** (`LegitimacySystem`)
5. **Alliance Update** (`AllianceSystem`)
6. **War Update** (`WarSystem`)
7. **Research Update** (`ResearchSystem`)
8. **Trade Update** (`TradeSystem`)
9. **Investment Update** (`InvestmentSystem`)
10. **Conflict Update** (`ConflictSystem`)

### 2.3 Key Interdependencies

```
Regions ──┬──> Power (+0.2/region)
          ├──> Resources (production bonuses)
          └──> Legitimacy (via average stability)

Resources ──> Legitimacy (penalty if scarce)

Power (all factions) ──> Legitimacy (via Gini coefficient)
```

---

## 3. Power System

### 3.1 Parameters (PowerConfig)

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `base_power_growth` | `0.01` | Natural growth (+1% per tick) |
| `power_decay` | `0.005` | Natural decline (-0.5% per tick) |
| `region_power_weight` | `0.2` | Bonus per controlled region |
| `alliance_power_bonus` | `0.1` | Bonus per active alliance |
| `max_power` | `100.0` | Maximum power ceiling |

### 3.2 Mathematical Formula

Power for a faction is updated according to the following sequence:

#### Step 1: Base Growth
```
power_new = power × (1 + base_power_growth)
```

#### Step 2: Natural Decay
```
power_new = power_new × (1 - power_decay)
```

#### Step 3: Regional Bonus (if regions controlled)
```
power_new = power_new + (num_regions × region_power_weight)
```

#### Step 4: Alliance Bonus (if alliances active)
```
power_new = power_new + (num_alliances × alliance_power_bonus)
```

#### Step 5: Apply Ceiling
```
power_final = min(power_new, max_power)
```

### 3.3 Consolidated Formula

```
power(t+1) = min(
    power(t) × (1 + base_power_growth) × (1 - power_decay)
    + (num_regions × region_power_weight)
    + (num_alliances × alliance_power_bonus),
    max_power
)
```

### 3.4 Analysis & Calibration

#### Net Growth Without Territory

With default values:
```
Net rate = (1 + 0.01) × (1 - 0.005) = 1.01 × 0.995 ≈ 1.00495
```
Approximately **+0.5% per tick**. A faction without territory gains power very slowly.

#### Territorial Impact

Each region adds **+0.2** raw power per tick (before multipliers).

**Example:**
- Faction with 5 regions: +1.0 raw power/tick
- After multipliers: ~+1.005 additional

#### Growth Scenarios

| Situation | Initial Power | After 100 ticks | After 1000 ticks |
|-----------|---------------|-----------------|------------------|
| No territory | 50.0 | ~52.5 | ~82.4 |
| 3 regions | 50.0 | ~70.3 | 100.0 (ceiling) |
| 5 regions | 50.0 | ~80.5 | 100.0 (ceiling) |

#### Calibration Recommendations

**For faster growth:**
- Increase `base_power_growth` (e.g., `0.02` = +2%/tick)
- Result: Factions reach ceiling faster

**To prioritize territorial expansion:**
- Increase `region_power_weight` (e.g., `0.5`)
- Result: Territorial control becomes decisive

**To stabilize great powers:**
- Reduce `max_power` (e.g., `80.0`)
- Result: Ceiling reached earlier, forces balance

**For more pronounced decline:**
- Increase `power_decay` (e.g., `0.01` = -1%/tick)
- Result: Factions must constantly conquer to compensate

---

## 4. Legitimacy System

### 4.1 Parameters (LegitimacyConfig)

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `base_legitimacy_decay` | `0.01` | Natural erosion (-1%/tick) |
| `stability_legitimacy_factor` | `0.3` | Stability→legitimacy conversion coefficient |
| `inequality_penalty` | `0.4` | Inequality penalty (Gini coefficient) |
| `starvation_legitimacy_loss` | `0.5` | Absolute loss if famine |
| `revolution_threshold` | `25.0` | Threshold triggering revolutions |
| `revolution_chance` | `0.15` | 15% probability if below threshold |
| `legitimacy_floor` | `0.0` | Absolute minimum |
| `legitimacy_ceiling` | `100.0` | Absolute maximum |

### 4.2 Mathematical Formula

#### Step 1: Base Decay
```
legitimacy = legitimacy × (1 - base_legitimacy_decay)
```

#### Step 2: Regional Stability Bonus
```
avg_stability = Σ(region.cohesion) / num_regions

legitimacy = legitimacy + (avg_stability × stability_legitimacy_factor)
```

**Note:** This bonus is only applied if the faction controls at least one region.

#### Step 3: Inequality Penalty (Gini Coefficient)

The Gini coefficient measures power distribution inequality among **all active factions** (power ≠ 0).

```
gini_coefficient = gini([f.power for f in active_factions])  // ∈ [0, 1]

legitimacy = legitimacy - (gini_coefficient × inequality_penalty × 100)
```

**Gini Interpretation:**
- `0.0`: Perfect equality (all factions have equal power)
- `0.5`: Moderate inequality
- `1.0`: Total monopoly (one faction holds all power)

#### Step 4: Starvation Penalty
```
If food < food_threshold OR energy < energy_threshold:
    legitimacy = legitimacy - starvation_legitimacy_loss
```

#### Step 5: Apply Limits
```
legitimacy = clamp(legitimacy, legitimacy_floor, legitimacy_ceiling)
```

### 4.3 Consolidated Formula

```
legitimacy(t+1) = clamp(
    legitimacy(t) × (1 - base_legitimacy_decay)
    + (avg_stability × stability_legitimacy_factor)
    - (gini × inequality_penalty × 100)
    - (starvation_penalty if resources scarce),
    0.0,
    100.0
)
```

### 4.4 Analysis & Calibration

#### Gini Coefficient Impact

| Gini | Meaning | Penalty (inequality_penalty=0.4) |
|------|---------|----------------------------------|
| 0.0 | Perfect equality | 0 points |
| 0.3 | Low inequality | -12 points |
| 0.5 | Average inequality | -20 points |
| 0.7 | High inequality | -28 points |
| 1.0 | Total monopoly | -40 points |

**Implications:**
- A dominant faction (high Gini) reduces legitimacy for **all** factions
- Encourages power balance
- Can trigger revolutions even for stable factions if global inequality is high

#### Typical Scenarios

**Scenario 1: Stable Faction with Territories**
- Average regional stability: 80.0
- Global Gini: 0.3 (low inequality)
- Resources: 30.0 (no famine)

```
legitimacy(t+1) = legitimacy(t) × 0.99
                  + (80.0 × 0.3)
                  - (0.3 × 0.4 × 100)
                = legitimacy(t) × 0.99 + 24.0 - 12.0
                = legitimacy(t) × 0.99 + 12.0
```
**Result:** Legitimacy gradually increases.

**Scenario 2: Faction in Famine in Unequal World**
- Average stability: 60.0
- Global Gini: 0.8 (high inequality)
- Resources: 3.0 (famine)

```
legitimacy(t+1) = legitimacy(t) × 0.99
                  + (60.0 × 0.3)
                  - (0.8 × 0.4 × 100)
                  - 0.5
                = legitimacy(t) × 0.99 + 18.0 - 32.0 - 0.5
                = legitimacy(t) × 0.99 - 14.5
```
**Result:** Rapid legitimacy decline (approximately -15 points/tick).

#### Calibration Recommendations

**To slow legitimacy decline:**
- Reduce `base_legitimacy_decay` to `0.005` (-0.5%/tick)
- Increase `stability_legitimacy_factor` to `0.5` to value stability

**To tolerate more inequality:**
- Reduce `inequality_penalty` to `0.2`
- Result: Gini of 1.0 inflicts -20 instead of -40

**For more frequent revolutions:**
- Increase `revolution_chance` to `0.30` (30%)
- Or increase `revolution_threshold` to `35.0`

**For more tolerable famine situations:**
- Reduce `starvation_legitimacy_loss` to `0.2`
- Or adjust resource thresholds

---

## 5. Economic System

### 5.1 Parameters (EconomyConfig)

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `base_credits_income` | `5.0` | Base credit income per tick |
| `base_materials_income` | `2.0` | Base materials income per tick |
| `base_influence_income` | `1.0` | Base influence income per tick |
| `region_credits_factor` | `2.0` | Credit production multiplier |
| `region_materials_factor` | `1.0` | Materials production multiplier |
| `upkeep_power_factor` | `0.5` | Credit upkeep per power point |
| `corruption_factor` | `0.02` | Corruption/tax rate (2%) |
| `food_per_population` | `0.01` | Food consumption per capita |
| `energy_per_power` | `0.1` | Energy consumption per power point |

### 5.2 Specialized Resource Production

Resources are produced based on region environment types:

| Environment | Credits | Materials | Food | Energy |
|-------------|---------|-----------|------|--------|
| **URBAN** | High (×2) | Low | Low | Negative (consumption) |
| **COASTAL** | Medium (×1.25) | Medium | Medium (fishing) | Neutral |
| **INDUSTRIAL** | Low (×0.5) | Very High (×2.5) | None | High (power plants) |
| **RURAL** | Low | Low | Very High (×3) | None |
| **WILDERNESS** | None | Low (×0.3) | None | None |

### 5.3 Mathematical Formula

#### Step 1: Base Income
```
credits += base_credits_income
materials += base_materials_income
influence += base_influence_income
food += 1.0
energy += 0.5
```

#### Step 2: Regional Production
For each controlled region:
```
pop_factor = region.population / 1000.0
dev_mult = 1.0 + (region.infrastructure / 100.0)
efficiency = region.cohesion / 100.0

Apply environment-specific bonuses (see table above)
```

#### Step 3: Consumption
```
food_required = total_population × food_per_population
energy_required = faction.power.total × energy_per_power

food -= food_required
energy -= energy_required
```

#### Step 4: Upkeep Costs
```
upkeep = faction.power.total × upkeep_power_factor
credits -= upkeep
```

#### Step 5: Corruption/Tax
```
credits *= (1 - corruption_factor)
materials *= (1 - corruption_factor)
food *= 0.98  // Storage loss
energy *= 0.98  // Transmission loss
```

### 5.4 Resource Scarcity Effects

**Food Shortage (food < 0):**
- Legitimacy loss: `starvation_ratio × 5.0`
- Event: "FOOD SHORTAGE! Legitimacy dropping"
- Food set to 0

**Energy Crisis (energy < 0):**
- Event: "ENERGY CRISIS!"
- Energy set to 0
- Potential future penalties

### 5.5 Calibration Recommendations

**To increase resource accumulation:**
- Increase `base_*_income` values
- Increase `region_*_factor` multipliers

**To make economy more challenging:**
- Increase `corruption_factor` to `0.05` (5% loss)
- Increase consumption rates

**To adjust scarcity thresholds:**
- Modify `food_per_population` and `energy_per_power`

---

## 6. Global Analysis & Calibration

### 6.1 System Interdependencies

#### Economy → Legitimacy
```
resources < threshold  ──> legitimacy -= penalty/tick
```
**Impact:** A faction in famine rapidly loses legitimacy, risking revolution.

#### Power → Legitimacy (via Gini)
```
Unequal power distribution  ──> High Gini  ──> Penalty for all factions
```
**Impact:** A dominant faction destabilizes the entire political system.

#### Regions → All Systems
```
Regions ──┬──> Power (+0.2/region)
          ├──> Resources (production bonuses)
          └──> Legitimacy (via average stability)
```
**Impact:** Territorial control is crucial, but unstable regions can be counterproductive.

### 6.2 Recommended Test Scenarios

#### Scenario 1: Isolated Faction Without Territory

**Configuration:**
- Initial power: 50.0
- Initial legitimacy: 50.0
- Initial resources: 50.0
- Regions: 0
- Alliances: 0

**Objectives:**
- Verify base growth/decline rates
- Observe economic effects

**Expected Results:**
- Power: Very slow growth (~0.5%/tick)
- Legitimacy: Slow decline (-1%/tick) then stabilization
- Resources: Linear growth (+income/tick before corruption)

#### Scenario 2: Two Balanced Factions

**Configuration:**
- 2 factions with power = 50.0 each
- Each faction controls 3 regions (stability = 100.0)

**Objectives:**
- Observe Gini coefficient impact (close to 0)
- Verify stability bonus

**Expected Results:**
- Gini ≈ 0.0 → low legitimacy penalty
- Legitimacy increases thanks to regional stability
- Stable and sustainable situation

#### Scenario 3: Dominant Faction (Monopoly)

**Configuration:**
- Faction A: power = 90.0, 8 regions
- Faction B: power = 10.0, 1 region

**Objectives:**
- Verify inequality collapse
- Test revolution triggering

**Expected Results:**
- Gini ≈ 0.8-0.9 → penalty of -32 to -36 points
- Legitimacy of all factions drops
- Revolution likely if legitimacy < 25.0

### 6.3 Metrics to Monitor

#### Global Metrics
- **Gini Coefficient**: Measures power inequality
- **Number of Active Factions**: Factions with power > 0
- **Total Power**: Sum of all powers
- **Resource Security Indices**: Food and energy supply ratios

#### Per-Faction Metrics
- **Power**: Value and trend (growth/decline)
- **Legitimacy**: Value and number below revolution threshold
- **Resources**: Value and number in famine
- **Number of Controlled Regions**
- **Average Stability**: Of controlled regions
- **Number of Alliances**

#### Event Metrics
- **Number of Revolutions Triggered**
- **Number of Collapsed Factions**
- **Number of Revolts**
- **Alliance Formations/Breaks**

---

## 7. Other System Configurations

### 7.1 Simulation Configuration (SimulationConfig)

```python
@dataclass(frozen=True)
class SimulationConfig:
    max_ticks: int = 1_000_000
    snapshot_interval: int = 100
    base_tick_duration: float = 1.0
```

### 7.2 Faction Configuration (FactionConfig)

```python
@dataclass(frozen=True)
class FactionConfig:
    default_power: float = 50.0
    min_power: float = 0.0
    max_power: float = 100.0
    
    default_legitimacy: float = 50.0
    min_legitimacy: float = 0.0
    max_legitimacy: float = 100.0
    
    default_resources: float = 50.0
    min_resources: float = -100.0
    max_resources: float = 1000.0
```

### 7.3 Trait Configuration (TraitConfig)

Faction traits modify core mechanics:

| Trait | Effect |
|-------|--------|
| **Militarist** | `upkeep_mod = 0.8` (20% reduction) |
| **Pacifist** | `legitimacy_bonus = 1.2` (20% increase) |
| **Industrialist** | `income_mod = 1.3` (30% increase) |
| **Technocrat** | `research_efficiency = 1.5`, `corruption_mod = 0.7` |
| **Populist** | `base_legitimacy = 60.0` (higher starting) |
| **Diplomat** | Alliance bonuses |
| **Imperialist** | Conquest advantages |
| **Autocrat** | Reduced legitimacy decay |

### 7.4 Alliance Configuration (AllianceConfig)

```python
@dataclass(frozen=True)
class AllianceConfig:
    trade_threshold: float = 50.0
    trade_shortage_threshold: float = 10.0
    trade_amount: float = 10.0
    trade_credit_bonus: float = 2.0
    trade_legitimacy_bonus: float = 0.5
```

---

## 8. Conclusions & Recommendations

### 8.1 Recommended Configurations by Playstyle

#### "Balanced" Style (Default)

Current configuration after bug fixes.

#### "Rapid Expansion" Style

```python
PowerConfig:
    base_power_growth = 0.02
    region_power_weight = 0.5
    alliance_power_bonus = 0.2

EconomyConfig:
    base_credits_income = 10.0
    base_materials_income = 4.0
    corruption_factor = 0.01
```

#### "Difficult Survival" Style

```python
LegitimacyConfig:
    base_legitimacy_decay = 0.02
    inequality_penalty = 0.6
    revolution_threshold = 30.0
    revolution_chance = 0.25

EconomyConfig:
    corruption_factor = 0.05
    food_per_population = 0.02
```

#### "Dominant Empire" Style

```python
PowerConfig:
    max_power = 200.0
    region_power_weight = 1.0

LegitimacyConfig:
    inequality_penalty = 0.2

CollapseConfig:
    faction_power_floor = 1.0
```

### 8.2 Recommended Unit Tests

#### Test 1: Growth Without Territory
```python
def test_power_growth_no_territory():
    faction = Faction(power=50.0, regions=[], alliances=[])
    for _ in range(100):
        update_power(faction)
    assert 52.0 < faction.power < 53.0
```

#### Test 2: Gini Impact
```python
def test_gini_penalty():
    faction1 = Faction(power=90.0, legitimacy=50.0)
    faction2 = Faction(power=10.0, legitimacy=50.0)
    
    update_legitimacy([faction1, faction2])
    
    assert faction1.legitimacy < 50.0
    assert faction2.legitimacy < 50.0
```

---

**For implementation details and code examples, see the source code in `core/defaults.py` and `systems/` directory.**
