import itertools

from gym.envs.registration import register

register(
	id='OpenMazeNoBacktrack-v0',
	entry_point='gym_openmaze.envs:OpenMazeNoBacktrack',
	max_episode_steps=1000
)

register(
	id='OpenMazeInchworm-v0',
	entry_point='gym_openmaze.envs:OpenMazeInchworm',
	max_episode_steps=1000
)

register(
	id='OpenMazeUrgency-v0',
	entry_point='gym_openmaze.envs:OpenMaze',
	max_episode_steps=1000
)

register(
	id='OpenMazeOnlyCompletionReward-v0',
	entry_point='gym_openmaze.envs:OpenMaze',
	kwargs={
		'unvisted_state_reward': 0.0,
		'visted_state_reward': 0.0,
		'completion_bonus_reward': 1.,
	},
	max_episode_steps=1000
)

register(
	id='OpenMazeDiscountCompletion-v0',
	entry_point='gym_openmaze.envs:OpenMaze',
	kwargs={
		'unvisted_state_reward': 0.0,
		'visted_state_reward': 0.0,
		'completion_bonus_reward': 1.,
		'use_discounting': True,
	},
	max_episode_steps=1000
)


max_episode_steps = 2000
cycles = itertools.chain(
	range(1, 20), range(20, 100, 10), range(100, max_episode_steps + 1, 100)
)
windows = itertools.chain(range(2, 10), range(10, 20, 2))
for max_cycles, window_size in itertools.product(cycles, windows):
	cycle_id = 'Max{}CyclesInWindowSize{}'.format(max_cycles, window_size)

	register(
		id='OpenMazeUrgency{}-v0'.format(cycle_id),
		entry_point='gym_openmaze.envs:OpenMaze',
		kwargs={
			'unvisted_state_reward': 0.1,
			'visted_state_reward': 0.0,
			'completion_bonus_reward': 1.,
			'allowed_cycle_count': max_cycles,
			'cycle_window': window_size,
		},
		max_episode_steps=max_episode_steps,
	)

	register(
		id='OpenMazeOnlyCompletionReward{}-v0'.format(cycle_id),
		entry_point='gym_openmaze.envs:OpenMaze',
		kwargs={
			'unvisted_state_reward': 0.0,
			'visted_state_reward': 0.0,
			'completion_bonus_reward': 1.,
			'allowed_cycle_count': max_cycles,
			'cycle_window': window_size,
		},
		max_episode_steps=max_episode_steps,
	)

	register(
		id='OpenMazeDiscountCompletion{}-v0'.format(cycle_id),
		entry_point='gym_openmaze.envs:OpenMaze',
		kwargs={
			'unvisted_state_reward': 0.0,
			'visted_state_reward': 0.0,
			'completion_bonus_reward': 1.,
			'allowed_cycle_count': max_cycles,
			'cycle_window': window_size,
			'use_discounting': True,
		},
		max_episode_steps=max_episode_steps,
	)
