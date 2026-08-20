# StarCraft2Bot - Linux/WSL Setup

This folder contains Linux/WSL-specific scripts for running the StarCraft II bot.

## Prerequisites

- WSL2 or Linux
- Python 3.9+
- StarCraft II installed on Windows (accessible via WSL)
- uv package manager

## Quick Start

### 1. Install Dependencies
```bash
# Install uv
pip install uv

# Install project dependencies
uv sync
```

### 2. Setup Maps (if needed)
```bash
# Copy maps already discoverable by python-sc2 into the SC2 and project folders
python3 download_maps.py
```

Despite its historical filename, `download_maps.py` does not fetch maps from
the network. If it cannot find any genuine `.SC2Map` archives, obtain them using
the main [Game Maps](../../README.md#game-maps) guide.

### 3. Run Training
```bash
# Run the training script
uv run src/trainppo.py

# Or run the bot directly
uv run src/incredibot-sct.py
```

## Scripts

- **`download_maps.py`** - Copies genuine maps already discoverable by
  python-sc2 into the configured SC2 installation and project `Maps` directory

## Configuration

The bot automatically:
- Detects WSL environment
- Sets SC2PATH to Windows StarCraft II installation
- Configures maps directory
- Sets wandb to offline mode

## Cross-Platform Notes

Since StarCraft II is installed on Windows, the bot will:
1. Access Windows StarCraft II installation via WSL
2. Run Python code in WSL environment
3. Communicate with Windows StarCraft II process

## Troubleshooting

### Missing Maps
If the bot can't find maps, ensure the Windows Maps directory exists:
```bash
# Check if Maps directory exists
ls -la "/mnt/e/XboxGames/StarCraft II/Maps/"

# If not, run the download script
python3 download_maps.py
```

### Dependencies
If you get module errors:
```bash
uv sync
uv run python_script.py
```
