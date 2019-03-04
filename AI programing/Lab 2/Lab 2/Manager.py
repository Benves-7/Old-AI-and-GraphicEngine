from PathFinder import *
from BaseGameEntity import *

class Manager:
	map = None



class ResourceManager(Manager):
	treenodes = []
	treesAreKnown = False
	bestNode = None

	def FindTreeNodes():
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
    pass