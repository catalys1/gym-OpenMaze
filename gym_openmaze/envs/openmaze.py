import numpy as np
import gym
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


class OpenMazeUrgency(gym.Env):
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

	def __init__(self, size=(10,7), random=False, urgency_function=lambda step: 0.001*step, completion_reward=1.0):
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
		self.steps = 0

		self.action_space = spaces.Discrete(len(self.ACTIONS))
		self.observation_space = spaces.Box(
			low=0, high=max(size), shape=size, dtype=np.uint8)
		self.action_space.available_actions = self.available_actions

		self.view = None

		self.COMPLETION_REWARD = completion_reward
		self.step_reward = 0.0
		self.urgency_function = urgency_function

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
			reward = self.step_reward
			done = True
		elif self.maze_cells[new_location[0],new_location[1]] != self.WALL_CELL:
			dist_from_goal = self._distance_from_goal(new_location)
			if dist_from_goal < self.min_dist_from_goal:
				reward = self.step_reward
				self.min_dist_from_goal = dist_from_goal
			self.agent_location = new_location

		self.steps += 1
		self.step_reward = self.urgency_function(self.steps)
				
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
