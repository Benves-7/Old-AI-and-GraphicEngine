from Worker import *
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
			self.globalState.Execute(owner)
		if self.ownerCurrentState:
			self.ownerCurrentState.Execute(owner)

	def ChangeState(self, newState):
		assert(newState and "<StateMachine::ChangeState>: trying to change to a null state")
		self.ownerPreviousState = self.ownerCurrentState
		self.ownerCurrentState.Exit(owner)
		self.ownerCurrentState = newState
		self.ownerCurrentState.Enter(owner)

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