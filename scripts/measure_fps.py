#!/usr/bin/env python3
import time

import matplotlib.pyplot as plt
import numpy as np
from minetester.minetest_env import Minetest

headless = False
do_prints = False
render = False
sync = False
sync_args = dict(
    sync_port = 30010
    sync_dtime = 0.05
)

env = Minetest(
    base_seed=42,
    start_minetest=False,
    headless=headless,
    start_xvfb=False,
    **(sync_args if sync else {})
)

_ = env.reset()
tot_time = 0
time_list = []
fps_list = []
step = 0
while True:
    start = time.time()
    try:
        action = env.action_space.sample()
        _ = env.step(action)
        if render:
            env.render()
        if do_prints:
            print(f"Step {step}")

        dtime = time.time() - start
        tot_time += dtime
        fps = 1/dtime
        time_list.append(tot_time)
        fps_list.append(fps)
        step += 1
    except KeyboardInterrupt:
        break
env.close()

# Print stats
fps_np = np.array(fps_list)
print(f"Runtime = {tot_time:.2f}s")
print(f"Avg. FPS = {fps_np.mean():.2f}, Min. FPS = {fps_np.min():.2f}, Max. FPS = {fps_np.max():.2f}")

# Plot FPS over time
plt.figure()
plt.plot(time_list, fps_list, label="data")
# Calculate moving average
window = int(len(fps_list) * 0.1) + 1
mav = np.convolve(fps_np, np.ones(window) / window, mode="same")
plt.plot(time_list, mav, label="moving avg.")
plt.xlabel("time [s]")
plt.ylabel("FPS")
plt.legend()
if sync:
    plt.savefig(f"fps_testloop_sync_{'headless_' if headless else ''}.png")
else:
    plt.savefig(f"fps_testloop_async_{'headless' if headless else ''}.png")
plt.show()
