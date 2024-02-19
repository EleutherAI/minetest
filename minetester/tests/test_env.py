"""Tests for Minetest environment."""
import random
from typing import Any, Dict

import gymnasium as gym
import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env
from gymnasium.vector import AsyncVectorEnv, SyncVectorEnv
from gymnasium.wrappers import TimeLimit

import minetester  # noqa: F401
from minetester import Minetest
from minetester.utils import start_xserver


@pytest.fixture(params=["xvfb", "sdl2"])
def minetest_env(unused_xserver_number, unused_tcp_port_factory, request):
    """Create Minetest environment."""
    env_port, server_port = unused_tcp_port_factory(), unused_tcp_port_factory()
    headless, start_xvfb = (True, True) if request.param == "xvfb" else (True, False)
    mt = Minetest(
        env_port=env_port,
        server_port=server_port,
        base_seed=42,
        headless=headless,
        start_xvfb=start_xvfb,
        x_display=unused_xserver_number,
    )
    yield mt
    mt.close()


def test_first_transition(minetest_env):
    """Test first transition."""
    obs, info = minetest_env.reset()
    assert isinstance(obs, np.ndarray)
    assert isinstance(info, dict)
    action = minetest_env.action_space.sample()
    assert isinstance(action, dict) and all(
        isinstance(key, str) and isinstance(value, (int, np.int64, np.ndarray))
        for key, value in action.items()
    )
    obs, rew, done, truncated, info = minetest_env.step(action)
    assert isinstance(obs, np.ndarray)
    assert isinstance(rew, float)
    assert isinstance(done, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)


def test_loop(minetest_env):
    """Execution test of step-action-loop."""
    max_steps = 10
    minetest_env = TimeLimit(minetest_env, max_episode_steps=max_steps)
    minetest_env.reset()
    done, truncated = False, False
    while not (done or truncated):
        action = minetest_env.action_space.sample()
        _, _, done, truncated, _ = minetest_env.step(action)


@pytest.mark.parametrize("vec_env_cls", [AsyncVectorEnv, SyncVectorEnv])
def test_loop_vec_env(vec_env_cls, unused_xserver_number, unused_tcp_port_factory):
    """Execution test of vectorized step-action-loop."""

    def _make_env(
        rank: int,
        seed: int,
        max_steps: int,
        env_kwargs: Dict[str, Any],
    ):
        def _init():
            # Make sure that each Minetest instance has
            # - different server and client ports
            # - different seeds
            env_port, server_port = unused_tcp_port_factory(), unused_tcp_port_factory()
            env = Minetest(
                env_port=env_port,
                server_port=server_port,
                base_seed=seed + rank,
                **env_kwargs,
            )
            # Assign random timelimit to check that resets work properly
            env = TimeLimit(
                env,
                max_episode_steps=random.randint(max_steps // 2, max_steps),
            )
            return env

        return _init

    # Env settings
    seed = 42
    max_steps = 20
    env_kwargs = {
        "display_size": (600, 400),
        "fov": 72,
        "headless": True,
        "x_display": unused_xserver_number,
    }

    # Create a vectorized environment
    num_envs = 2  # Number of envs to use (<= number of avail. cpus)
    venv = vec_env_cls(
        [
            _make_env(rank=i, seed=seed, max_steps=max_steps, env_kwargs=env_kwargs)
            for i in range(num_envs)
        ],
    )

    # Start loop
    xserver = start_xserver(unused_xserver_number)
    venv.reset()
    step = 0
    while step < max_steps:
        actions = venv.action_space.sample()
        venv.step(actions)
        step += 1
    venv.close()
    xserver.terminate()


def test_gymnasium_api(unused_tcp_port_factory):
    env_port = unused_tcp_port_factory()
    server_port = unused_tcp_port_factory()
    env = gym.make(
        "Minetest-v0",
        env_port=env_port,
        server_port=server_port,
        headless=True,
        start_xvfb=False,
    )
    # Note: render check is skipped because it creates
    # a new environment for each render_mode without incrementing
    # the environment and server ports
    # TODO implement automatic port incrementation and check render
    check_env(env, skip_render_check=True)
