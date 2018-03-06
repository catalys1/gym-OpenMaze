import pygame
import numpy as np

class MazeView(object):

	def __init__(self, maze, screen_size=(225,300)):
		pygame.init()
		pygame.display.set_caption('Maze')
		self.clock = pygame.time.Clock()
		self.game_over = False
		self.maze = maze
		self.maze_size = maze.shape

		self.agent_position = (self.maze_size[0]-2,1)

		self.screen = pygame.display.set_mode(screen_size)
		self.screen_size = np.array(screen_size) - 1
		
		self.maze_layer = pygame.Surface(self.screen_size).convert()
		self.agent_layer = pygame.Surface((self.CELL_W,self.CELL_H)).convert()
		self.agent_layer.set_colorkey((0,0,0))

		wall_color = (50,50,50,255)
		empty_color = (220,220,220,255)
		start_color = (50,240,50,255)
		goal_color = (50,50,240,255)
		self.cell_colors = {
			0: empty_color,
			1: wall_color,
			2: start_color, 
			3: goal_color
		}

		self._draw_maze()
		self.update()

	def _draw_maze(self):
		line_color = (0, 0, 0, 255)

		for y in range(self.maze_size[0]):
			for x in range(self.maze_size[1]):
				# import pdb; pdb.set_trace()
				color = self.cell_colors[self.maze[y][x]]
				pygame.draw.rect(
					self.maze_layer, color, 
					(x*self.CELL_W,y*self.CELL_H,self.CELL_W,self.CELL_H))

		# drawing the horizontal lines
		for y in range(self.maze_size[0]+1):
			pygame.draw.line(self.maze_layer, line_color, (0, y * self.CELL_H),
							(self.SCREEN_W, y * self.CELL_H))

		# drawing the vertical lines
		for x in range(self.maze_size[1]+1):
			pygame.draw.line(self.maze_layer, line_color, (x * self.CELL_W, 0),
							(x * self.CELL_W, self.SCREEN_H))
		self.screen.blit(self.maze_layer, (0,0))

	def _draw_robot(self):
		w, h = self.CELL_W, self.CELL_H
		x, y = int(w/2), int(h/2)
		r = int(min(w, h) / 2 - 2)
		color = (240,20,20,255)
		pygame.draw.circle(self.agent_layer, color, (x, y), r)
		x = self.agent_position[1] * w + 1
		y = self.agent_position[0] * h + 1
		self.screen.blit(self.agent_layer, (x,y))

	def update_agent(self, x, y):
		self.agent_position = (y,x)

	def update(self):
		self.screen.blit(self.maze_layer, (0,0))
		self._draw_robot()
		pygame.display.update()

	def quit(self):
		self.display.quit()
		pygame.quit()

	@property
	def SCREEN_SIZE(self):
		return tuple(self.screen_size)

	@property
	def SCREEN_W(self):
		return int(self.SCREEN_SIZE[0])

	@property
	def SCREEN_H(self):
		return int(self.SCREEN_SIZE[1])

	@property
	def CELL_W(self):
		return float(self.SCREEN_W) / float(self.maze_size[1])

	@property
	def CELL_H(self):
		return float(self.SCREEN_H) / float(self.maze_size[0])


if __name__ == '__main__':
	import curses
	screen = curses.initscr()
	curses.noecho()
	curses.cbreak()
	screen.keypad(True)

	maze = np.zeros((10,7))
	maze[:,(0,-1)] = 1
	maze[(0,-1),:] = 1
	maze[-2,1:-1] = 2
	maze[1,1:-1] = 3
	y_coords = [2,3,4,6,6,7]
	x_coords = [3,1,3,2,3,3]
	maze[y_coords, x_coords] = 1

	maze = MazeView(maze)
	maze.update()
	
	try:
		while True:
			inp = screen.getch()
			y,x = maze.agent_position
			if inp == ord('q'):
				break
			elif inp == curses.KEY_UP:
				y = y-1
			elif inp == curses.KEY_DOWN:
				y = y+1
			elif inp == curses.KEY_RIGHT:
				x = x+1
			elif inp == curses.KEY_LEFT:
				x = x-1
			screen.addstr(0,0,' '*10)
			screen.addstr(0,0, '{}, {}'.format(x,y))
			maze.update_agent(x, y)
			maze.update()
	finally:
		curses.nocbreak()
		screen.keypad(0)
		curses.echo()
		curses.endwin()
