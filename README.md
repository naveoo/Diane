# Diane - Geopolitical Faction Simulation Engine

**A high-performance, modular simulation engine for modeling complex political dynamics, resource economics, and diplomatic relations in dynamic worlds.**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/discord-bot%20ready-7289da.svg)](https://discord.com/)

---

## 🌍 Overview

Diane is a sophisticated political faction simulation framework designed for researchers, game developers, and enthusiasts interested in modeling geopolitical systems. The engine simulates the intricate interplay between military power, economic resources, political legitimacy, and regional stability across multiple factions competing for dominance.

### Key Features

- **🎯 Multi-System Architecture**: Modular systems for power dynamics, economy, legitimacy, conflicts, alliances, research, and trade
- **📊 Advanced Analytics**: Comprehensive metrics including Gini coefficients, Hegemony Index (HHI), resource security indices, and diplomatic fragmentation
- **📈 Historical Tracking**: SQLite-based persistence with full simulation replay capability
- **🤖 Discord Integration**: Full-featured bot for interactive simulation management and real-time visualization
- **📉 Data Visualization**: Automatic chart generation for metrics, power distribution, and historical trends
- **🔧 Highly Configurable**: Centralized configuration system for fine-tuning simulation parameters

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/diane.git
   cd diane
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (for Discord bot)
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

### Running the Simulation

#### Command-Line Interface

Run a demonstration simulation with default scenarios:

```bash
python main.py
```

This executes a 100-tick simulation with three major factions, logging events such as power shifts, economic crises, and diplomatic changes. All data is persisted to `diane_simulation.db`.

#### Discord Bot

For interactive simulation management:

```bash
python discord_bot.py
```

**Available Commands:**
- `!start [name]` - Initialize a new simulation session
- `!step [ticks]` - Advance simulation by N ticks
- `!status` - Display current faction states
- `!metrics` - Generate comprehensive analytics with charts
- `!history` - View historical evolution graphs
- `!rankings [category]` - Show top factions by power/economy/stability
- `!compare <faction1> <faction2>` - Detailed faction comparison

See [SCENARIOS.md](docs/SCENARIOS.md) for custom world creation.

---

## 🏗️ Architecture

### Core Components

```
Diane/
├── engine.py           # Central orchestration layer
├── domains/            # Data models (Faction, Region, World)
├── systems/            # Game logic modules
│   ├── power.py        # Military strength dynamics
│   ├── economy.py      # Resource management
│   ├── legitimacy.py   # Political support
│   ├── conflict.py     # Revolts, wars, coups
│   ├── alliance.py     # Diplomatic relations
│   ├── research.py     # Technological advancement
│   └── trade.py        # Resource exchange
├── deltas/             # State change management
├── persistence/        # SQLite storage
├── metrics.py          # Geopolitical analytics
├── visualizer.py       # Chart generation
├── rules/              # Configuration (defaults.py)
└── docs/               # Detailed documentation
```

### Design Principles

- **Event-Driven Architecture**: All state changes are managed through validated deltas
- **Modular Systems**: Each system (Power, Economy, etc.) operates independently with clear interfaces
- **Data Persistence**: Every tick is recorded for complete simulation replay
- **Performance Optimized**: Uses `__slots__` and `@dataclass(slots=True)` for memory efficiency

---

## 📜 Simulation Mechanics

### 1. Power & Military Dynamics

Factions accumulate military power through:
- **Territorial Control**: Each region provides power bonuses based on environment type
- **Branch Specialization**: Army, Navy, and Air Force grow independently
- **Alliance Networks**: Diplomatic ties provide strategic advantages

**Environment-Specific Bonuses:**
- **Urban**: High credit generation, energy consumption
- **Coastal**: Naval power, fishing resources
- **Industrial**: Materials and energy production
- **Rural**: Food production, population growth
- **Wilderness**: Raw material extraction

### 2. Economic System

The economy operates on four specialized resources:

| Resource | Production | Consumption | Critical For |
|----------|-----------|-------------|--------------|
| **Credits** | Taxation, trade | Military upkeep | Faction operations |
| **Materials** | Industrial regions | Infrastructure | Development |
| **Food** | Rural/coastal regions | Population | Legitimacy |
| **Energy** | Industrial regions | Military, urban | Power projection |

**Resource Scarcity**: Shortages trigger legitimacy penalties and potential collapse.

### 3. Legitimacy & Stability

Political support is influenced by:
- **Regional Cohesion**: Average stability across controlled territories
- **Economic Equality**: Gini coefficient penalties for power imbalances
- **Resource Security**: Food and energy shortages reduce legitimacy
- **Starvation Events**: Severe penalties for prolonged resource crises

**Critical Thresholds:**
- Legitimacy < 25: Revolution risk
- Regional stability < 30: Revolt risk
- Resources < threshold: Starvation penalties

### 4. Research & Technology

Factions invest **Influence** to gain **Knowledge**, which:
- Enhances Composite Power Index (CPI)
- Provides technological advantages
- Unlocks future bonuses (configurable)

### 5. Trade & Diplomacy

Allied factions automatically exchange resources:
- Surplus energy/food traded for mutual benefit
- Trade increases credits and legitimacy
- Strengthens alliance bonds

---

## 📊 Advanced Analytics

### Geopolitical Metrics

**World-Level Indicators:**
- **Hegemony Index (HHI)**: Power concentration (0 = competition, 1 = monopoly)
- **Power Gini**: Inequality in military strength distribution
- **Global Tension**: Predictor of conflict likelihood
- **Resource Security**: Food and energy supply vs. demand ratios
- **Diplomatic Fragmentation**: Percentage of isolated factions

**Faction-Level Indicators:**
- **Composite Power Index (CPI)**: Knowledge-weighted military strength
- **Strategic Depth**: Population distribution entropy
- **Economic Intensity**: Resources per capita
- **Threat Assessment**: Cumulative danger from hostile factions
- **Diplomatic Influence**: Alliance network strength

### Visualization

The system generates professional charts:
- **Power Distribution** (Pie Chart)
- **Resource Security** (Bar Chart)
- **World Indicators** (Horizontal Bar)
- **Power Evolution** (Time Series)
- **Legitimacy Trends** (Time Series)
- **Resource Evolution** (Multi-Line)

---

## 🔧 Configuration

All simulation parameters are centralized in `core/defaults.py`:

```python
@dataclass(frozen=True)
class PowerConfig:
    base_power_growth: float = 0.01
    power_decay: float = 0.005
    region_power_weight: float = 0.2
    alliance_power_bonus: float = 0.1
    max_power: float = 100.0
```

**Configuration Categories:**
- `SimulationConfig`: Tick duration, snapshot intervals
- `PowerConfig`: Military growth and decay rates
- `EconomyConfig`: Resource production and consumption
- `LegitimacyConfig`: Stability thresholds and penalties
- `ConflictConfig`: Revolution and revolt probabilities
- `AllianceConfig`: Trade and diplomatic parameters

See [RULES_GUIDE.md](docs/RULES_GUIDE.md) for comprehensive parameter documentation.

---

## 📖 Documentation

- **[SCENARIOS.md](docs/SCENARIOS.md)**: Creating custom worlds and factions
- **[RULES_GUIDE.md](docs/RULES_GUIDE.md)**: Detailed mechanics and configuration reference
- **API Documentation**: (Coming soon)

---

## 🛠️ Development

### Project Structure

- **Domains**: Immutable data models with `__slots__` optimization
- **Systems**: Stateless logic processors implementing `BaseSystem`
- **Deltas**: Atomic state changes with validation
- **Persistence**: SQLite for snapshots, JSON for serialization

### Adding New Systems

1. Create a new class inheriting from `BaseSystem`
2. Implement `compute_delta(world, builder)` method
3. Register in `engine.py` systems list
4. Add configuration to `rules/defaults.py`

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by geopolitical simulation frameworks and grand strategy games
- Built with Python's dataclasses and modern type hints
- Discord.py for bot integration
- Matplotlib for visualization

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

**Made with ❤️ for simulation enthusiasts and geopolitical researchers**