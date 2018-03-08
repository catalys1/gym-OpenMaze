import gym
import gym_openmaze
import random

env = gym.make("openmaze-v0")

rewards = []
observation = env.reset()
while True:
    observation, reward, done, info = env.step(env.action_space.sample())
    print(env.observation_space.available_actions(*observation[0]))

    env.render()

    if done:
        break

print('Total reward: {}'.format(sum(rewards)))