from Window import *
from queue import *
from math import *
from time import *

class Node():
    # Node for a* pathfinding

	def __init__(self, parent = None, position = None):
		self.parent = parent
		self.position = position

		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self, other):
		return self.position == other.position 

def Explore(map,window, start_node):


def A_Star(map, window, start_node = None, end_node = None):
	# Returns a list of tuples as a path from given start to given end in the given maze.

	# Create start and end node.
	if start_node == None:
		for node in map.grid:
			if node.isSpawn:
				start_node = Node(None, node.id)
			elif node.isGoal:
				end_node = Node(None, node.id)
	else:
		start_node = Node(None, start_node)
		end_node = Node(None, end_node)

	start_node.g = start_node.h = start_node.f = 0
	end_node.g = end_node.h = end_node.f = 0

	# Make open and closed list.
	open_list = []
	closed_list = []

	# Add the start node.
	open_list.append(start_node)

	# Loop until you find the end.
	while len(open_list) > 0:
		# Get the current node.

		current_node = open_list[0]
		current_index = 0
		#if(len(open_list)>100):
		#	open_list = Sort_F_Cost(open_list)
		for index, item in enumerate(open_list):
			if item.f < current_node.f:
				current_node = item
				current_index = index

		# Pop current off open list, add to closed list
		open_list.pop(current_index)
		closed_list.append(current_node)


		# Found Goal
		if current_node == end_node:
			path = []
			current = current_node
			while current is not None:
				path.append(current.position)
				current = current.parent
			return path[::-1] # return reversed path

		# Generate children
		children = []
		neighbours = map.FindNeighboursAll(current_node.position)
		for node_position in neighbours:

			# Append
			children.append(Node(current_node, node_position))

		# Loop through children
		#window.DrawNode(current_node.position, "red", int(current_node.f))
		neighbours = []
		for child in children:

			# Child is on the closed list.
			if child in closed_list:
				continue

			# Create the f, g and h values
			if child.position == current_node.position +1 or child.position == current_node.position -1 or child.position == current_node.position + map.width or child.position == current_node.position - map.width:
				if map.grid[current_node.position].isSwamp:
				    child.g = current_node.g + 20
				else:
					child.g = current_node.g + 10
			else:
				if map.grid[current_node.position].isSwamp:
				    child.g = current_node.g + 28
				else:
					child.g = current_node.g + 14
			
			child.h = ((abs(map.grid[child.position].x - map.grid[end_node.position].x)*10)) + ((abs(map.grid[child.position].y - map.grid[end_node.position].y) *10))
			child.f = child.g + child.h

			# Child is already in the open list
			if child in open_list and child.g > open_list[open_list.index(child)].g:
					continue
			# Add the cild to the open list
			open_list.append(child)
			
			#window.DrawNode(child.position, "green", int(child.f))
			map.grid[child.position].f = child.f

def BreadthFirst(map, window):

	for node in map.grid:
		if node.isSpawn:
			start_node = node.id
		elif node.isGoal:
			end_node = node.id
	frontier = Queue()
	frontier.put(start_node)
	came_from = {}
	came_from[start_node] = True
	
	while not frontier.empty():
		current = frontier.get()
		#window.drawnode(current, "red")
		for next in map.FindNeighbours(current):
			if next not in came_from:
				#window.drawnode(next, "green")
				frontier.put(next)
				came_from[next] = current

		if current == end_node:
			path = []
			while current != start_node:
				path.append(current)
				current = came_from[current]
			path.append(start_node)
			path.reverse()
			return path
	return

def DepthFirst(map, window):
	for node in map.grid:
		if node.isSpawn:
			start_node = node.id
		elif node.isGoal:
			end_node = node.id

	stack = []
	stack.append(start_node)
	came_from = {}
	came_from[start_node] = True
	while len(stack) > 0:
		current = stack.pop()
		#window.drawnode(current, "red")
		for next in map.FindNeighbours(current):
			if next not in came_from:
				#window.drawnode(next, "green")
				stack.append(next)
				came_from[next] = current

		if current == end_node:
			path = []
			while current != start_node:
				path.append(current)
				current = came_from[current]
			path.append(start_node)
			path.reverse()
			return path
	return

class PathLocatorObject():
    
	map = None
	window = None
	start_node = None
	end_node = None
	frontier = Queue()
	came_from = {}
	up_interupted = False
	down_interupted = False
	left_interupted = False
	right_interupted = False

	def __init__(self, map, window):
		self.map = map
		self.window = window
		for node in map.grid:
			if node.isSpawn:
				self.start_node = node.id
			elif node.isGoal:
				self.end_node = node.id
		self.frontier.put(self.start_node)
		self.came_from = {}
		self.came_from[self.start_node] = True

	def moveUp(self, current, window):
		next = current - self.map.width
		if next in self.came_from:
			self.up_interupted = True
			self.map.grid[current].up = True
			return current
		if self.map.grid[next].isWalkable:
			self.came_from[next] = current
			#window.drawnode(next, "green")
			self.map.grid[current].up = True
			return next
		else:
			self.up_interupted = True
			self.map.grid[current].up = True
			return current

	def moveDown(self, current, window):
		next = current + self.map.width
		if next in self.came_from:
			self.down_interupted = True
			self.map.grid[current].down = True
			return current
		if self.map.grid[next].isWalkable:
			self.came_from[next] = current
			#window.drawnode(next, "green")
			self.map.grid[current].down = True
			return next
		else: 
			self.down_interupted = True
			self.map.grid[current].down = True
			return current

	def moveLeft(self, current, window):
		next = current - 1
		if next in self.came_from:
			self.left_interupted = True
			self.map.grid[current].left = True
			return current
		if self.map.grid[next].isWalkable:
			self.came_from[next] = current
			#window.drawnode(next, "green")
			self.map.grid[current].left = True
			return next
		else: 
			self.left_interupted = True
			self.map.grid[current].left = True
			return current

	def moveRight(self, current, window):
		next = current + 1
		if next in self.came_from:
			self.right_interupted = True
			self.map.grid[current].right = True
			return current
		if self.map.grid[next].isWalkable:
			self.came_from[next] = current
			#window.drawnode(next, "green")
			self.map.grid[current].right = True
			return next
		else: 
			self.right_interupted = True
			self.map.grid[current].right = True
			return current

	def CancelInterupts(self):
		self.up_interupted = False
		self.down_interupted = False
		self.left_interupted = False
		self.right_interupted = False
		
def PathLocator(map, window):
	PLO = None
	PLO = PathLocatorObject(map, window)

	current = PLO.start_node

	while current is not PLO.end_node:

		while not PLO.up_interupted:
			if current == PLO.end_node:
				break
			current = PLO.moveUp(current, window)

		while not PLO.down_interupted:
			if current == PLO.end_node:
				break
			current = PLO.moveDown(current, window)

		while not PLO.left_interupted:
			if current == PLO.end_node:
				break
			current = PLO.moveLeft(current, window)

		while not PLO.right_interupted:
			if current == PLO.end_node:
				break
			current = PLO.moveRight(current, window)

		if current == PLO.end_node:
			path = []
			while current != PLO.start_node:
				path.append(current)
				current = PLO.came_from[current]
			path.append(PLO.start_node)
			path.reverse()
			return path
		
		if (PLO.map.grid[current].up and PLO.map.grid[current].down and PLO.map.grid[current].left and PLO.map.grid[current].right):
			#window.drawnode(current, "red")
			current = PLO.came_from[current]
			PLO.CancelInterupts()
		else:
			PLO.CancelInterupts()