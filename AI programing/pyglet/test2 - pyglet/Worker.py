from StateMachine import *
from BaseGameEntity import *
from State import *
from JsonLoader import *

class Worker(MovingEntity):

	# identifier.
	id = None
	FSM = None
	pos = None
	circle = None
	speed = None
	Path = []

	# internal stats.

	def __init__(self):
		self.id = BaseGameEntityClass.SetID(self)
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Worker())
		self.FSM.SetGlobalState(WorkerGlobalState())
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

	def __init__(self, worker):
		self.id = worker.id
		self.pos = worker.pos
		self.circle = worker.circle
		self.circle.setFill(JsonLoader.Data["explorer"]["color"])
		center = self.circle.getCenter()
		self.searchRectangel = Rectangle(Point(center.getX() - 100, center.getY() + 100),Point(center.getX() + 100, center.getY() - 100))
		#self.searchRectangel.draw(self.window.window)
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Explorer())
		self.FSM.SetGlobalState(ExplorerGlobalState())
		self.speed = JsonLoader.Data["explorer"]["speed"]

	def Update(self):
	    self.FSM.Update()

	def ExploreNeighbours(self):
		neighbours = self.map.ExploreNeighbours(self.pos)
		for node in neighbours:
			self.window.window.items[node].setFill(self.map.grid[node].color)