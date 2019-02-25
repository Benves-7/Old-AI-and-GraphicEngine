from Graphics import *
from JsonLoader import *

class Window:
	Data = None
	width = None
	heigth = None
	window = None
	map = None
	indent_X = None
	indent_Y = None

	def __init__(self, name):
		self.Data = JsonLoader.Data["mapDisplay"]
		self.width = self.Data["width"]
		self.heigth = self.Data["height"]
		self.MakeWindow(name)

	def MakeWindow(self, name):
		window = self.window = GraphWin(name, self.width, self.heigth, autoflush=False)
		window.master.geometry(self.Data["offset"])
	
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
				if (node.isKnown or not bool(self.Data["fogofwar"]) or node.isBorder):
					a.setFill(node.color)
				else:
					a.setFill("gray")
				a.draw(self.window)
				if bool(self.Data["gridnumbering"]):
					b = Text(node.center, str(node.id))
					b.draw(self.window)
		self.window.redraw()
		return

	def Draw(self, point):
		self.window.addItem(point)

	def DrawPath(self, path):
		for step in path:
			for node in self.map.grid:
				if step == node.id:
					a = Circle(node.center, self.indent_X / 2)
					a.setFill(self.Data["pathcolor"])
					a.draw(self.window)
					if bool(self.Data["gridnumbering"]):
						b = Text(node.center, str(node.id))
						b.draw(self.window)
		self.window.redraw()
		return

	def DrawPathFCost(self, path):
		for step in path:
			for node in self.map.grid:
				if step == node.id:
					a = Circle(node.center, self.indent_X / 2)
					a.setFill(self.Data["pathcolor"])
					a.draw(self.window)
					b = Text(node.center, int(node.f))
					b.draw(self.window)
		return
	
	def DrawNode(self, currentNode, color, text = 0):
		a = Circle(self.map.grid[currentNode].center, self.indent_X/2)
		a.setFill(color)
		a.draw(self.window)
		if bool(self.Data["gridnumbering"]):
			b = Text(self.map.grid[currentNode].center, str(self.map.grid[currentNode].id))
			b.draw(self.window)
		
	def DrawNodeFCost(self, currentNode, color, text):
		a = Circle(self.map.grid[currentNode].center, self.indent_X/2)
		a.setFill(color)
		a.draw(self.window)
		b = Text(self.map.grid[currentNode].center, str(text))
		b.draw(self.window)