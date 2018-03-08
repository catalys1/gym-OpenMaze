import gym
import gym_openmaze
import random

env = gym.make("openmaze-v0")

rewards = []
observation = env.reset()
while True:
    observation, reward, done, info = env.step(
    	random.choice(env.action_space.available_actions(*observation)))

    env.render()

    if done:
        break

print('Total reward: {}'.format(sum(rewards)))