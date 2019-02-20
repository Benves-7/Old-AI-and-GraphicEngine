from StateMachine import *
from BaseGameEntity import *
from State import *

class Worker(BaseGameEntityClass):

	# identifier.
	id = None
	FSM = None

	# internal stats.


	def __init__():
		self.id = BaseGameEntityClass.SetID()
		self.FSM = StateMachine(self)
		self.FSM.SetCurrentState(Begin_Life())
		self.FSM.SetGlobalState(WorkerGlobalState())

	def Update(self):
		self.FSM.Update()

	def GetFSM(self):
		return self.FSM



