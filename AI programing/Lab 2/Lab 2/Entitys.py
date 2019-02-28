from StateMachine import *
from BaseGameEntity import *
from State import *
from JsonLoader import *
from random import *

class Worker(MovingEntity):

	# identifier.
	id = 0
	FSM = None
	pos = None
	circle = None
	speed = None
	path = []
	pathBack = []

	# internal stats.

	def __init__(self):
		self.SetID()
		self.path = []
		self.pathBack = []
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Worker())
		self.FSM.SetGlobalState(WorkerGlobalState())
		EntityManager.RegisterEntity(self)
		for node in self.map.grid:
			if node.isSpawn:
				self.pos = node.id
				self.circle = node.center
		self.speed = JsonLoader.Data["worker"]["speed"]
		self.circle = Circle(self.circle,3)
		self.circle.setFill(JsonLoader.Data["worker"]["color"])


	def Update(self):
		self.FSM.Update()

	def GetFSM(self):
		return self.FSM

class Explorer(MovingEntity):
    
	id = None
	FSM = None
	circle = None
	pos = None
	searchRectangel = None
	speed = None
	path = []
	pathBack = []
	failedPathFindingAttempts = 0

	def __init__(self, worker):
		self.id = worker.id
		self.pos = worker.pos
		EntityManager.RemoveEntity(self)
		EntityManager.RegisterEntity(self)
		self.circle = worker.circle
		self.circle.setFill(JsonLoader.Data["explorer"]["color"])
		center = self.circle.getCenter()
		self.pathBack = []
		self.searchRectangel = Rectangle(Point(center.getX() - 150, center.getY() + 150),Point(center.getX() + 150, center.getY() - 150))
		#self.searchRectangel.draw(self.window.window)
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Explorer())
		self.FSM.SetGlobalState(ExplorerGlobalState())
		self.speed = JsonLoader.Data["explorer"]["speed"]

	def Update(self):
	    self.FSM.Update()

	def ExploreNeighbours(self):
		neighbours = self.map.ExploreNeighbours(self.pos)
		for nodeindex in neighbours:
			self.window.window.items[nodeindex].setFill(self.map.grid[nodeindex].color)
			for tree in range(0, self.map.grid[nodeindex].numTrees):
				self.map.grid[nodeindex].trees.append(Tree(tree, nodeindex))
				self.map.grid[nodeindex].trees[-1].circle.draw(self.window.window)

	def Del(self):
		self.circle.undraw()
		EntityManager.Del(self.id)

class TownHall(StaticEntity):
	pos = 0
	circle = None

	def __init__(self, pos):
		self.pos = pos
		self.circle = Circle(self.map.grid[pos].center, 6)
		self.circle.setFill("Dark Blue")
		self.circle.draw(self.window.window)

class Tree(StaticEntity):
	id = 0
	circle = None

	def __init__(self, id, nodeindex):
		self.id = id

		moveX = uniform(-self.window.indent_X/2, self.window.indent_X/2)
		moveY = uniform(-self.window.indent_Y/2, self.window.indent_Y/2)

		self.circle = Circle(Point(self.map.grid[nodeindex].center.getX() + moveX, self.map.grid[nodeindex].center.getY() + moveY), 2)
		self.circle.setFill("lightGreen")