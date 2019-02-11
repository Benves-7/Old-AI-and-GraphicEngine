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
		#self.heigth = len(list)
		for line in list:
			self.heigth += 1
			for character in line:
				if character == '0':
					self.grid.append(Node(True, False, False, (255, 255, 255), self.nextID))
				elif character == 'X':
					self.grid.append(Node(False, False, False, (20, 20, 20), self.nextID))
				elif character == 'S':
					self.grid.append(Node(True, True, False, (0, 0, 255), self.nextID))
				elif character == 'G':
					self.grid.append(Node(True, False, True, (0, 255, 0), self.nextID))
				self.nextID += 1

	def FindNeighbours(self, id):
		neighbours = []
		if self.grid[id - 1].isWalkable:
			neighbours.append(id - 1)
		if self.grid[id + 1].isWalkable:
			neighbours.append(id + 1)
		if self.grid[id - self.width].isWalkable:
			neighbours.append(id - self.width)
		if self.grid[id + self.width].isWalkable:
			neighbours.append(id + self.width)
		return neighbours

class Node():

	# Nodes checked.
	up = False
	down = False
	left = False
	right = False

	# Type of node.
	isWalkable = False
	isSpawn = False
	isGoal = False

	# Identifer.
	id = 0
	color = ()
	x = 0
	y = 0

	# centerpoint.
	center = None

	def __init__(self, walkable, spawn, goal, color, id = 0):
		self.isWalkable = walkable
		self.isSpawn = spawn
		self.isGoal = goal
		self.color = color
		self.id = id