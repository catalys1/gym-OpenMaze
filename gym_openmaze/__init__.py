from gym.envs.registration import register

register(
	id='openmazenobacktrack-v0',
	entry_point='gym_openmaze.envs:OpenMazeNoBacktrack',
	max_episode_steps=1000
)

register(
	id='openmazeurgency-v0',
	entry_point='gym_openmaze.envs:OpenMazeUrgency',
	max_episode_steps=1000
)

register(
	id='openmazeinchworm-v0',
	entry_point='gym_openmaze.envs:OpenMazeInchworm',
	max_episode_steps=1000
)