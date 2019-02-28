from PathFinder import *
from Manager import *

class State():
	def Enter(self, entity):
		return -1
	def Execute(self, entity):
		return -1
	def Exit(self, entity):
		return -1
	def OnMessage(entity, telegram):
		pass

class DEAD(State):
	def Execute(self, explorer):
		explorer.Del()


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
			explorer.pos = explorer.path.pop(0)
			explorer.ExploreNeighbours()
	
	def Exit(self, explorer):
		return 1


# Workers --------------------------------
class WorkerGlobalState(State):
	def Enter(self, worker):
		return 1

	def Execute(self, worker):
		if ResourceManager.searchForTrees(worker):
			if worker.path == None or len(worker.path) == 0:
				worker.path = BreadthFirst(worker.map, worker.window, worker.pos, ResourceManager.treenodes[0].id)
				ResourceManager.treenodes[0].treesLeft -= 1
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
		if worker.GoTowards():
			worker.pos = worker.path[0]
			worker.pathBack.append(worker.path.pop(0))
			if worker.pos == worker.townHall.pos and len(worker.pathBack) > 1:
			    worker.path = BreadthFirst(worker.map, worker.window, worker.pos, ResourceManager.ClosestTreeNode())
			if len(worker.path) == 0:
				worker.pathBack.reverse()
				worker.path = worker.pathBack
				worker.pathBack = []
	def Exit(self, worker):
		return 1



