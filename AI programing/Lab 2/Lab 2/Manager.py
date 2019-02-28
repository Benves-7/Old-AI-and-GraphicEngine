from PathFinder import *
from BaseGameEntity import *

class Manager:
	map = None



class ResourceManager(Manager):
	treenodes = []

	def FindTreeNodes():
		ResourceManager.map = BaseGameEntityClass.map
		for node in ResourceManager.map.grid:
			if node.treesLeft > 0 and node not in ResourceManager.treenodes:
				ResourceManager.treenodes.append(node)

	def searchForTrees(worker):
		for node in ResourceManager.treenodes:
		    if node.treesLeft == 0:
		        ResourceManager.treenodes.remove(node)

		for node in ResourceManager.treenodes:
			if node.isKnown:
				return True
		return False

	def ClosestTreeNode():
	    for node in ResourceManager.treenodes:
	        pass  ##FIX

	def closestTree():
		pass
