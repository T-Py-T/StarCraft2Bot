# StarCraft2Bot - Windows Setup

This folder contains Windows-specific scripts and setup instructions for running the StarCraft II bot.

## Prerequisites

- Windows 10/11
- Python 3.9+ installed
- StarCraft II installed on Windows
- PowerShell (for running scripts)
- UV package manager (recommended)

## Quick Start

### 1. Install Dependencies
```powershell
# Install uv (if not already installed)
pip install uv

# Install project dependencies
uv sync
```

### 2. Test Scripts (Optional)
```powershell
# Test PowerShell script syntax
.\test_scripts.ps1
```

### 3. Setup StarCraft II Maps
```powershell
# Create the Maps directory (simple version - recommended)
.\download_maps_simple.ps1

# Place a genuine Simple64.SC2Map in the project Maps directory,
# then copy it into the StarCraft II installation
uv run create_simple_map.py

# Or try the full download script (may have issues with Xbox Game Pass version)
.\download_maps.ps1
```

### 4. Run Training
```powershell
# Run the training script
uv run src/trainppo.py

# Or run the bot directly
uv run src/incredibot-sct.py
```

## Scripts

- **`setup_maps.ps1`** - Creates Maps directory and provides instructions
- **`download_maps_simple.ps1`** - Simple version that just creates Maps directory (recommended)
- **`download_maps.ps1`** - Full version that tries to download maps (may have issues)
- **`create_simple_map.py`** - Copies a genuine `Simple64.SC2Map` archive from
  the project `Maps` directory into the StarCraft II installation. Set
  `SC2_MAP_SOURCE` to use a different source path.
- **`test_scripts.ps1`** - Tests PowerShell script syntax

## Configuration

The bot automatically detects your Windows StarCraft II installation and configures:
- SC2PATH environment variable
- Maps directory location
- Wandb settings (offline mode by default)

## Troubleshooting

### PowerShell Execution Policy
If you get execution policy errors, run:
```powershell
PowerShell -ExecutionPolicy Bypass -File script_name.ps1
```

### Missing Maps
If the bot can't find maps, run:
```powershell
.\download_maps_simple.ps1
# First place a genuine Simple64.SC2Map in the project Maps directory,
# or set SC2_MAP_SOURCE to its full path.
uv run create_simple_map.py
```

### Dependencies
If you get module errors, ensure you're using uv:
```powershell
uv sync
uv run python_script.py
```

### Xbox Game Pass Version
If you have StarCraft II from Xbox Game Pass, the download script may not work. In that case:
1. Use the `download_maps_simple.ps1` script to create Maps directory
2. Obtain a genuine map archive as described in the main
   [Game Maps](../../README.md#game-maps) guide
3. Use `create_simple_map.py` to copy that archive into the installation
4. Or use maps already included with the installation
