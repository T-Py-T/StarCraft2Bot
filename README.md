# StarCraft2Bot

A modern, modular StarCraft II bot and reinforcement learning (RL) training environment.

## Features
- Modular bot code for StarCraft II using [BurnySC2](https://github.com/BurnySc2/python-sc2)
- RL environment compatible with [OpenAI Gym](https://www.gymlibrary.dev/)
- PPO training and evaluation with [Stable Baselines3](https://stable-baselines3.readthedocs.io/)
- Experiment tracking with [Weights & Biases (wandb)](https://wandb.ai/)
- Fast, reproducible dependency management with [uv](https://github.com/astral-sh/uv)

## Requirements
- Python 3.9–3.12
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- StarCraft II installed (see [BurnySC2 setup guide](https://github.com/BurnySc2/python-sc2#installation))

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

## Usage

- **Train PPO agent:**
  ```sh
  uv venv
  uv pip run python src/trainppo.py
  ```
- **Test a trained model:**
  ```sh
  uv pip run python src/test_model.py
  ```
- **Custom training:**
  ```sh
  uv pip run python src/load-train-mlpp.py
  ```

## Project Structure

```
StarCraft2Bot/
├── src/                # All source code (bot, env, training scripts)
│   ├── incredibot-sct.py
│   ├── sc2env.py
│   ├── trainppo.py
│   ├── load-train-mlpp.py
│   └── test_model.py
├── tests/              # (Optional) Unit tests
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # uv dependency lock file
├── .gitignore
└── README.md
```

## Contributing

Pull requests and issues are welcome! Please:
- Use clear commit messages
- Follow PEP8 style (run `ruff` and `mypy` for linting/type checks)
- Add tests for new features if possible

## License

MIT License. See [LICENSE](LICENSE) for details.