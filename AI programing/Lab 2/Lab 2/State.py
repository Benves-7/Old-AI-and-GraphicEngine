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


# Explorer--------------------------------
class ExplorerGlobalState(State):
	def Enter(self, explorer):
		return 1

	def Execute(self, explorer):
		if len(explorer.path) < 1:
			explorer.path = A_Star(explorer.map, explorer.window, explorer.pos)

	def Exit(self, explorer):
		return 1

class Begin_Life_Explorer(State):
	def Enter(self, explorer):
		return 1
	def Execute(self, explorer):
		explorer.circle.draw(explorer.window.window)
		explorer.FSM.ChangeState(Explore())
		explorer.ExploreNeighbours()
	def Exit(self, explorer):
		return 1

class Explore(State):
	def Enter(self, explorer):
		return 1

	def Execute(self, explorer):
		if explorer.GoTowards():
			explorer.pos = explorer.path[0]
			explorer.ExploreNeighbours()
			explorer.path.pop(0)
	
	def Exit(self, explorer):
		return 1


# Workers --------------------------------
class WorkerGlobalState(State):
	def Enter(self, worker):
		return 1

	def Execute(self, worker):
		if True:
		    pass

	def Exit(self, worker):
		return 1

class Begin_Life_Worker(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		worker.circle.draw(worker.window.window)
		worker.FSM.ChangeState(Work())
	def Exit(self, worker):
		return 1

class Work(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		    pass
	def Exit(self, worker):
		return 1



