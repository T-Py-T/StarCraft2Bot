# StarCraft II PPO Agent Makefile
# Common tasks for training, evaluation, and setup

.PHONY: help install setup-maps train train-ppo train-mlpp test test-live test-bot test-model clean clean-models clean-logs clean-wandb clean-all build check-env setup-windows setup-linux setup-macos

# Default target
help:
	@echo "StarCraft II PPO Agent - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install          Install dependencies with uv"
	@echo "  setup-maps       Setup maps for current platform"
	@echo "  setup-windows    Setup for Windows"
	@echo "  setup-linux      Setup for Linux"
	@echo "  setup-macos      Setup for macOS"
	@echo ""
	@echo "Training Commands:"
	@echo "  train            Run basic PPO training"
	@echo "  train-ppo        Run PPO training (explicit)"
	@echo "  train-mlpp       Run MLPP training"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test             Run headless unit tests"
	@echo "  test-live        Run SC2 and model integration tests"
	@echo "  test-bot         Test the bot directly"
	@echo "  test-model       Test a trained model"
	@echo ""
	@echo "Utility Commands:"
	@echo "  clean            Clean temporary files"
	@echo "  clean-models     Clean trained models"
	@echo "  clean-logs       Clean log files"
	@echo "  clean-wandb      Clean wandb files"
	@echo "  clean-all        Clean everything"
	@echo "  build            Build the package"
	@echo "  check-env        Check environment setup"
	@echo ""

# Installation
install:
	@echo "Installing dependencies with uv..."
	uv sync

# Map setup (platform-specific)
setup-maps:
	@echo "Setting up maps for current platform..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "macOS detected - running macOS setup..."; \
		cd run/macos && python3 setup_maps.py; \
	elif [ "$$(uname)" = "Linux" ]; then \
		echo "Linux detected - running Linux setup..."; \
		cd run/linux && python3 download_maps.py; \
	else \
		echo "Windows detected - please run: cd run/windows && .\\setup_maps.ps1"; \
	fi

# Platform-specific setup
setup-windows:
	@echo "Setting up for Windows..."
	@echo "Please run the following commands in PowerShell:"
	@echo "  cd run/windows"
	@echo "  .\\setup_maps.ps1"
	@echo "  uv run create_simple_map.py"

setup-linux:
	@echo "Setting up for Linux..."
	cd run/linux && python3 download_maps.py

setup-macos:
	@echo "Setting up for macOS with CrossOver..."
	cd run/macos && python3 setup_maps.py
	@python3 src/sc2_crossover_launcher_v3.py

# Training commands
train: train-ppo

train-ppo:
	@echo "Starting PPO training..."
	uv run src/trainppo.py

train-mlpp:
	@echo "Starting MLPP training..."
	uv run src/load-train-mlpp.py

# Testing commands
test:
	@echo "Running headless unit tests..."
	uv run pytest -q tests

test-live: test-bot test-model

test-bot:
	@echo "Testing bot directly..."
	uv run src/test_bot.py

# macOS-specific test
test-macos:
	@echo "Testing bot with CrossOver setup..."
	@python3 src/sc2_crossover_launcher_v3.py
	@uv run src/test_bot_enhanced.py

# Remote development with Parallels Windows VM
setup-remote-dev:
	@echo "Setting up remote development with Parallels Windows VM..."
	@./scripts/setup_remote_dev.sh

test-remote:
	@echo "Testing bot in Windows VM..."
	@ssh starcraft2-vm "cd starcraft2-ppo-agent && uv run src/test_bot.py"

sync-and-run:
	@echo "Syncing changes and running bot in Windows VM..."
	@./sync_and_run.sh

test-model:
	@echo "Testing trained model..."
	uv run src/test_model.py

# Environment check
check-env:
	@echo "Checking environment setup..."
	@echo "Python version:"
	@uv run python --version
	@echo ""
	@echo "Platform: $$(uname)"
	@echo ""
	@echo "Checking StarCraft II configuration..."
	@uv run python -c "from src.config import IS_WINDOWS, IS_LINUX, IS_MACOS; print('Config loaded successfully')"
	@echo ""
	@echo "Dependencies:"
	@uv run python -c "import sc2, gymnasium, stable_baselines3, wandb; print('All dependencies available')"

# Build
build:
	@echo "Building package..."
	uv build

# Cleanup commands
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".DS_Store" -delete

clean-models:
	@echo "Cleaning trained models..."
	rm -rf src/models/*/
	@echo "Models cleaned."

clean-logs:
	@echo "Cleaning log files..."
	rm -rf src/logs/*/
	@echo "Logs cleaned."

clean-wandb:
	@echo "Cleaning wandb files..."
	rm -rf src/wandb/
	@echo "Wandb files cleaned."

clean-all: clean clean-models clean-logs clean-wandb
	@echo "All cleanup completed."

# Development helpers
dev-install:
	@echo "Installing development dependencies..."
	uv sync --extra dev

lint:
	@echo "Running linter..."
	uv run ruff check src/ run/ tests/

format:
	@echo "Formatting code..."
	uv run ruff format src/ run/ tests/

type-check:
	@echo "Running type checker..."
	uv run mypy --ignore-missing-imports src/ipc.py src/sc2env.py

# Quick start for new users
quick-start: install setup-maps check-env
	@echo ""
	@echo "Quick start completed!"
	@echo "Next steps:"
	@echo "1. Configure StarCraft II path in src/config.py"
	@echo "2. Run 'make train' to start training"
	@echo "3. Run 'make test' to run headless unit tests"

# Platform detection and setup
detect-platform:
	@echo "Detected platform: $$(uname)"
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "macOS detected - use 'make setup-macos'"; \
	elif [ "$$(uname)" = "Linux" ]; then \
		echo "Linux detected - use 'make setup-linux'"; \
	else \
		echo "Windows detected - use 'make setup-windows'"; \
	fi

# Show project status
status:
	@echo "StarCraft II PPO Agent Status:"
	@echo "============================="
	@echo "Platform: $$(uname)"
	@echo "Python: $$(uv run python --version 2>/dev/null || echo 'Not available')"
	@echo "Dependencies: $$(if uv run python -c 'import sc2, gymnasium, stable_baselines3, wandb' 2>/dev/null; then echo 'Installed'; else echo 'Missing'; fi)"
	@echo "Maps directory: $$(if [ -d "Maps" ]; then echo 'Exists ($(shell ls Maps/*.SC2Map 2>/dev/null | wc -l) maps)'; else echo 'Missing'; fi)"
	@echo "Models: $$(if [ -d "src/models" ]; then echo '$(shell ls src/models/ 2>/dev/null | wc -l) trained models'; else echo 'No models'; fi)"
	@echo "Logs: $$(if [ -d "src/logs" ]; then echo '$(shell ls src/logs/ 2>/dev/null | wc -l) log directories'; else echo 'No logs'; fi)"
