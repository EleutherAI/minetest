from minetester import Minetest

mt = Minetest(
    env_port=5555,
    seed=0, 
    start_minetest=False
)
mt.reset()

while True:
    action = mt.action_space.sample()
    mt.step(action)
    mt.render()