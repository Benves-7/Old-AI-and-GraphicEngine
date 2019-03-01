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
		if explorer.path == None:
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
			if len(explorer.path) == 0:
				explorer.path = None
	
	def Exit(self, explorer):
		return 1


# Workers --------------------------------
class WorkerGlobalState(State):
	def Enter(self, worker):
		return 1

	def Execute(self, worker):
		if ResourceManager.treesAreKnown:
			worker.FSM.Changestate(GoingToWork())
			if worker.path == None:
				worker.path = BreadthFirst(worker.map, worker.window, worker.pos, ResourceManager.ClosestTreeNode())
				if ResourceManager.bestNode:
					ResourceManager.bestNode.treesReserved -= 1
		else:
			worker.FSM.ChangeState(IDLE())

	def Exit(self, worker):
		return 1

class IDLE(State):
	def Execute(self, worker):
		#skip
		return 0

class Begin_Life_Worker(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		worker.circle.draw(worker.window.window)
		worker.FSM.ChangeState(GoingToWork())
	def Exit(self, worker):
		return 1

class GoingToWork(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		if worker.GoTowards():
			worker.pos = worker.path[0]
			worker.pathBack.append(worker.path.pop(0))
			if len(worker.path) == 0:
				worker.FSM.ChangeState(ChopWood())
	def Exit(self, worker):
		return 1

class ChopWood(State):
	def Enter(self, worker):
	    worker.startTime = time()

	def Execute(self, worker):
		worker.freezeTime = time()
		if worker.freezeTime - worker.startTime > 5:
			worker.map.grid[worker.pos].treesLeft -= 1
			tree = worker.map.grid[worker.pos].trees.pop()
			tree.circle.undraw()
			worker.pathBack.reverse()
			worker.path = worker.pathBack
			worker.pathBack = []
			worker.FSM.ChangeState(TransportBack())
		return

class TransportBack(State):
	def Execute(self, worker):
		if worker.map.grid[worker.pos].trees and len(worker.pathBack) < 1:
			worker.carrying["wood"] = 1
		if worker.GoTowards():
			worker.pos = worker.path[0]
			worker.pathBack.append(worker.path.pop(0))
			if len(worker.path) == 0:
				worker.townHall.wood += 1
				worker.path = None
				worker.pathBack = []
				worker.FSM.ChangeState(GoingToWork())
	return


# Builders -------------------------------

