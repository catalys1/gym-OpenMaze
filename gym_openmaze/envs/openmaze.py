import collections

import gym
import numpy as np
from gym import spaces

from gym_openmaze.envs.maze_view import MazeView


class OpenMazeNoBacktrack(gym.Env):
	'''OpenMaze(size=(10,7), random=False)
	An open maze environment. There are start and goal cells, with obstacles
	between them.

	Parameters
	----------
	size : array_like
		A tuple of (num_rows, num_cols). Default: (10,7)
	random : bool
		If true, generates a random maze of size `size`. If False, generates
		the default 10x7 maze. Default: False.
	'''

	metadata = {
		'render.modes': ['human', 'print']
	}

	EMPTY_CELL = 0
	WALL_CELL = 1
	START_CELL = 2
	GOAL_CELL = 3

	ACTIONS = ['N', 'E', 'S', 'W']
	ACTION_ENUM = {i:a for i,a in enumerate(ACTIONS)}
	ACTION_MOVEMENT = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

	def __init__(self, size=(10,7), random=False):
		self.maze_size = np.array(size)
		self.maze_cells = np.zeros(size)

		if random:
			self._construct_random_maze()
		else:
			self._construct_default_maze()

		self.agent_start_location = np.array((self.maze_size[0]-2, 1))
		self.agent_location = self.agent_start_location
		self.goal_locations = np.argwhere(self.maze_cells==self.GOAL_CELL)
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)
		self.last_dist_from_goal = self.min_dist_from_goal

		self.action_space = spaces.Discrete(len(self.ACTIONS))
		self.observation_space = spaces.Box(
			low=0, high=max(size), shape=size, dtype=np.uint8)
		self.action_space.available_actions = self.available_actions

		self.view = None

		self.COMPLETION_REWARD = 1.0
		self.STEP_REWARD = (
			self.COMPLETION_REWARD /
			self._distance_from_goal(self.agent_location)
		)

	def _construct_random_maze(self):
		pass

	def _construct_default_maze(self):

		self._fill_edges()
		self.maze_cells[-2,1:-1] = self.START_CELL
		self.maze_cells[1,1:-1] = self.GOAL_CELL

		y_coords = [2,3,4,6,6,7]
		x_coords = [3,1,3,2,3,3]
		self.maze_cells[y_coords, x_coords] = self.WALL_CELL


	def _fill_edges(self):

		self.maze_cells[(0,-1),:] = 1
		self.maze_cells[:,(0,-1)] = 1

	def _distance_from_goal(self, location):
		return np.abs(self.goal_locations-location).sum(axis=1).min()

	def available_actions(self, y, x):
		movements = ((0, (y-1, x)), (1, (y, x+1)), (2, (y-1, x)), (3, (y, x-1)))
		valid = np.zeros(self.action_space.n)
		for i, move in movements:
			if (np.greater(move, 0).all() and np.less(move, self.maze_size).all()
				and self.maze_cells[move] != self.WALL_CELL):
				valid[i] = 1
		# valid = [
		# 	action for action, move in movements
		# 	if np.greater(move, 0).all() and np.less(move, self.maze_size).all()
		# 	and self.maze_cells[move] != self.WALL_CELL
		# ]
		return valid

	def step(self, action):

		reward = 0
		done = False
		info = {}

		try:
			action = int(action)
			action = self.ACTION_ENUM[action]
		except:
			pass
		delta = self.ACTION_MOVEMENT[action]

		new_location = self.agent_location + delta
		if (min(new_location) < 0
				or new_location[0] >= self.maze_size[0]
				or new_location[1] >= self.maze_size[1]):
			pass
		elif self.maze_cells[new_location[0],new_location[1]] == self.GOAL_CELL:
			reward = self.STEP_REWARD
			done = True
		elif self.maze_cells[new_location[0],new_location[1]] != self.WALL_CELL:
			dist_from_goal = self._distance_from_goal(new_location)
			if dist_from_goal < self.min_dist_from_goal:
				reward = self.STEP_REWARD
				self.min_dist_from_goal = dist_from_goal
			elif dist_from_goal > self.last_dist_from_goal:
				reward = -self.STEP_REWARD * 0.1
			self.last_dist_from_goal = dist_from_goal
			self.agent_location = new_location

		return (
			self.agent_location,
			reward,
			done,
			info
		)

	def reset(self):
		self.agent_location = self.agent_start_location
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)
		return self.agent_location

	def render(self, mode='human'):
		if mode == 'human':
			if self.view is None:
				self.view = MazeView(maze=self.maze_cells)
			self.view.update_agent(*self.agent_location[::-1])
			self.view.update()
		else:
			print(self.agent_location)


class OpenMazeInchworm(gym.Env):
	'''OpenMaze(size=(10,7), random=False)
	An open maze environment. There are start and goal cells, with obstacles
	between them.

	Parameters
	----------
	size : array_like
		A tuple of (num_rows, num_cols). Default: (10,7)
	random : bool
		If true, generates a random maze of size `size`. If False, generates
		the default 10x7 maze. Default: False.
	'''

	metadata = {
		'render.modes': ['human', 'print']
	}

	EMPTY_CELL = 0
	WALL_CELL = 1
	START_CELL = 2
	GOAL_CELL = 3

	ACTIONS = ['N', 'E', 'S', 'W']
	ACTION_ENUM = {i:a for i,a in enumerate(ACTIONS)}
	ACTION_MOVEMENT = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

	def __init__(self, size=(10,7), random=False):
		self.maze_size = np.array(size)
		self.maze_cells = np.zeros(size)

		if random:
			self._construct_random_maze()
		else:
			self._construct_default_maze()

		self.agent_start_location = np.array((self.maze_size[0]-2, 1))
		self.agent_location = self.agent_start_location
		self.goal_locations = np.argwhere(self.maze_cells==self.GOAL_CELL)
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)

		self.action_space = spaces.Discrete(len(self.ACTIONS))
		self.observation_space = spaces.Box(
			low=0, high=max(size), shape=size, dtype=np.uint8)
		self.action_space.available_actions = self.available_actions

		self.view = None

		self.COMPLETION_REWARD = 1.0
		self.STEP_REWARD = (
			self.COMPLETION_REWARD /
			self._distance_from_goal(self.agent_location)
		)

	def _construct_random_maze(self):
		pass

	def _construct_default_maze(self):

		self._fill_edges()
		self.maze_cells[-2,1:-1] = self.START_CELL
		self.maze_cells[1,1:-1] = self.GOAL_CELL

		y_coords = [2,3,4,6,6,7]
		x_coords = [3,1,3,2,3,3]
		self.maze_cells[y_coords, x_coords] = self.WALL_CELL


	def _fill_edges(self):

		self.maze_cells[(0,-1),:] = 1
		self.maze_cells[:,(0,-1)] = 1

	def _distance_from_goal(self, location):
		return np.abs(self.goal_locations-location).sum(axis=1).min()

	def available_actions(self, y, x):
		movements = ((0, (y-1, x)), (1, (y, x+1)), (2, (y-1, x)), (3, (y, x-1)))
		valid = np.zeros(self.action_space.n)
		for i, move in movements:
			if (np.greater(move, 0).all() and np.less(move, self.maze_size).all()
				and self.maze_cells[move] != self.WALL_CELL):
				valid[i] = 1
		# valid = [
		# 	action for action, move in movements
		# 	if np.greater(move, 0).all() and np.less(move, self.maze_size).all()
		# 	and self.maze_cells[move] != self.WALL_CELL
		# ]
		return valid

	def step(self, action):

		reward = 0
		done = False
		info = {}

		try:
			action = int(action)
			action = self.ACTION_ENUM[action]
		except:
			pass
		delta = self.ACTION_MOVEMENT[action]

		new_location = self.agent_location + delta
		if (min(new_location) < 0
				or new_location[0] >= self.maze_size[0]
				or new_location[1] >= self.maze_size[1]):
			pass
		elif self.maze_cells[new_location[0],new_location[1]] == self.GOAL_CELL:
			reward = self.STEP_REWARD
			done = True
		elif self.maze_cells[new_location[0],new_location[1]] != self.WALL_CELL:
			dist_from_goal = self._distance_from_goal(new_location)
			if dist_from_goal < self.min_dist_from_goal:
				reward = self.STEP_REWARD
				self.min_dist_from_goal = dist_from_goal
			self.agent_location = new_location

		return (
			self.agent_location,
			reward,
			done,
			info
		)

	def reset(self):
		self.agent_location = self.agent_start_location
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)
		return self.agent_location

	def render(self, mode='human'):
		if mode == 'human':
			if self.view is None:
				self.view = MazeView(maze=self.maze_cells)
			self.view.update_agent(*self.agent_location[::-1])
			self.view.update()
		else:
			print(self.agent_location)


class OpenMaze(gym.Env):
	'''OpenMaze(size=(10,7), random=False)
	An open maze environment. There are start and goal cells, with obstacles
	between them.

	Parameters
	----------
	size : array_like
		A tuple of (num_rows, num_cols). Default: (10,7)
	random : bool
		If true, generates a random maze of size `size`. If False, generates
		the default 10x7 maze. Default: False.
	'''

	metadata = {
		'render.modes': ['human', 'print']
	}

	EMPTY_CELL = 0
	WALL_CELL = 1
	START_CELL = 2
	GOAL_CELL = 3

	ACTIONS = ['N', 'E', 'S', 'W']
	ACTION_ENUM = {i:a for i,a in enumerate(ACTIONS)}
	ACTION_MOVEMENT = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

	def __init__(self,
				 size=(10,7),
				 random=False,
				 unvisted_state_reward=0.,
				 visted_state_reward=0.,
				 completion_bonus_reward=1.,
				 cycle_window=2,
				 allowed_cycle_count=np.inf):
		self.maze_size = np.array(size)
		self.maze_cells = np.zeros(size)

		if random:
			self._construct_random_maze()
		else:
			self._construct_default_maze()

		self.agent_start_location = np.array((self.maze_size[0]-2, 1))
		self.goal_locations = np.argwhere(self.maze_cells==self.GOAL_CELL)

		self.action_space = spaces.Discrete(len(self.ACTIONS))
		self.observation_space = spaces.Box(
			low=0, high=max(size), shape=size, dtype=np.uint8)
		self.action_space.available_actions = self.available_actions

		self.view = None

		self.visted_state_reward = visted_state_reward
		self.unvisted_state_reward = unvisted_state_reward
		self.completion_bonus_reward = completion_bonus_reward

		self.allowed_cycle_count = allowed_cycle_count
		self.cycle_window = cycle_window

		low = min(self.visted_state_reward, self.unvisted_state_reward)
		high = max(self.visted_state_reward, self.unvisted_state_reward)
		self.reward_range = (low, self.completion_bonus_reward + high)
		self.reset()

	def _construct_random_maze(self):
		pass

	def _construct_default_maze(self):

		self._fill_edges()
		self.maze_cells[-2,1:-1] = self.START_CELL
		self.maze_cells[1,1:-1] = self.GOAL_CELL

		y_coords = [2,3,4,6,6,7]
		x_coords = [3,1,3,2,3,3]
		self.maze_cells[y_coords, x_coords] = self.WALL_CELL


	def _fill_edges(self):

		self.maze_cells[(0,-1),:] = self.WALL_CELL
		self.maze_cells[:,(0,-1)] = self.WALL_CELL

	def _distance_from_goal(self, location):
		return np.abs(self.goal_locations-location).sum(axis=1).min()

	def available_actions(self, y, x):
		valid = np.zeros(self.action_space.n)
		movements = ((y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1))
		if self.maze_cells[(y, x)] != self.WALL_CELL:
			for i, move in enumerate(movements):
				if (np.greater(move, 0).all()
					and np.less(move, self.maze_size).all()
					and self.maze_cells[move] != self.WALL_CELL):
					valid[i] = 1
		return valid

	def step(self, action):
		reward = 0
		done = False
		info = {}

		try:
			action = int(action)
			action = self.ACTION_ENUM[action]
		except:
			pass

		_new_location = self.agent_location + self.ACTION_MOVEMENT[action]
		new_location = tuple(_new_location)

		if (min(new_location) < 0
			or new_location[0] >= self.maze_size[0]
			or new_location[1] >= self.maze_size[1]):
			return tuple(self.agent_location), reward, done, info

		if self.maze_cells[new_location] == self.GOAL_CELL:
			reward = self.completion_bonus_reward
			done = True
		elif self.maze_cells[new_location] == self.WALL_CELL:
			return tuple(self.agent_location), reward, done, info

		self.steps += 1

		if new_location in self.all_visited_states:
			reward += self.visted_state_reward
		else:
			reward += self.unvisted_state_reward

		# naive cycle detection
		if new_location in self.previous_states:
			self.cycle_count += 1
		if self.cycle_count > self.allowed_cycle_count:
			done = True
		self.previous_states.append(new_location)
		self.all_visited_states.add(new_location)

		self.agent_location = _new_location
		return new_location, reward, done, info

	def reset(self):
		self.steps = 0
		self.cycle_count = 0
		self.all_visited_states = set()
		self.previous_states = collections.deque(maxlen=self.cycle_window)
		self.agent_location = self.agent_start_location
		# self.min_dist_from_goal = self._distance_from_goal(self.agent_location)
		return tuple(self.agent_location)

	def render(self, mode='human'):
		if mode is None:
			return tuple(self.agent_location)
		elif mode == 'human':
			if self.view is None:
				self.view = MazeView(maze=self.maze_cells)
			self.view.update_agent(*self.agent_location[::-1])
			self.view.update()
		elif callable(mode):
			mode(tuple(self.agent_location))
		else:
			print(tuple(self.agent_location))
