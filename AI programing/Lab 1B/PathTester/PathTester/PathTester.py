from MapLoader import *
from Window import *
from PathFinder import *

def Test_on_Map1(type = ""):
	map = Map("Map1.txt")
	window = Window()
	window.DrawGrid(map)
	if type == "A-Star":
	    path = A_Star(map, window)
	elif type == "BreadthFirst":
		path = BreadthFirst(map, window)
	elif type == "Own":
		path = PathLocator(map, window)
	elif type == "DepthFirst":
		path = DepthFirst(map, window)
	elif type == "":
		return
	window.DrawPath(path)
	
	for step in path:
		print(step)
	print("----------------------------------------------")

def Test_on_Map2(type = ""):
	map = Map("Map2.txt")
	window = Window()
	window.DrawGrid(map)
	if type == "A-Star":
	    path = A_Star(map, window)
	elif type == "BreadthFirst":
		path = BreadthFirst(map, window)
	elif type == "Own":
		path = PathLocator(map, window)
	elif type == "DepthFirst":
		path = DepthFirst(map, window)
	elif type == "":
		return
	window.DrawPath(path)
	
	for step in path:
		print(step)
	print("----------------------------------------------")


def Test_on_Map3(type = ""):
	map = Map("Map3.txt")
	window = Window()
	window.DrawGrid(map)
	if type == "A-Star":
	    path = A_Star(map, window)
	elif type == "BreadthFirst":
		path = BreadthFirst(map, window)
	elif type == "Own":
		path = PathLocator(map, window)
	elif type == "DepthFirst":
		path = DepthFirst(map, window)
	elif type == "":
		return
	window.DrawPath(path)
	
	for step in path:
		print(step)
	print("----------------------------------------------")

#Test_on_Map1("A-Star")
#Test_on_Map2("A-Star")
#Test_on_Map3("A-Star")

Test_on_Map1("BreadthFirst")
Test_on_Map2("BreadthFirst")
Test_on_Map3("BreadthFirst")

#Test_on_Map1("Own")
#Test_on_Map2("Own")
#Test_on_Map3("Own")