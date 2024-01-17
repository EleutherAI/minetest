"""Gymnasium API checker for Minetest environment."""
import gymnasium as gym
from gymnasium.utils.env_checker import check_env

import minetester  # noqa: F401

env = gym.make("Minetest-v0")

# Note: render check is skipped because it creates
# a new environment for each render_mode without incrementing
# the environment and server ports
# TODO implement automatic port incrementation and check render
check_env(env.unwrapped, skip_render_check=True)
