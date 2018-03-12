import gym
import gym_openmaze
import random

envs = [
	'OpenMazeDiscountCompletion-v0',
]

for e in envs:
	env = gym.make(e)

	rewards = []
	observation = env.reset()
	while True:
		observation, reward, done, info = env.step(
			random.choice(env.action_space.available_actions(*observation)))
		rewards.append(reward)

		env.render()

		if done:
			break

	print('Total reward ({}): {}'.format(e, sum(rewards)))