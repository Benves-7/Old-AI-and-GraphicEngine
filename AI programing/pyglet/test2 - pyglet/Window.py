from JsonLoader import *
import pyglet

class PygWin(pyglet.window.Window):
	def __init__(self, *args, **kwrgs):
		super().__init__(*args, **kwrgs)

class Window:
	Data = None
	width = None
	heigth = None
	pygwin = None
	map = None
	indent_X = None
	indent_Y = None

	def __init__(self, name):
		self.Data = JsonLoader.Data["mapDisplay"]
		self.width = self.Data["width"]
		self.heigth = self.Data["height"]
		self.pygwin = PygWin(self.width,self.heigth, name)
