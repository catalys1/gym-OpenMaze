import numpy as np
import gym

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

	EMPTY_CELL = 0
	WALL_CELL = 1
	START_CELL = 2
	GOAL_CELL = 3

	ACTIONS = ['N', 'E', 'S', 'W']
	ACTION_ENUM = {i:a for i,a in enumerate(ACTIONS)}
	ACTION_MOVEMENT = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

	STEP_REWARD = 1.0
	COMPLETION_REWARD = 5.0

	def __init__(self, size=(10,7), random=False):
		self.maze_size = size
		self.maze_cells = np.zeros(size)	

		if random:
			self._construct_random_maze()
		else:
			self._construct_default_maze()

		self.agent_start_location = np.array((self.size[0]-2, 1))
		self.agent_location = self.agent_start_location
		self.goal_locations = np.argwhere(self.maze_cells==self.GOAL_CELL)
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)

	def _construct_random_maze(self):
		pass

	def _construct_default_maze(self):

		self._fill_edges()
		self.maze_cells[-2,1:-1] = START_CELL
		self.maze_cells[1,1:-1] = END_CELL

		y_coords = [2,3,4,6,6,7]
		x_coords = [3,1,3,2,3,3]
		self.maze_cells[y_coords, x_coords] = WALL_CELL


	def _fill_edges(self):

		self.maze_cells[(0,1),:] = 1
		self.maze_cells[:,(0,1)] = 1

	def _distance_from_goal(self, location):
		return np.abs(self.goal_locations-location).sum(axis=1).min()

	def step(self, action):

		reward = 0
		done = False
		info = {}

		if isinstance(action, int):
			action = self.ACTION_ENUM(action)
		delta = self.ACTION_MOVEMENT[action]

		new_location = self.agent_location + delta
		if self.maze_cells[*new_location] == self.GOAL_CELL:
			reward = self.COMPLETION_REWARD
			done = True
		elif self.maze_cells[*new_location] != self.WALL_CELL:
			dist_from_goal = self._distance_from_goal(new_location)
			if dist_from_goal < self.min_dist_from_goal:
				reward = self.STEP_REWARD
				self.min_dist_from_goal = dist_from_goal
			self.agent_location = new_location

		return self.agent_location, reward, done, info

	def reset(self):
		self.agent_location = self.agent_start_location
		self.min_dist_from_goal = self._distance_from_goal(self.agent_location)

	def render(self, mode='human', close=False):
		pass