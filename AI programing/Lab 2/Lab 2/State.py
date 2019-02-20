class State():
	def Enter():
		return -1
	def Execute():
		return -1
	def Exit():
		return -1

class Begin_Life(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		return 1
	def Exit(self, worker):
		return 1

class WorkerGlobalState(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		return 1
	def Exit(self, worker):
		return 1