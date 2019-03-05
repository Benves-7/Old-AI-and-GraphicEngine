from MapLoader import *
from Window import *
from JsonLoader import *
from BaseGameEntity import *
from PathFinder import *
from Entitys import *


class Manager:
	map = None

	def Bind():
	    Manager.map = BaseGameEntityClass.map

	def Start():
		JsonLoader.LoadInJson()
		map = BaseGameEntityClass.map = Map("Karta Laboration 2.txt")
		window = BaseGameEntityClass.window = Window("map")
		window.DrawGrid(map)
		BaseGameEntityClass.data = JsonLoader.Data["entitys"]
		BaseGameEntityClass.PlaceStatic()
		i = 0
		while i < JsonLoader.Data["entitys"]["numentitys"]:
			EntityManager.workers.append(Worker())
			i+=1


	def Update():
		ResourceManager.searchForTrees()
		TrainingManager.CheckStatus()

		for x in EntityManager.explorers:
			x.Update()

		for x in EntityManager.workers:
			x.Update()

		for x in EntityManager.builders:
			x.Update()

		for x in EntityManager.fineworkers:
			x.Update()

class ResourceManager(Manager):
	treenodes = []
	treesAreKnown = False
	bestNode = None

	def BindMap():
		ResourceManager.map = BaseGameEntityClass.map

	def searchForTrees():
		if ResourceManager.RemoveEmpty():
			return 

		for node in ResourceManager.treenodes:
			if node.isKnown:
				ResourceManager.treesAreKnown = True
				return
		ResourceManager.treesAreKnown = False

	def RemoveEmpty():
		for node in ResourceManager.treenodes:
			if node.treesReserved == 0:
				ResourceManager.treenodes.remove(node)
		if len(ResourceManager.treenodes) == 0:
			return True
	
	def ClosestTreeNode():

		treenodes = ResourceManager.treenodes #

		if ResourceManager.bestNode and ResourceManager.bestNode.treesReserved > 0:
		    return ResourceManager.bestNode.id
		else:
			if ResourceManager.RemoveEmpty():
				ResourceManager.treesAreKnown = False
				ResourceManager.bestNode = None
				return BaseGameEntityClass.townHall.pos
			dist = 10000
			for node in ResourceManager.treenodes:
				if node.treesReserved >= 1:
					if node.dist < dist:
						ResourceManager.bestNode = node
						dist = node.dist

		return ResourceManager.bestNode.id

class TrainingManager(Manager):
	def CheckStatus():
		if len(EntityManager.explorers) < JsonLoader.Data["entitys"]["explorer"]["goalnumber"] and EntityManager.workers[-1].FSM.isInState(IDLE()):
			print("explorer needed.")
			EntityManager.explorers.append(Explorer(EntityManager.workers.pop()))
		if len(EntityManager.builders) < JsonLoader.Data["entitys"]["builder"]["goalnumber"] and EntityManager.workers[-1].FSM.isInState(IDLE()) and BaseGameEntityClass.townHall.wood > JsonLoader.Data["entitys"]["colemil"]["cost"]:
			print("builder needed.")
			EntityManager.builders.append(Builder(EntityManager.workers.pop()))
		if len(EntityManager.fineworkers) < JsonLoader.Data["entitys"]["fineworker"]["goalnumber"] and EntityManager.workers[-1].FSM.isInState(IDLE()) and BaseGameEntityClass.coleMil and BaseGameEntityClass.coleMil.complete:
			print("fineworker needed.")
			EntityManager.fineworkers.append(FineWorker(EntityManager.workers.pop()))