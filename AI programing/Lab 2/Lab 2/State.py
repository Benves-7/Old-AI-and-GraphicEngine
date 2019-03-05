from PathFinder import *
from Manager import *
from JsonLoader import *

class State():
	def Enter(self, entity):
		return -1
	def Execute(self, entity):
		return -1
	def Exit(self, entity):
		return -1
	def OnMessage(entity, telegram):
		pass

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self.__eq__(other)

class DEAD(State):
	def Execute(self, explorer):
		explorer.Del()

class IDLE(State):
	def Execute(self, worker):
		return 0 # Skip turn...

# Explorer--------------------------------
class ExplorerGlobalState(State):
	def Enter(self, explorer):
		return 1

	def Execute(self, explorer):
		if explorer.path == None and explorer.failedPathFindingAttempts < 200:
			explorer.path = A_Star(explorer.map, explorer, explorer.pos)
		elif explorer.path == None and explorer.failedPathFindingAttempts >= 200:
			for node in explorer.map.grid:
				if not node.isKnown:
					end_node = node.id
					break
			explorer.path = BreadthFirst(explorer.map, explorer.window, explorer.pos, end_node)

	def Exit(self, explorer):
		return 1

class Begin_Life_Explorer(State):
	def Execute(self, explorer):
		explorer.circle.draw(explorer.window.window)
		explorer.FSM.ChangeState(Explore())
		explorer.ExploreNeighbours()

class Explore(State):
	def Execute(self, explorer):
		if explorer.GoTowards():
			explorer.pos = explorer.path.pop(0)
			explorer.ExploreNeighbours()
			if len(explorer.path) == 0:
				explorer.path = None
		return

# Workers --------------------------------
class WorkerGlobalState(State):
	PathToBestNode = None

	def Execute(self, worker):
		if ResourceManager.treesAreKnown and worker.FSM.isInState(IDLE()):
			if worker.path == None:
				if WorkerGlobalState.PathToBestNode and ResourceManager.bestNode.treesReserved > 0:
					worker.path = WorkerGlobalState.PathToBestNode.copy()
				else:
					WorkerGlobalState.PathToBestNode = worker.path = BreadthFirst(worker.map, worker.window, worker.pos, ResourceManager.ClosestTreeNode())
				if ResourceManager.bestNode:
					ResourceManager.bestNode.treesReserved -= 1
				worker.FSM.ChangeState(GoingToWork())
		return

class Begin_Life_Worker(State):
	def Enter(self, worker):
		return 1
	def Execute(self, worker):
		worker.circle.draw(worker.window.window)
		worker.FSM.ChangeState(IDLE())
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
				worker.FSM.ChangeState(IDLE())
		return


# Builders -------------------------------
class BuilderGlobalState(State):
	def Execute(self, builder):
		if not builder.colemil and builder.townHall.wood >= JsonLoader.Data["entitys"]["colemil"]["cost"] and builder.FSM.isInState(IDLE()):
			builder.path = BreadthFirst(builder.map, builder.window, builder.pos, builder.map.FindBuildingSite(builder.townHall)[0])
			builder.FSM.ChangeState(GoToBuildingSite())
		return

class Begin_Life_Builder(State):
	def Execute(self, builder):
		builder.circle.draw(builder.window.window)
		builder.FSM.ChangeState(IDLE())

class GoToBuildingSite(State):
	def Execute(self, builder):
		if builder.GoTowards():
			builder.pos = builder.path.pop(0)
			if len(builder.path) == 0:
				builder.FSM.ChangeState(Build())
		return

class Build(State):
	def Enter(self, builder):
		builder.startTime = time()
		BaseGameEntityClass.coleMil = Entitys.ColeMil(builder.pos)

	def Execute(self, builder):
		builder.freezeTime = time()
		if not builder.colemil and builder.freezeTime - builder.startTime > JsonLoader.Data["entitys"]["colemil"]["time"]:
			BaseGameEntityClass.coleMil.circle.setFill(BaseGameEntityClass.coleMil.color)
			BaseGameEntityClass.townHall.wood -= 10
			builder.colemil = True
			builder.coleMil.complete = True
			builder.FSM.ChangeState(IDLE())
		return


# Hanterkare -----------------------------
class FineWorkerGlobalState(State):
	def Execute(self, fineWorker):
		if fineWorker.coleMil and fineWorker.coleMil.complete and fineWorker.FSM.isInState(IDLE()):
			fineWorker.path = BreadthFirst(fineWorker.map, fineWorker.window, fineWorker.pos, fineWorker.map.FindBuildingSite(fineWorker.townHall)[0])
			fineWorker.FSM.ChangeState(GoToWork())
		return

class Begin_Life_Fine_Worker(State):
	def Execute(self, fineWorker):
		fineWorker.circle.draw(fineWorker.window.window)
		fineWorker.FSM.ChangeState(IDLE())

class GoToWork(State):
	def Execute(self, fineWorker):
		if fineWorker.GoTowards():
			fineWorker.pos = fineWorker.path.pop(0)
			if len(fineWorker.path) == 0:
				fineWorker.FSM.ChangeState(MakeCharcoal())
		return

class MakeCharcoal(State):
	def Enter(self, fineWorker):
		fineWorker.startTime = time()

	def Execute(self, fineWorker):
		fineWorker.freezeTime = time()
		t = fineWorker.freezeTime - fineWorker.startTime
		if fineWorker.freezeTime - fineWorker.startTime > 3 and fineWorker.townHall.wood > 2:
			fineWorker.townHall.charcoal += 1
			fineWorker.townHall.wood -= 2
			fineWorker.startTime = time()
