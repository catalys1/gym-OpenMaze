import gym
import gym_openmaze
import random

env = gym.make("openmaze-v0")

rewards = []
observation = env.reset()
while True:
    observation, reward, done, info = env.step(random.choice(observation[1]))
    print(reward)
    rewards.append(reward)

    env.render()

    if done:
        break

print('Total reward: {}'.format(sum(rewards)))