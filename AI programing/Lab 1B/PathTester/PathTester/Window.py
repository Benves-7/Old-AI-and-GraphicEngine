from Graphics import *

class Window:
	width = 1000
	heigth = 1000
	window = None
	map = None
	indent_X = None
	indent_Y = None

	def __init__(self, name):
		self.MakeWindow(name)

	def MakeWindow(self, name):
		self.window = GraphWin(name, self.width, self.heigth)
		self.window.master.geometry("+2000-400")

	def DrawGrid(self, map):
		self.map = map
		indent_X = self.indent_X = self.width/map.width
		indent_Y = self.indent_Y = self.heigth/map.heigth
		for y in range (0, map.heigth):
			for x in range(0, map.width):
				node = map.grid[x + (y * map.width)]
				node.x = x
				node.y = y
				a = Rectangle(Point(x*indent_X, y*indent_Y), Point(x * indent_X + indent_X, y * indent_Y + indent_Y))
				node.center = a.getCenter()
				a.setFill(color_rgb(node.color[0], node.color[1], node.color[2]))
				a.draw(self.window)
				if node.isWalkable:
					b = Text(node.center, str(node.id))
					b.draw(self.window)
		return

	def DrawPath(self, path):
		for step in path:
			for node in self.map.grid:
				if step == node.id:
					a = Circle(node.center, self.indent_X / 2)
					a.setFill("yellow")
					a.draw(self.window)
					b = Text(node.center, str(node.id))
					b.draw(self.window)
		return

	def DrawPathFCost(self, path):
		for step in path:
			for node in self.map.grid:
				if step == node.id:
					a = Circle(node.center, self.indent_X / 2)
					a.setFill("yellow")
					a.draw(self.window)
					b = Text(node.center, int(node.f))
					b.draw(self.window)
		return
	
	def DrawNode(self, currentNode, color, text = 0):
		a = Circle(self.map.grid[currentNode].center, self.indent_X/2)
		a.setFill(color)
		a.draw(self.window)
		b = Text(self.map.grid[currentNode].center, str(self.map.grid[currentNode].id))
		b.draw(self.window)
		
	def DrawNodeFCost(self, currentNode, color, text):
		a = Circle(self.map.grid[currentNode].center, self.indent_X/2)
		a.setFill(color)
		a.draw(self.window)
		b = Text(self.map.grid[currentNode].center, str(text))
		b.draw(self.window)