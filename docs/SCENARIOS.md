# Creating Custom Scenarios

This guide explains how to create custom worlds, factions, and regions for the Diane simulation engine.

---

## Overview

Diane supports two methods for scenario creation:

1. **Interactive Creation** (Discord Bot) - Build scenarios step-by-step with commands
2. **JSON Upload** - Define complete scenarios in structured JSON files

---

## Method 1: Interactive Creation (Discord)

### Quick Start

```
!new_scenario              # Initialize a new draft
!add_faction f_empire "The Empire" 80 40 100 Militarist Industrialist
!add_region r_capital "Capital City" f_empire URBAN 85
!view_draft                # Review your scenario
!start_custom "My Scenario"  # Launch simulation
```

### Available Commands

#### `!new_scenario`
Creates a fresh draft scenario for your user account.

#### `!capture_draft`
Captures the current active simulation state into your draft. Useful for:
- Saving interesting simulation states
- Capturing dynamically-created rebel factions
- Creating scenarios from evolved worlds

#### `!add_faction <id> <name> [power] [legitimacy] [resources] [traits...]`

Creates or updates a faction with specified parameters.

**Parameters:**
- `id` (required): Unique faction identifier (e.g., `f_empire`)
- `name` (required): Display name (use quotes for multi-word names)
- `power` (optional, default: 50.0): Initial military strength (0-100)
- `legitimacy` (optional, default: 50.0): Political support (0-100)
- `resources` (optional, default: 50.0): Starting economic resources
- `traits` (optional): Faction characteristics (see [Traits](#faction-traits))

**Example:**
```
!add_faction f_republic "United Republic" 60 85 120 Diplomat Pacifist
```

#### `!add_region <id> <name> [owner_id] [env_type] [infrastructure]`

Creates or updates a region.

**Parameters:**
- `id` (required): Unique region identifier (e.g., `r_capital`)
- `name` (required): Display name
- `owner_id` (optional): Faction ID that controls this region
- `env_type` (optional, default: RURAL): Environment type (see [Environment Types](#environment-types))
- `infrastructure` (optional, default: 20.0): Development level (0-100)

**Example:**
```
!add_region r_industrial "Iron Foundries" f_empire INDUSTRIAL 75
```

#### `!assign_region <region_id> <faction_id>`

Transfers control of an existing region to a faction.

**Example:**
```
!assign_region r_neutral_zone f_republic
```

#### `!view_draft`

Displays your current scenario configuration, including:
- All factions with their stats
- All regions with ownership
- Validation warnings

#### `!start_custom [session_name]`

Launches a simulation using your draft scenario.

**Example:**
```
!start_custom "Empire vs Republic"
```

---

## Method 2: JSON Scenario Upload

### JSON Structure

```json
{
  "factions": [
    {
      "id": "f_empire",
      "name": "Solar Empire",
      "power": 80.0,
      "legitimacy": 45.0,
      "resources": 100.0,
      "knowledge": 10.0,
      "traits": ["Militarist", "Industrialist"],
      "color": "#E74C3C"
    },
    {
      "id": "f_republic",
      "name": "United Republic",
      "power": 50.0,
      "legitimacy": 85.0,
      "resources": 80.0,
      "knowledge": 15.0,
      "traits": ["Diplomat", "Pacifist"],
      "color": "#3498DB"
    }
  ],
  "regions": [
    {
      "id": "r_capital",
      "name": "Imperial Capital",
      "population": 8000,
      "owner": "f_empire",
      "environment": "URBAN",
      "infrastructure": 90.0,
      "cohesion": 85.0
    },
    {
      "id": "r_colony",
      "name": "Frontier Colony",
      "population": 1200,
      "owner": "f_republic",
      "environment": "RURAL",
      "infrastructure": 40.0,
      "cohesion": 95.0
    },
    {
      "id": "r_neutral",
      "name": "Disputed Territory",
      "population": 500,
      "owner": null,
      "environment": "WILDERNESS",
      "infrastructure": 10.0,
      "cohesion": 30.0
    }
  ],
  "alliances": [
    ["f_empire", "f_ally1"],
    ["f_republic", "f_ally2"]
  ]
}
```

### Field Descriptions

#### Faction Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | ✓ | - | Unique identifier |
| `name` | string | ✓ | - | Display name |
| `power` | float | | 50.0 | Military strength (0-100) |
| `legitimacy` | float | | 50.0 | Political support (0-100) |
| `resources` | float | | 50.0 | Economic resources |
| `knowledge` | float | | 0.0 | Technological advancement |
| `traits` | array | | [] | Faction characteristics |
| `color` | string | | "#808080" | Hex color for visualizations |

#### Region Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | ✓ | - | Unique identifier |
| `name` | string | ✓ | - | Display name |
| `population` | integer | | 1000 | Population size |
| `owner` | string | | null | Controlling faction ID |
| `environment` | string | | "RURAL" | Environment type |
| `infrastructure` | float | | 20.0 | Development (0-100) |
| `cohesion` | float | | 100.0 | Social stability (0-100) |

### Upload Process

1. Create your JSON file (e.g., `my_scenario.json`)
2. In Discord, drag and drop the file
3. Add the comment: `!upload_scenario`
4. Wait for validation confirmation
5. Run `!start_custom` to begin simulation

---

## Reference Data

### Faction Traits

Traits modify faction behavior and bonuses:

| Trait | Effect |
|-------|--------|
| **Militarist** | Reduced military upkeep costs |
| **Pacifist** | Increased legitimacy from stability |
| **Industrialist** | Enhanced resource production |
| **Technocrat** | Faster research, reduced corruption |
| **Populist** | Higher base legitimacy |
| **Diplomat** | Alliance bonuses |
| **Imperialist** | Conquest advantages |
| **Autocrat** | Reduced legitimacy decay |

### Environment Types

Regions have different production profiles:

| Type | Primary Production | Secondary Effects |
|------|-------------------|-------------------|
| **URBAN** | Credits (×2) | High energy consumption |
| **COASTAL** | Credits, Food (fishing) | Naval power bonus |
| **INDUSTRIAL** | Materials, Energy | Pollution penalties |
| **RURAL** | Food (×3) | Population growth |
| **WILDERNESS** | Materials (low) | Minimal infrastructure |

---

## Best Practices

### Balanced Scenarios

For stable, long-running simulations:
- **Power Distribution**: Keep faction power within 2:1 ratio
- **Resource Allocation**: Ensure all factions have food/energy sources
- **Territory**: Distribute regions to avoid immediate conflicts
- **Legitimacy**: Start factions at 50-80 legitimacy for stability

### Conflict-Focused Scenarios

For dramatic, unstable worlds:
- **Power Imbalance**: Create 1-2 dominant factions (power > 80)
- **Resource Scarcity**: Limit food/energy production regions
- **Low Legitimacy**: Start factions at 20-40 legitimacy
- **Contested Regions**: Leave key territories unowned

### Historical Recreations

When modeling real-world scenarios:
- **Population Accuracy**: Use realistic population ratios
- **Geographic Traits**: Match environment types to real geography
- **Alliance Networks**: Reflect historical diplomatic ties
- **Power Asymmetry**: Capture actual military imbalances

---

## Validation Rules

The engine validates scenarios before launch:

### Faction Validation
- ✓ Unique IDs
- ✓ Power, legitimacy, resources within bounds (0-100)
- ✓ Valid trait names
- ✓ Color in hex format

### Region Validation
- ✓ Unique IDs
- ✓ Valid environment types
- ✓ Owner faction exists (if specified)
- ✓ Infrastructure and cohesion within bounds (0-100)
- ✓ Population > 0

### Cross-Reference Validation
- ✓ All region owners exist as factions
- ✓ All alliance members exist as factions
- ✓ No circular alliance dependencies

---

## Example Scenarios

### Scenario 1: Cold War

Two superpowers with satellite states:

```json
{
  "factions": [
    {"id": "f_west", "name": "Western Alliance", "power": 85, "legitimacy": 75, "traits": ["Diplomat", "Industrialist"]},
    {"id": "f_east", "name": "Eastern Bloc", "power": 80, "legitimacy": 60, "traits": ["Militarist", "Autocrat"]},
    {"id": "f_neutral", "name": "Non-Aligned", "power": 30, "legitimacy": 90, "traits": ["Pacifist"]}
  ],
  "regions": [
    {"id": "r_west_core", "name": "Western Heartland", "owner": "f_west", "environment": "INDUSTRIAL", "population": 5000},
    {"id": "r_east_core", "name": "Eastern Heartland", "owner": "f_east", "environment": "INDUSTRIAL", "population": 6000},
    {"id": "r_proxy", "name": "Proxy State", "owner": null, "environment": "RURAL", "population": 800}
  ]
}
```

### Scenario 2: Fragmented World

Many small factions competing:

```json
{
  "factions": [
    {"id": "f1", "name": "City-State Alpha", "power": 40, "legitimacy": 80},
    {"id": "f2", "name": "City-State Beta", "power": 35, "legitimacy": 70},
    {"id": "f3", "name": "City-State Gamma", "power": 45, "legitimacy": 65},
    {"id": "f4", "name": "City-State Delta", "power": 30, "legitimacy": 85}
  ],
  "regions": [
    {"id": "r1", "name": "Alpha Territory", "owner": "f1", "environment": "URBAN"},
    {"id": "r2", "name": "Beta Territory", "owner": "f2", "environment": "COASTAL"},
    {"id": "r3", "name": "Gamma Territory", "owner": "f3", "environment": "INDUSTRIAL"},
    {"id": "r4", "name": "Delta Territory", "owner": "f4", "environment": "RURAL"}
  ]
}
```

---

## Troubleshooting

### Common Issues

**"Faction not found" error**
- Ensure faction IDs match exactly (case-sensitive)
- Check that factions are defined before regions reference them

**"Invalid environment type"**
- Use exact names: URBAN, COASTAL, INDUSTRIAL, RURAL, WILDERNESS

**"Validation failed"**
- Run `!view_draft` to see specific errors
- Check that all values are within valid ranges

**Simulation crashes immediately**
- Ensure at least one faction has regions
- Verify all factions have positive power and legitimacy
- Check for resource scarcity (food/energy)

---

## Advanced Topics

### Dynamic Faction Creation

Factions can emerge during simulation through:
- **Revolutions**: Low legitimacy spawns rebel factions
- **Regional Revolts**: Unstable regions may secede
- **Civil Wars**: Internal conflicts split factions

Use `!capture_draft` to save these dynamic states.

### Scenario Balancing

Test your scenarios with:
```
!start_custom "Test Run"
!step 100
!metrics
```

Analyze:
- Power Gini (should be < 0.7 for balance)
- Resource security indices (> 5.0 recommended)
- Legitimacy trends (stable or growing)

Adjust initial conditions based on results.

---

**For detailed mechanics and configuration, see [RULES_GUIDE.md](RULES_GUIDE.md)**
