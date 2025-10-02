# StarCraft2Bot

I built this StarCraft II bot to explore deep reinforcement learning in complex real-time strategy environments. The bot uses PPO to learn Protoss strategies, focusing on Void Ray air superiority tactics. It's a custom RL environment that processes visual game state and learns strategic decision-making through trial and error.

## What I Built

- **PPO Training**: Using Stable Baselines3 with MLP policies to learn optimal actions
- **Custom RL Environment**: Gymnasium wrapper around StarCraft II with 224x224x3 visual observations
- **Computer Vision Pipeline**: OpenCV extracts game state from screen captures
- **Experiment Tracking**: Wandb logs training metrics and hyperparameter sweeps
- **Protoss Strategy**: Bot learns Gateway → Cybernetics Core → Stargate → Void Ray build orders

## How It Works

### RL Environment
- **State**: 224x224x3 RGB screenshots from the game
- **Actions**: 6 discrete choices (Expand/Mine, Build Stargate, Build Void Ray, Scout, Attack, Flee)
- **Rewards**: I designed a multi-objective system that rewards economic growth, military production, and tactical execution
- **Training**: PPO learns through trial and error, with hyperparameters tracked in Wandb

### Bot Strategy
- **Protoss Focus**: Specialized in Void Ray air superiority tactics
- **Economic AI**: Automatically manages worker distribution and resource optimization
- **Military AI**: Dynamic unit production, scouting, and combat micro-management
- **Build Orders**: Learns optimal progression from Gateway → Cybernetics Core → Stargate → Void Ray

### Tech Stack
- **ML**: PyTorch, Stable Baselines3, Gymnasium
- **Game API**: BurnySC2 (python-sc2) for StarCraft II integration
- **Vision**: OpenCV for real-time game state extraction
- **Tracking**: Wandb for experiment logging and hyperparameter sweeps
- **Dev Tools**: uv for dependency management, cross-platform support

## Requirements

- Python 3.9–3.12
- StarCraft II installed (see platform-specific setup below)
- [uv](https://github.com/astral-sh/uv) for dependency management

## Quick Start

1. **Clone and setup:**
   ```sh
   git clone https://github.com/T-Py-T/StarCraft2Bot.git
   cd StarCraft2Bot
   pip install uv
   uv sync
   ```

2. **Train the AI model:**
   ```sh
   make train
   ```

3. **Test trained model:**
   ```sh
   make test-model
   ```

## Platform Setup

### Windows (Recommended)
```powershell
# Install StarCraft II from Battle.net
# Update STARCRAFT_II_PATH_WINDOWS in src/config.py
cd run/windows
.\setup_maps.ps1
```

### Linux/WSL
```bash
# Install StarCraft II
# Update STARCRAFT_II_PATH_LINUX in src/config.py
cd run/linux
python3 download_maps.py
```

### macOS
```bash
# Use Parallels Desktop for best compatibility
# See run/macos/PARALLELS_SETUP.md for detailed instructions
make setup-macos
```

## Training & Evaluation

### ML Training Pipeline
```bash
# Start PPO training with experiment tracking
make train

# Train with custom hyperparameters
uv run src/trainppo.py

# Load and continue training existing model
uv run src/load-train-mlpp.py
```

### Model Testing & Evaluation
```bash
# Test trained model against AI opponents
make test-model

# Direct bot testing
make test-bot

# Manual model evaluation
uv run src/test_model.py
```

### Experiment Management
```bash
# Monitor training with Wandb
# Training metrics automatically logged to: https://wandb.ai/tnt850910/SC2RLv6

# Clean up training artifacts
make clean-models
make clean-logs
```

## Configuration

### Key Settings (`src/config.py`)
- **StarCraft II Path**: Set platform-specific paths for game installation
- **Wandb Mode**: Configure experiment tracking (offline/online)
- **Training Parameters**: Adjust PPO hyperparameters and training duration
- **Reward Engineering**: Modify reward weights for different strategic objectives

## Game Maps

### Map Setup
Place StarCraft II map files (`.SC2Map`) directly in the `Maps/` folder. The AI automatically detects available maps for training and testing.

### Recommended Maps
- **Training**: `Simple64`, `Simple96`, `Simple128` for focused learning
- **Testing**: Standard ladder maps for competitive evaluation
- **Download**: [Blizzard Map Packs](https://github.com/Blizzard/s2client-proto?tab=readme-ov-file#downloads) (password: `iagreetotheeula`)

## Project Architecture

### Core ML Components
```
src/
├── sc2env.py           # Custom Gymnasium RL environment
├── trainppo.py         # PPO training pipeline with Wandb integration
├── incredibot-sct.py   # StarCraft II bot AI implementation
├── test_model.py       # Model evaluation and testing
└── config.py           # Configuration and hyperparameters
```

### Architecture
- **Modular Design**: Clean separation between environment, training, and bot logic
- **Cross-Platform**: Works on Windows, Linux, macOS with automatic OS detection
- **Experiment Tracking**: Wandb integration for reproducible training runs
- **Configurable**: Easy hyperparameter tuning and training duration adjustment

## Current Status & Results

### Training Performance
- **Episodes**: Configurable training duration (default: 10,000 timesteps per episode)
- **Reward System**: Multi-objective rewards balancing economy, military production, and tactics
- **Convergence**: PPO with MLP policies shows stable learning curves

### What the Bot Learned
- **Economic Management**: Automated worker distribution and resource optimization
- **Military Production**: Dynamic Void Ray production and tactical deployment
- **Scouting**: Strategic reconnaissance and enemy base detection
- **Combat**: Unit positioning and engagement timing

## Next Steps

I'm working on several improvements:
- **Multi-Race Support**: Extending beyond Protoss to Terran and Zerg strategies
- **Advanced Vision**: Implementing semantic segmentation for better game state understanding
- **Hierarchical RL**: Adding high-level strategic planning on top of tactical execution
- **Self-Play**: Training against progressively stronger versions of itself
- **Performance Optimization**: Reducing training time and improving sample efficiency

## License

MIT License - See [LICENSE](LICENSE) for details