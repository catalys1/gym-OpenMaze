import gym
import gym_openmaze

env = gym.make("openmaze-v0")

env.reset()
while True:
    observation, reward, done, info = env.step(env.action_space.sample())

    env.render()

    if done:
        break
