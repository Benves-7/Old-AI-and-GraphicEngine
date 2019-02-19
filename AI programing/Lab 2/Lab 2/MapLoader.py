from FileLoader import *
class Map:

	width = 0
	heigth = 0
	nextID = 0
	grid = []

	def __init__(self, fileName):
		self.grid = []
		self.MakeMap(fileName)

	def MakeMap(self, fileName):
		list = LoadFiletoList(fileName)
		self.width = len(list[0])
		i = 1
		for line in list:
			self.heigth += 1
			for character in line:
				if character == 'M':
					self.grid.append(Node(True, False, False, (0, 255, 0), self.nextID))
				elif character == 'X':
					self.grid.append(Node(False, False, False, (20, 20, 20), self.nextID))
				elif character == 'S':
					self.grid.append(Node(True, True, False, (0, 0, 255), self.nextID))
				elif character == 'G':
					self.grid.append(Node(True, False, True, (0, 255, 0), self.nextID))
				self.nextID += 1
			print("line " + str(i) + " done.")
			i+=1
		print("map complete.")
	def FindNeighbours(self, id):
		neighbours = []
		if self.grid[id - 1].isWalkable: #left
			neighbours.append(id - 1)
		if self.grid[id - self.width].isWalkable: #up
			neighbours.append(id - self.width)
		if self.grid[id + 1].isWalkable: #right
			neighbours.append(id + 1)
		if self.grid[id + self.width].isWalkable: #down
			neighbours.append(id + self.width)
		return neighbours

	def FindNeighboursA_Star(self, id):
		
		left = False
		right = False
		up = False
		down = False
		width = self.width

		neighbours = []
		if self.grid[id - 1].isWalkable: #left
			neighbours.append(id-1)
			left = True
		if self.grid[id + 1].isWalkable: #right
			neighbours.append(id+1)
			right = True
		if self.grid[id - width].isWalkable: #up
			neighbours.append(id-width)
			up = True
		if self.grid[id + width].isWalkable: #down
			neighbours.append(id+width)
			down = True
		if self.grid[id - width + 1].isWalkable and up and right:
			neighbours.append(id-width+1)
		if self.grid[id - width - 1].isWalkable and up and left:
			neighbours.append(id-width-1)
		if self.grid[id + width + 1].isWalkable and down and right:
			neighbours.append(id+width+1)
		if self.grid[id + width - 1].isWalkable and down and left:
			neighbours.append(id+width-1)
		return neighbours

class Node():

	# internal grid 10x10m  
	grid = []

	# Nodes checked.
	up = False
	down = False
	left = False
	right = False

	# Type of node.
	isWalkable = False
	isSpawn = False
	isGoal = False
	isKnown = False

	# Identifer.
	id = 0
	color = ()
	x = 0
	y = 0
	f = 0

	# centerpoint.
	center = None

	def __init__(self, walkable, spawn, goal, color, id = 0):
		self.isWalkable = walkable
		self.isSpawn = spawn
		self.isGoal = goal
		self.color = color
		self.id = id
		i = 0
		while i < 100:
			if self.isWalkable:
				self.grid.append(SmallNode(True, False, False))

class SmallNode():

	# Type of node.
	isWalkable = False
	isTree = False
	isWater = False

	def __init__(self, walkable, tree, water):
		self.isWalkable = walkable
		self.isTree = tree
		self.isWater = water