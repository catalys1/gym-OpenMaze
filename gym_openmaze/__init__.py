from gym.envs.registration import register

register(
	id='openmaze-v0',
	entry_point='gym_OpenMaze.envs:OpenMaze'
)
