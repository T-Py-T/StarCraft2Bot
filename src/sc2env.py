# Import config first to set environment variables
from config import WANDB_MODE
import os
os.environ["WANDB_MODE"] = WANDB_MODE

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import subprocess
import pickle
import time
import os
import sys

HEADLESS = True  # Set to True to run SC2 in headless mode (no graphics)
MAX_ATTEMPTS = 200
PKL_PATH = 'state_rwd_action.pkl'

class Sc2Env(gym.Env):
	"""Custom Environment that follows gym interface"""
	def __init__(self):
		super(Sc2Env, self).__init__()
		# Define action and observation space
		# They must be gym.spaces objects
		# Example when using discrete actions:
		self.action_space = spaces.Discrete(6)
		self.observation_space = spaces.Box(low=0, high=255,
											shape=(224, 224, 3), dtype=np.uint8)

	def step(self, action):
		# waits for action.
		for attempt in range(MAX_ATTEMPTS):
			try:
				with open(PKL_PATH, 'rb') as f:
					state_rwd_action = pickle.load(f)
					if state_rwd_action['action'] is not None:
						continue
					else:
						state_rwd_action['action'] = action
						with open(PKL_PATH, 'wb') as f:
							pickle.dump(state_rwd_action, f)
						break
			except Exception as e:
				pass
		else:
			print(f"[Error] step(): Max attempts ({MAX_ATTEMPTS}) reached waiting for action.")
			# Return default/failure state
			map = np.zeros((224, 224, 3), dtype=np.uint8)
			return map, 0, True, False, {}

		# waits for the new state to return (map and reward) (no new action yet. )
		for attempt in range(MAX_ATTEMPTS):
			try:
				if os.path.getsize(PKL_PATH) > 0:
					with open(PKL_PATH, 'rb') as f:
						state_rwd_action = pickle.load(f)
						if state_rwd_action['action'] is None:
							continue
						else:
							state = state_rwd_action['state']
							reward = state_rwd_action['reward']
							done = state_rwd_action['done']
							break
			except Exception as e:
				map = np.zeros((224, 224, 3), dtype=np.uint8)
				observation = map
				# if still failing, input an ACTION, 3 (scout)
				data = {"state": map, "reward": 0, "action": 3, "done": False}
				with open(PKL_PATH, 'wb') as f:
					pickle.dump(data, f)
				state = map
				reward = 0
				done = False
				action = 3
		else:
			print(f"[Error] step(): Max attempts ({MAX_ATTEMPTS}) reached waiting for state.")
			map = np.zeros((224, 224, 3), dtype=np.uint8)
			return map, 0, True, False, {}

		info ={}
		observation = state
		terminated = done
		truncated = False
		return observation, reward, terminated, truncated, info


	def reset(self, seed=None, options=None):
		print("RESETTING ENVIRONMENT!!!!!!!!!!!!!")
		map = np.zeros((224, 224, 3), dtype=np.uint8)
		observation = map
		data = {"state": map, "reward": 0, "action": None, "done": False}  # empty action waiting for the next one!
		with open(PKL_PATH, 'wb') as f:
			pickle.dump(data, f)

		# run incredibot-sct.py non-blocking:
		script_path = os.path.join(os.path.dirname(__file__), 'incredibot-sct.py')
		if HEADLESS:
			subprocess.Popen([sys.executable, script_path], env={**os.environ, "SC2_HEADLESS": "1"})
		else:
			subprocess.Popen([sys.executable, script_path])
		return observation, {}  # Gymnasium expects (observation, info)
