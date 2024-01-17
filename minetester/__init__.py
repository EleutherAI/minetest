"""Minetester: expose Minetest as environment via the Gymnasium interface."""

import gymnasium as gym

from minetester.minetest_env import Minetest  # noqa: F401

gym.register(
    id="Minetest-v0",
    entry_point=Minetest,
    nondeterministic=True,  # TODO: check this and try to make it deterministic
    order_enforce=True,
    kwargs={
        "base_seed": 42,
        "render_mode": "rgb_array",
        "headless": True,
        "start_xvfb": True,
    },
)
