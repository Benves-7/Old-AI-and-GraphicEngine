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

class Node():

	isWalkable = False
	isSpawn = False
	isGoal = False
	nextId = 0
	id = 0
	color = ()

	def __init__(self, walkable, spawn, goal, color, id = 0):
		self.isWalkable = walkable
		self.isSpawn = spawn
		self.isGoal = goal
		self.color = color
		self.id = id