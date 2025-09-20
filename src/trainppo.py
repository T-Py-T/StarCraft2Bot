# Import config first to set environment variables
from config import WANDB_MODE
import os
os.environ["WANDB_MODE"] = WANDB_MODE

from stable_baselines3 import PPO
from sc2env import Sc2Env
import time
from wandb.integration.sb3 import WandbCallback
import wandb


model_name = f"{int(time.time())}"

models_dir = f"models/{model_name}/"
logdir = f"logs/{model_name}/"


conf_dict = {"Model": "v19",
             "Machine": "Main",
             "policy":"MlpPolicy",
             "model_save_name": model_name}


run = wandb.init(
    project=f'SC2RLv6',
    entity="tnt850910",
    config=conf_dict,
    sync_tensorboard=True,  # auto-upload sb3's tensorboard metrics
    save_code=True,  # optional
)


if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)

env = Sc2Env()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
max_games = 10  # Limit the number of games/episodes for testing
iters = 0
while iters < max_games:
    print(f"On iteration: {iters+1} of {max_games}")
    iters += 1
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
    model.save(f"{models_dir}/{TIMESTEPS*iters}")
print(f"Training complete. Ran {max_games} games.")
