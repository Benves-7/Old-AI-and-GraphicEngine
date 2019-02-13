from MapLoader import *
from Window import *
from PathFinder import *
from time import *



def Test(type = "", mapname = ""):
	map = Map(mapname)
	window = Window(type)
	window.DrawGrid(map)
	if type == "A-Star":
		t = time()
		path = A_Star(map, window)
		t = time() - t
	elif type == "BreadthFirst":
		t = time()
		path = BreadthFirst(map, window)
		t = time() - t
	elif type == "Own":
		t = time()
		path = PathLocator(map, window)
		t = time() - t
	elif type == "DepthFirst":
		t = time()
		path = DepthFirst(map, window)
		t = time() - t
	elif type == "":
		return
	window.DrawPath(path)
	
	#for step in path:
	#	print(step)
	print(type + " on " + mapname[0:3] + " " + mapname[3] + " Steps = " + str(len(path)) + " in " + str(round(t, 4)) + "s.")
	print("----------------------------------------------")

Test("A-Star", "Map1.txt")
Test("A-Star", "Map2.txt")
Test("A-Star", "Map3.txt")

Test("BreadthFirst","Map1.txt")
Test("BreadthFirst", "Map2.txt")
Test("BreadthFirst", "Map3.txt")

Test("DepthFirst", "Map1.txt")
Test("DepthFirst", "Map2.txt")
Test("DepthFirst", "Map3.txt")

Test("Own", "Map1.txt")
Test("Own", "Map2.txt")
Test("Own", "Map3.txt")