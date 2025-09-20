# StarCraft2Bot

A modern, modular StarCraft II bot and reinforcement learning (RL) training environment.

## Features

- Modular bot code for StarCraft II using [BurnySC2](https://github.com/BurnySc2/python-sc2)
- RL environment compatible with [OpenAI Gym](https://www.gymlibrary.dev/)
- PPO training and evaluation with [Stable Baselines3](https://stable-baselines3.readthedocs.io/)
- Experiment tracking with [Weights & Biases (wandb)](https://wandb.ai/)
- Fast, reproducible dependency management with [uv](https://github.com/astral-sh/uv)
- Cross-platform support: Windows, Linux, and macOS

## Requirements

- Python 3.9–3.12
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- StarCraft II installed (see platform-specific setup below)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/StarCraft2Bot.git
   cd StarCraft2Bot
   ```

2. **Install [uv](https://github.com/astral-sh/uv):**
   ```sh
   pip install uv
   ```

3. **Install dependencies:**
   ```sh
   uv sync
   ```

## Platform-Specific Setup

The bot automatically detects your operating system and configures itself accordingly. Choose your platform below:

### 🪟 Windows (Recommended)

**Best for:** Native StarCraft II installation, best performance

**Setup:**
1. Install StarCraft II from Battle.net or Xbox Game Pass
2. Update `STARCRAFT_II_PATH_WINDOWS` in `src/config.py` with your installation path
3. Run the Windows setup script:
   ```powershell
   cd run/windows
   .\setup_maps.ps1
   ```

**Quick Start:**
```powershell
# Navigate to Windows folder
cd run/windows

# Setup maps
.\setup_maps.ps1

# Create a simple test map
uv run create_simple_map.py

# Run training (from project root)
cd ../..
uv run src/trainppo.py
```

**See:** [run/windows/README.md](run/windows/README.md) for detailed Windows instructions.

### 🐧 Linux / WSL

**Best for:** Development, server deployment

**Setup:**
1. Install StarCraft II (native Linux or through WSL)
2. Update `STARCRAFT_II_PATH_LINUX` in `src/config.py` with your installation path
3. Run the Linux setup script:
   ```bash
   cd run/linux
   python3 download_maps.py
   ```

**Quick Start:**
```bash
# Setup maps
cd run/linux
python3 download_maps.py

# Run training
cd ../..
uv run src/trainppo.py
```

**See:** [run/linux/README.md](run/linux/README.md) for detailed Linux instructions.

### 🍎 macOS

**Best for:** Development with Parallels Desktop (recommended)

**Important:** StarCraft II is not natively available on macOS. Use Parallels Desktop for the best experience.

**Setup Options:**

**Option 1: Parallels Desktop (Recommended)**
- Install Parallels Desktop
- Create a Windows VM
- Install StarCraft II in the VM
- Run the bot from within the VM
- See [run/macos/PARALLELS_SETUP.md](run/macos/PARALLELS_SETUP.md) for detailed instructions

**Option 2: CrossOver (Limited Compatibility)**
- Download from [CodeWeavers](https://www.codeweavers.com/crossover)
- Install StarCraft II through CrossOver
- **Note:** CrossOver has limited compatibility with StarCraft II
- See [run/macos/README.md](run/macos/README.md) for detailed instructions

**Quick Start (Parallels):**
```bash
# Setup maps
make setup-macos

# Follow Parallels setup guide
open run/macos/PARALLELS_SETUP.md

# Set up remote development (develop on Mac, run on VM)
make setup-remote-dev

# Test bot in Windows VM
make test-remote

# Run training from within Windows VM
make train
```

**See:** [run/macos/README.md](run/macos/README.md) for detailed macOS instructions.

## Universal Usage (All Platforms)

Once you've completed the platform-specific setup above, the following commands work the same across all platforms:

### Quick Start with Makefile

The easiest way to get started is using the provided Makefile:

```bash
# Install dependencies and setup maps
make quick-start

# Check your environment setup
make check-env

# Start training
make train

# Test the bot
make test
```

### Available Makefile Commands

```bash
# Setup Commands
make install          # Install dependencies with uv
make setup-maps       # Setup maps for current platform
make setup-windows    # Setup for Windows
make setup-linux      # Setup for Linux
make setup-macos      # Setup for macOS

# Training Commands
make train            # Run basic PPO training
make train-ppo        # Run PPO training (explicit)
make train-mlpp       # Run MLPP training

# Testing Commands
make test             # Run all tests
make test-bot         # Test the bot directly
make test-model       # Test a trained model

# Utility Commands
make clean            # Clean temporary files
make clean-models     # Clean trained models
make clean-logs       # Clean log files
make clean-wandb      # Clean wandb files
make clean-all        # Clean everything
make build            # Build the package
make check-env        # Check environment setup
make status           # Show project status
```

### Manual Commands (Alternative)

If you prefer not to use the Makefile:

```bash
# Basic training
uv run src/trainppo.py

# Training with custom parameters
uv run src/load-train-mlpp.py

# Test a trained model
uv run src/test_model.py

# Test the bot directly
uv run src/test_bot.py
```

### Configuration

The bot automatically detects your operating system and configures itself accordingly:

1. **StarCraft II Path (OS-specific):**
   - **Windows:** Set `STARCRAFT_II_PATH_WINDOWS` in `src/config.py`
   - **Linux/WSL:** Set `STARCRAFT_II_PATH_LINUX` in `src/config.py`
   - **macOS:** Set appropriate macOS path in `src/config.py`

2. **Wandb Settings:**
   - **Offline mode:** By default, wandb runs in offline mode (no prompts)
   - **Silent mode:** Wandb prompts are disabled by default
   - To enable online mode, change `WANDB_MODE = "online"` in `src/config.py`

3. **Path Verification:**
   The bot automatically checks if the StarCraft II executable exists and warns you if it's not found.

## Map Files Setup

All StarCraft II map files (`.SC2Map`) should be placed directly in the `Maps` folder at the root of the project. There is no need for subfolders by season or type. The bot and the python-sc2 library will find maps by filename in this directory.

**Recommended structure:**
```
StarCraft2Bot/
  Maps/
    AbyssalReefLE.SC2Map
    AcropolisLE.SC2Map
    AscensiontoAiurLE.SC2Map
    AutomatonLE.SC2Map
    BattleontheBoardwalkLE.SC2Map
    BlackpinkLE.SC2Map
    BlueshiftLE.SC2Map
    CatalystLE.SC2Map
    CeruleanFallLE.SC2Map
    DiscoBloodbathLE.SC2Map
    EphemeronLE.SC2Map
    KairosJunctionLE.SC2Map
    NeonVioletSquareLE.SC2Map
    OdysseyLE.SC2Map
    ParaSiteLE.SC2Map
    PortAleksanderLE.SC2Map
    StasisLE.SC2Map
    ThunderbirdLE.SC2Map
    TritonLE.SC2Map
    WintersGateLE.SC2Map
    WorldofSleepersLE.SC2Map
    # Melee maps (for custom or empty scenarios):
    Empty128.SC2Map
    Flat32.SC2Map
    Flat48.SC2Map
    Flat64.SC2Map
    Flat96.SC2Map
    Flat128.SC2Map
    Simple64.SC2Map
    Simple96.SC2Map
    Simple128.SC2Map
```

- **Melee maps:** `Simple64`, `Simple96`, `Simple128`, `Empty128`, `Flat32`, `Flat48`, `Flat64`, `Flat96`, `Flat128` are for custom or empty scenarios.
- **PvP/PvAI maps:** All other `.SC2Map` files are standard competitive or AI ladder maps.

**Note:**
- If you add more maps, ensure their filenames do not conflict. If two maps have the same name, one will overwrite the other.
- You do not need to maintain the original Blizzard folder structure for maps; a flat folder is sufficient for python-sc2.

## Official Map and Replay Packs

For the most up-to-date and complete StarCraft II map packs (including ladder and melee maps), download directly from Blizzard:

- [Blizzard/s2client-proto Map and Replay Packs](https://github.com/Blizzard/s2client-proto?tab=readme-ov-file#downloads)

**Instructions:**
- Download the desired map pack zip file.
- Extract all `.SC2Map` files into your `Maps` folder (see above for structure).
- You may also extract replays for analysis or training.

The password for the map and replay packs is: `iagreetotheeula` (by using these files, you agree to the AI and Machine Learning License).

## Project Structure

```sh
StarCraft2Bot/
├── src/                # Core bot code (platform-independent)
│   ├── config.py       # Configuration settings (OS detection, paths)
│   ├── incredibot-sct.py
│   ├── sc2env.py
│   ├── trainppo.py
│   ├── load-train-mlpp.py
│   └── test_model.py
├── run/                # Platform-specific run scripts
│   ├── windows/        # Windows-specific scripts and setup
│   │   ├── README.md       # Windows setup instructions
│   │   ├── setup_maps.ps1  # PowerShell script for map setup
│   │   ├── download_maps.ps1 # PowerShell script for map downloads
│   │   └── create_simple_map.py # Python script for test maps
│   ├── linux/          # Linux-specific scripts and setup
│   │   ├── README.md       # Linux setup instructions
│   │   └── download_maps.py # Python script for map downloads
│   └── macos/          # macOS-specific scripts and setup
│       ├── README.md       # macOS setup instructions
│       └── setup_maps.py   # Python script for map setup
├── Maps/               # Downloaded maps (created by scripts)
├── tests/              # (Optional) Unit tests
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # uv dependency lock file
├── .gitignore
└── README.md
```

## Troubleshooting

### Common Issues

1. **"Unsupported operating system" warning**
   - This is expected if StarCraft II is not found
   - Follow the platform-specific setup instructions above

2. **"Maps directory not found" error**
   - This is common with Xbox Game Pass or incomplete StarCraft II installations
   - Run the appropriate platform setup script
   - Or use built-in maps (the bot now uses "Simple64" by default)

3. **macOS-specific issues**
   - StarCraft II is not natively available on macOS
   - Use Wine, CrossOver, or virtualization
   - See [run/macos/README.md](run/macos/README.md) for detailed instructions

### Performance Tips

- **Windows:** Best performance, native support
- **Linux:** Good performance, good for development
- **macOS:** May have performance issues with Wine/CrossOver, consider virtualization

## Contributing

Pull requests and issues are welcome! Please:

- Use clear commit messages
- Follow PEP8 style (run `ruff` and `mypy` for linting/type checks)
- Add tests for new features if possible

## License

MIT License. See [LICENSE](LICENSE) for details

## Known Warnings and Issues

- **DeprecationWarning in sc2process.py**
  - You may see a warning like:
    ```
    DeprecationWarning: parameter 'timeout' of type 'float' is deprecated, please use 'timeout=ClientWSTimeout(ws_close=...)'
    ```
  - This comes from the `python-sc2` package (not this repo) and does not affect functionality.
  - To fix: Wait for an upstream update, or manually edit your local `sc2process.py` to use the new `timeout` parameter as described in the warning.