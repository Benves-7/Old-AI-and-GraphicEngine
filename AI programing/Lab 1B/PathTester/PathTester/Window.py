from Graphics import *

class Window:
	width = 1000
	heigth = 1000
	window = None
	
	def __init__(self):
		self.MakeWindow()

	def MakeWindow(self):
		self.window = GraphWin("pathtest", self.width, self.heigth)

	def DrawGrid(self, map):
		indent_X = self.width/map.width
		indent_Y = self.heigth/map.heigth
		
		for y in range (0, map.heigth):
			for x in range(0, map.width):
				index = x + (y * map.width)
				a = Rectangle(Point(x*indent_X, y*indent_Y), Point(x * indent_X + indent_X, y * indent_Y + indent_Y))
				a.setFill(color_rgb(map.grid[index].color[0], map.grid[index].color[1], map.grid[index].color[2]))
				b = Text(a.getCenter(), str(map.grid[x + (y * map.width)].id))
				a.draw(self.window)
				if map.grid[index].isWalkable:
				   b.draw(self.window) 