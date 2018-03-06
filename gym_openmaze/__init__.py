from gym.envs.registration import register

register(
	id='openmaze-v0',
	entry_point='gym_openmaze.envs:OpenMaze',
	max_episode_steps=1000
)
