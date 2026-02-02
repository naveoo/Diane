# Diane - Political Faction Simulation

Diane is a high-performance, modular political faction simulation engine. It models the complex interplay between power, economy, legitimacy, and regional stability in a dynamic world.

## 🚀 Quick Start

To run the demonstration simulation via CLI:

```powershell
python main.py
```

To run via **Discord Bot**:

1. Ensure `.env` contains your `BOT_TOKEN`.
2. Start the bot:
```powershell
python discord_bot.py
```
3. Use commands like `!start`, `!step 10`, `!status`.
4. **Custom Scenarios**: See [Creating Custom Scenarios](docs/SCENARIOS.md) for interactive and JSON-based world building.

This will run a 1000-tick simulation with two major factions and several regions, logging events like coups, civil wars, and alliances. All simulation data is saved in `diane_simulation.db`.

## 🏗️ Architecture

The project follows a modular, event-driven architecture using **Deltas** to manage state changes.

### Core Components
- **`engine.py`**: The central orchestrator (`SimulationEngine`). It manages the loop: Systems → Deltas → Validation → Application → Persistence.
- **`domains/`**: Data models for `Faction`, `Region`, and `World`. Optimized using `__slots__` and `@dataclass(slots=True)`.
- **`systems/`**: Specialized logic handlers:
    - `PowerSystem`: Branch-aware military growth (Army, Navy, Air).
    - `EconomySystem`: Resource generation based on regional infrastructure and environment.
    - `LegitimacySystem`: Support, Gini-based inequality, and resource starvation.
    - `ConflictSystem`: Revolts, Revolutions, Civil Wars, and Coups.
    - `AllianceSystem`: Diplomatic ties and faction traits.
    - `WarSystem`: Inter-faction conquest and regional expansion.
    - `InvestmentSystem`: Long-term development and maintenance.
    - `RegionSystem`: Climate-affected growth and socio-economic evolution.
    - `ResearchSystem`: Technological progression using Influence.
    - `TradeSystem`: Automatic resource exchange between allied factions.
- **Traits System**: Factions possess characteristic traits (Militarist, Industrialist, etc.) that modify core mechanics.
- **`deltas/`**: Efficient state transition management (`WorldDelta`) with validation.
- **`persistence/`**: SQLite-based storage for high-fidelity replay of every simulation tick.

## 📜 Key Mechanics

### 1. Power & Geography
Factions grow in power based on their controlled regions. Environment types (Urban, Coastal, Rural, etc.) provide distinct bonuses to different military branches and produce specialized resources:
- **Food** (Rural, Coastal): Essential for population and legitimacy.
- **Energy** (Industrial, Urban): Required for military and urban maintenance.
- **Materials** (Industrial): Used for infrastructure.

### 2. Legitimacy & Social Cohesion
Legitimacy is maintained through stability and economic stability. High inequality (Gini Coefficient) or starvation triggers unrest, potentially leading to revolutions or military coups.

### 3. Diplomatic Evolution
Alliances shift dynamically based on faction interests and diplomatic traits. Factions may cooperate for stability or compete for new territory.

### 4. High-Fidelity Persistence
The engine records every atomic state change, allowing for total simulation replay and branch analysis.

## 📂 Project Structure

```text
Diane/
├── deltas/           # Atomic change management
├── domains/          # Core data models (Factions, Regions)
├── persistence/      # SQLite storage and JSON serialization
├── rules/            # Configuration constants (defaults.py)
├── systems/          # Game logic implementations
├── docs/             # Detailed rules (RULES_GUIDE.md)
├── engine.py         # Main orchestration layer
└── main.py           # Demo entry point
```

## 🛠️ Configuration

All simulation parameters (growth rates, thresholds, chances) are centralizing in `rules/defaults.py`. You can adjust these to change the "feel" of the simulation.

---