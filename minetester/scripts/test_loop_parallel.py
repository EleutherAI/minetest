"""Test loop with parallel Minetest environments."""

if __name__ == "__main__":
    import random
    from typing import Any, Dict, Optional

    from gymnasium.vector import AsyncVectorEnv
    from gymnasium.wrappers import TimeLimit

    from minetester import Minetest
    from minetester.utils import start_xserver

    def _make_env(
        rank: int,
        seed: int = 0,
        max_steps: int = 1e9,
        env_kwargs: Optional[Dict[str, Any]] = None,
    ):
        env_kwargs = env_kwargs or {}

        def _init():
            # Make sure that each Minetest instance has
            # - different server and client ports
            # - different and deterministic seeds
            env = Minetest(
                env_port=5555 + rank,
                server_port=30000 + rank,
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
    max_steps = 100
    x_display = 4
    env_kwargs = {
        "display_size": (600, 400),
        "fov": 72,
        "headless": True,
        "x_display": x_display,
    }

    # Create a vectorized environment
    num_envs = 2  # Number of envs to use (<= number of avail. cpus)
    vec_env_cls = AsyncVectorEnv
    venv = vec_env_cls(
        [
            _make_env(rank=i, seed=seed, max_steps=max_steps, env_kwargs=env_kwargs)
            for i in range(num_envs)
        ],
    )

    # Start X server
    xserver = start_xserver(x_display)

    # Start loop
    render = True
    obs, _ = venv.reset()
    done = [False] * num_envs
    step = 0
    while step < max_steps:
        print(f"Elapsed steps: {venv.get_attr('_elapsed_steps')}")
        actions = venv.action_space.sample()
        obs, rew, done, _, info = venv.step(actions)
        if render:
            venv.call("render")
        step += 1
    venv.close()
    xserver.terminate()
