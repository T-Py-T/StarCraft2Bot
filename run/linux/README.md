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
# Download maps to Windows StarCraft II installation
python3 download_maps.py
```

### 3. Run Training
```bash
# Run the training script
uv run src/trainppo.py

# Or run the bot directly
uv run src/incredibot-sct.py
```

## Scripts

- **`download_maps.py`** - Downloads StarCraft II maps (works with WSL)

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