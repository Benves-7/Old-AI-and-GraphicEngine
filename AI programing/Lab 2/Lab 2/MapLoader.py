from FileLoader import *
from JsonLoader import *

class Map:
	Data = None
	width = 0
	heigth = 0
	nextID = 0
	grid = []

	def __init__(self, fileName):
		self.Data = JsonLoader.Data["mapLoader"]
		self.grid = []
		self.MakeMap(fileName)

	def MakeMap(self, fileName):
		list = LoadFiletoList(fileName)
		self.width = len(list[0])
		i = 1
		for line in list:
			self.heigth += 1
			for character in line:
				if character	== 'X':
					self.grid.append(Node(self.Data["nodeTypes"]["unpassableNode"], self.nextID)) #unpassable
				elif character	== 'S':
					self.grid.append(Node(self.Data["nodeTypes"]["groundNode"], self.nextID, True)) #spawn
				elif character	== 'P':
					self.grid.append(Node(self.Data["nodeTypes"]["goalNode"], self.nextID)) #goal
				elif character	== 'M':
					self.grid.append(Node(self.Data["nodeTypes"]["groundNode"], self.nextID)) #ground
				elif character	== 'G':
					self.grid.append(Node(self.Data["nodeTypes"]["swampNode"], self.nextID)) #swamp
				elif character	== 'B':
					self.grid.append(Node(self.Data["nodeTypes"]["mountainNode"], self.nextID)) #mountain
				elif character	== 'V':
					self.grid.append(Node(self.Data["nodeTypes"]["waterNode"], self.nextID)) #water
				elif character	== 'T':
					self.grid.append(Node(self.Data["nodeTypes"]["treeNode"], self.nextID)) #trees
				self.nextID += 1

		print("Map done.")

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

	def FindNeighboursAll(self, id):
		
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
	# Nodes checked.
	up = False
	down = False
	left = False
	right = False

	# Type of node.
	isSpawn = False
	isBorder = False
	isSwamp = False
	isWalkable = False
	isbuildable = False
	isKnown = False

	#stats
	speed = 0
	numTrees = 0

	# Identifer.
	id = 0
	color = None
	curColor = None
	x = 0
	y = 0
	f = 0

	# centerpoint.
	center = None

	def __init__(self, Data, id, spawn = False):
		if spawn:
		    self.isSpawn = self.isKnown = spawn
		if Data["type"] == "swamp":
			self.isSwamp = True
		self.isWalkable = bool(Data["isWalkable"])
		if self.isWalkable:
		    self.speed = Data["speed"]
		self.isbuildable = bool(Data["isBuildable"])

		if "numTrees" in Data:
			numTrees = Data["numTrees"]
		if "isBorder" in Data:
			self.isBorder = bool(Data["isBorder"])

		self.color = Data["color"]

		self.id = id