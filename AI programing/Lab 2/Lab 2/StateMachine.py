from Entitys import *

class StateMachine():
    
	owner = None
	ownerCurrentState = None
	ownerPreviousState = None
	globalState = None

	def __init__(self, owner):
		self.owner = owner

	def SetCurrentState(self, state):
		self.ownerCurrentState = state

	def SetGlobalState(self, state):
		self.globalState = state

	def SetPreviousState(self, state):
		self.ownerPreviousState = state

	def Update(self):
		if self.globalState:
			self.globalState.Execute(self.owner)

		if self.ownerCurrentState:
			self.ownerCurrentState.Execute(self.owner)

	def ChangeState(self, newState):
		assert(newState and "<StateMachine::ChangeState>: trying to change to a null state")
		self.ownerPreviousState = self.ownerCurrentState
		self.ownerCurrentState.Exit(self.owner)
		self.ownerCurrentState = newState
		self.ownerCurrentState.Enter(self.owner)

	def RevertToPreviousState(self):
		self.ChangeState(self.ownerPreviousState)

	def CurrentState(self):
		return self.ownerCurrentState

	def GlobalState(self):
		return self.globalState

	def PreviusState(self):
		return self.ownerPreviousState

	def isInState(self, state):
		if self.ownerCurrentState == state:
		    return True
		else:
			return False

	def HandelMessage(self, telegram):
		if self.ownerCurrentState and self.ownerCurrentState.OnMessage(self.owner, telegram):
			return True
		elif(self.globalState and self.globalState.OnMessage(self.owner,telegram)):
			return True
		return False