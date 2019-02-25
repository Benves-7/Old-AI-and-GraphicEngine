from StateMachine import *
from BaseGameEntity import *
from State import *
from JsonLoader import *

class Worker(MovingEntity):

	# identifier.
	id = None
	FSM = None
	pos = None
	speed = None
	Path = []

	# internal stats.

	def __init__(self, map):
		self.id = BaseGameEntityClass.SetID(self)
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Worker())
		self.FSM.SetGlobalState(WorkerGlobalState())
		for node in map.grid:
		    if node.isSpawn:
		        self.pos = node.center
		self.speed = JsonLoader.Data["worker"]["speed"]
		self.pos = Circle(self.pos,3)
		self.pos.setFill("red")


	def Update(self):
		self.FSM.Update()

	def GetFSM(self):
		return self.FSM

class Explorer(MovingEntity):
    
	id = None
	FSM = None
	pos = None
	speed = None
	path = []

	def __init__(self, worker):
		self.id = worker.id
		self.pos = worker.pos
		self.pos.setFill("yellow")
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life_Explorer())
		self.FSM.SetGlobalState(ExplorerGlobalState())
		self.speed = JsonLoader.Data["explorer"]["speed"]

	def Update(self):
	    self.FSM.Update()