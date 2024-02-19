"""Test loop for Minetest environment."""

if __name__ == "__main__":
    from gymnasium.wrappers import TimeLimit

    from minetester import Minetest

    render = True
    max_steps = 100

    env = Minetest(
        base_seed=42,
        start_minetest=True,
        headless=True,
        start_xvfb=True,
    )
    env = TimeLimit(env, max_episode_steps=max_steps)

    env.reset()
    done = False
    step = 0
    while True:
        try:
            action = env.action_space.sample()
            _, rew, done, truncated, info = env.step(action)
            print(step, rew, done or truncated, info)
            if render:
                env.render()
            if done or truncated:
                env.reset()
            step += 1
        except KeyboardInterrupt:
            break
    env.close()
