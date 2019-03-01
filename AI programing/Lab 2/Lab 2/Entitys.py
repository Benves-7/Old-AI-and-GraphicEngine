from StateMachine import *
from BaseGameEntity import *
from Manager import *
from State import *
from JsonLoader import *
from random import *

class Worker(MovingEntity):

	# identifier.
	id = 0   # number of worker
	FSM = None
	pos = None # number of the tile worker is on.
	circle = None
	speed = None # speedmodifier

	startTime = 0
	freezeTime = 0
	carrying = {}

	path = []
	pathBack = []

	# internal stats.

	def __init__(self):
		self.SetID()
		self.path = None
		self.pathBack = []
		self.carrying = {}
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Worker())
		self.FSM.SetGlobalState(WorkerGlobalState())
		EntityManager.RegisterEntity(self)
		for node in self.map.grid:
			if node.isSpawn:
				self.pos = node.id
				self.circle = node.center
		self.speed = self.data["worker"]["speed"]
		self.circle = Circle(self.circle,3)
		self.circle.setFill(self.data["worker"]["color"])


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
	path = None
	pathBack = []
	failedPathFindingAttempts = 0

	def __init__(self, worker):
		self.id = worker.id
		self.pos = worker.pos
		EntityManager.RemoveEntity(self)
		EntityManager.RegisterEntity(self)
		self.circle = worker.circle
		self.circle.setFill(self.data["explorer"]["color"])
		self.pathBack = []
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Explorer())
		self.FSM.SetGlobalState(ExplorerGlobalState())
		self.speed = self.data["explorer"]["speed"]

	def Update(self):
	    self.FSM.Update()

	def ExploreNeighbours(self):
		neighbours = self.map.ExploreNeighbours(self.pos)
		for nodeindex in neighbours:
			self.window.window.items[nodeindex].setFill(self.map.grid[nodeindex].color)
			for tree in range(0, self.map.grid[nodeindex].numTrees):
				self.map.grid[nodeindex].trees.append(Tree(tree, nodeindex))
				self.map.grid[nodeindex].trees[-1].circle.draw(self.window.window)
			if self.map.grid[nodeindex].trees:
				ResourceManager.treenodes.append(self.map.grid[nodeindex])
				self.map.grid[nodeindex].dist = ((abs(self.map.grid[nodeindex].x - self.map.grid[self.townHall.pos].x))) + ((abs(self.map.grid[nodeindex].y - self.map.grid[self.townHall.pos].y)))

	def Del(self):
		self.circle.undraw()
		EntityManager.Del(self.id)

class Builder(MovingEntity):

	# identifier.
	id = 0   # number of worker
	FSM = None
	pos = None # number of the tile worker is on.
	circle = None
	speed = None # speedmodifier

	startTime = 0
	freezeTime = 0

	path = []

	def __init__(self, worker):
		self.id = worker.id
		self.pos = worker.pos
		EntityManager.RemoveEntity(self)
		EntityManager.RegisterEntity(self)
		self.circle = worker.circle
		self.circle.setFill(self.data["builder"]["color"])
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Builder())
		self.FSM.SetGlobalState(BuilderGlobalState())
		self.speed = self.data["builder"]["speed"]


class TownHall(StaticEntity):
	pos = 0
	circle = None
	wood = 0

	def __init__(self, pos):
		self.pos = pos
		self.map.grid[pos].isbuildable = False
		self.circle = Circle(self.map.grid[pos].center, 6)
		self.circle.setFill(self.data["townhall"]["color"])
		self.circle.draw(self.window.window)

class ColeMil(StaticEntity):
	pos = 0
	circle = None
	color = None

	def __init__(self, pos):
		self.pos = pos
		self.map.grid[pos].isBuildable = False
		self.circle = Circle(self.map.grid[pos].center, 6)
		self.color = self.data["colemil"]["color"]
		self.circle.draw(self.window.window)

class Tree(StaticEntity):
	id = 0
	circle = None

	def __init__(self, id, nodeindex):
		self.id = id

		moveX = uniform(-self.window.indent_X/3, self.window.indent_X/3)
		moveY = uniform(-self.window.indent_Y/3, self.window.indent_Y/3)

		self.circle = Circle(Point(self.map.grid[nodeindex].center.getX() + moveX, self.map.grid[nodeindex].center.getY() + moveY), 2)
		self.circle.setFill("lightGreen")