# Social Circle Simulation

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://pygame.org)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

A  cellular automaton simulation that models human social behavior and group dynamics. This  simulation explores emergent patterns in social contagion, demonstrating how individual interactions create complex population-level behaviors.

![circle](https://github.com/user-attachments/assets/8d8fdd16-d8b0-46a7-b3de-b9b1f9baf30d)
![second](https://github.com/user-attachments/assets/45178d51-dfe1-4275-b3ac-7acaa9a97bed)


## ✨ Features

- 🎬 **Real-time Visualization**: Watch behavior patterns emerge and evolve dynamically
- 🧠 **Complex Social Rules**: Individual and group-based interactions with realistic probability models
- 📊 **Population Dynamics**: Advanced birth, death, conversion, and migration mechanics
- 🎮 **Interactive Controls**: Toggle kill mechanics, pause simulation, adjust simulation speed
- 📈 **Statistical Tracking**: Comprehensive monitoring of population changes and behavioral shifts
- ⚖️ **Overpopulation Management**: Intelligent population control with crowding-based selection algorithms

## 🚀 Installation

### 📋 Prerequisites
- Python 3.11+ 🐍
- pip package manager 📦

### 🔧 Dependencies
```bash
pip install pygame numpy
```

### ⚡ Quick Start
```bash
git clone [your-repository-url]
cd human-behavior-simulation
python simulation.py
```

## 🔬 How It Works

### 🎯 Cell Types
- **🔴 Red (Bad)**: Represents negative behaviors or attitudes
- **🟢 Green (Good)**: Represents positive behaviors or attitudes  
- **⚫ Black**: Empty space

### ⚔️ Interaction Rules

#### 👤 Individual Interactions
- **Good vs Bad encounters**:
  - 3+ Bad neighbors → 75% kill Good, 25% convert to Bad
  - 2 Bad neighbors → 50% kill, 50% convert
  - 1 Bad neighbor → 50% chance both become same type

- **Bad vs Good encounters**:
  - 3+ Good neighbors → 90% convert Bad to Good, 10% kill
  - 2 Good neighbors → Convert Bad to Good
  - 1 Good neighbor → 50% chance both become same type

#### 👥 Group Dynamics
- **🔢 Large Groups** (4+ connected cells): Enhanced reproductive capabilities
  - 🔴 Bad groups: 60% spawn probability
  - 🟢 Good groups: 30% spawn probability
- **⚔️ Group Competition**: Strategic elimination of isolated opposing individuals

#### 📊 Population Control
- **🏠 Maximum Density**: 40% of total grid capacity
- **💥 Overpopulation Events**: Advanced crowding algorithms with weighted elimination
- **🚶 Random Movement**: Stochastic migration patterns to nearby vacant spaces

### 🎛️ Special Mechanics
- **🏝️ Isolation Death**: Homogeneous environments create 10% mortality risk
- **🎲 Random Conversion**: 1% spontaneous behavioral transformation probability
- **🔄 Kill Toggle**: Configurable death mechanics (converts lethal events to conversions)

## 🎮 Controls

| Key/Action | Function | Description |
|------------|----------|-------------|
| **R** | 🔄 Reset | Initialize new simulation |
| **SPACE** | ⏯️ Pause/Resume | Toggle simulation state |
| **+/=** | ⚡ Speed Up | Increase iteration rate |
| **-** | 🐌 Slow Down | Decrease iteration rate |
| **🖱️ Click Toggle** | 💀 Kill Mode | Enable/Disable elimination mechanics |

## ⚙️ Configuration

Parameters can be customized in `simulation.py`:

```python
CELL_SIZE = 4           # 🎨 Visual rendering scale
GRID_WIDTH = 200        # 📏 Horizontal grid dimensions  
GRID_HEIGHT = 150       # 📐 Vertical grid dimensions
MAX_POPULATION = 40%    # 🏠 Maximum sustainable density
INITIAL_POPULATION = 15% # 🌱 Starting population ratio
```

## 📈 Statistics Dashboard

The simulation provides comprehensive real-time analytics:
- **🔢 Generation**: Current evolutionary iteration
- **👥 Population**: Live count vs maximum system capacity
- **⚖️ Distribution**: Behavioral composition (Bad vs Good ratios)
- **📊 Events**: Per-generation conversions, deaths, and births tracking

## 🔍 Interesting Behaviors to Observe

- **🏘️ Cluster Formation**: Emergent homophily and spatial segregation
- **⚔️ Border Conflicts**: High-intensity dynamics at behavioral boundaries
- **📈 Population Cycles**: Complex demographic boom-bust patterns
- **🌊 Conversion Cascades**: Minority influence and tipping point phenomena
- **⚖️ Stability vs Chaos**: Equilibrium states versus perpetual oscillation

## 🛠️ Technical Architecture

- **🏗️ Built with**: Python, Pygame, NumPy
- **📊 Grid Architecture**: Configurable dimensions (default 200×150)
- **⚡ Performance**: Optimized spatial algorithms with bounded neighbor search
- **🧮 Algorithm**: Custom probabilistic cellular automaton with social physics

Made with ❤️ from NiceGuy
