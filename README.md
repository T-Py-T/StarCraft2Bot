# StarCraft II PPO Agent

A reinforcement-learning environment and Protoss strategy agent for StarCraft
II. The project couples a Gymnasium environment to a BurnySC2 bot through a
small, process-safe IPC contract, then trains a PPO policy with Stable
Baselines3.

The strongest public evidence today is the environment boundary and its
headless regression suite. Live training quality, convergence, and competitive
gameplay still require a licensed StarCraft II installation and are not claimed
as verified by this repository.

## At a glance

| Area | Public evidence | What it demonstrates |
| --- | --- | --- |
| RL environment | [`src/sc2env.py`](src/sc2env.py) | Fixed-shape observations, discrete actions, rewards, and episode lifecycle |
| Runtime protocol | [`src/ipc.py`](src/ipc.py) | Atomic request/response publication, correlation IDs, stale-message rejection, and isolated run directories |
| Game agent | [`src/incredibot-sct.py`](src/incredibot-sct.py) | Protoss economy, production, scouting, attack, and retreat actions through BurnySC2 |
| PPO pipeline | [`src/trainppo.py`](src/trainppo.py) | Stable Baselines3 training entry point and optional Weights & Biases tracking |
| Headless validation | [`tests/`](tests), [PR workflow](.github/workflows/test.yml) | Protocol and environment behavior without launching StarCraft II |
| Cross-platform tooling | [`run/`](run), [`scripts/`](scripts) | Windows, Linux/WSL, and macOS/VM setup paths |

## Architecture

```text
PPO learner / Gymnasium
        │ action request
        ▼
atomic request archive + episode/request ID
        │
        ▼
BurnySC2 Protoss bot ──► StarCraft II
        │
        └──────── observation + reward + terminal response
                         │
                         ▼
              atomic response archive
```

The IPC layer uses separate single-writer request and response files. Unique
temporary files make publication atomic; archive loading rejects object
payloads; correlation identifiers prevent a learner from accepting stale state
from a previous step or episode. `SC2_RUNTIME_DIR` isolates concurrent runs.

## Action and observation contract

- **Observation:** `224 × 224 × 3` visual state.
- **Actions:** expand/mine, build Stargate, build Void Ray, scout, attack, or
  retreat.
- **Policy:** PPO with Stable Baselines3.
- **Strategy scope:** Protoss progression toward Void Ray production.
- **Tracking:** optional Weights & Biases and TensorBoard instrumentation.

The reward implementation is inspectable in the environment, but this public
repository does not retain a model card, training dataset, seed matrix, raw
training curves, evaluation replays, or a reproducible win-rate artifact.

## Headless validation

The local gate exercises the software boundary that can be tested without the
commercial game runtime:

```bash
uv sync --locked --extra dev
make test
make lint
make type-check
```

The tests cover atomic publication, request and episode correlation, fixed
observation shape, stale-message handling, terminal precedence, and the initial
ready handshake. The GitHub Actions workflow runs only for pull requests, after
agents have run the same checks locally.

## Live setup

Prerequisites:

- Python 3.9–3.12 on the current default branch;
- a licensed StarCraft II installation;
- compatible maps; and
- [`uv`](https://docs.astral.sh/uv/) for the locked environment.

```bash
git clone https://github.com/T-Py-T/starcraft2-ppo-agent.git
cd starcraft2-ppo-agent
uv sync --locked --extra dev

make setup-maps
make train
```

Platform-specific setup lives under [`run/`](run). Live validation is
deliberately separate from `make test` because it depends on the installed game,
maps, display/runtime configuration, and local model artifacts.

## Repository map

```text
src/
├── sc2env.py             # Gymnasium environment
├── ipc.py                # process-safe state exchange
├── incredibot-sct.py     # Protoss game agent
├── trainppo.py           # PPO training entry point
├── test_model.py         # live model evaluation
└── config.py             # runtime paths and settings
tests/                    # headless protocol/environment regressions
run/                      # platform-specific game setup
scripts/                  # remote-development helpers
```

## Evidence boundary and next proof

This repository currently proves the tested software contract around training;
it does not prove that a trained policy converges or wins. The next portfolio-
grade evidence should be one versioned evaluation bundle containing the exact
code and environment revisions, seeds, opponent difficulty, maps, episode
budget, raw metrics, model checksum, and representative replays.

The repository does not currently include a repository-wide license file. Do
not infer an MIT grant from earlier README text; upstream packages and game
assets remain subject to their own terms.
