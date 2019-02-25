from PathFinder import *

class State():
	def Enter():
		return -1
	def Execute():
		return -1
	def Exit():
		return -1
	def OnMessage(entity, telegram):
		pass

class Begin_Life_Explorer(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		worker.pos.draw(worker.window.window)
		worker.FSM.ChangeState(Explore())
	def Exit(self, worker):
		return 1

class Begin_Life_Worker(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		worker.window.Draw(worker.pos)
	def Exit(self, worker):
		return 1

class Explore(State):
	def Enter(self, explorer):
		print("going exploring!")
	def Execute(self, explorer):
		if explorer.GoTowards():
			explorer.path.pop(0)

class WorkerGlobalState(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		return 1
	def Exit(self, worker):
		return 1

class ExplorerGlobalState(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		if len(worker.path) < 1:
			worker.path = A_Star(worker.map, worker.window, worker.pos)
			print("path found.")
	def Exit(self, worker):
		return 1