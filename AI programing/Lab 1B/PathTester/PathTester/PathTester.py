from MapLoader import *
from Window import *

def Test_on_Map1():
	map = Map("Map1.txt")
	window2 = Window()
	window2.DrawGrid(map)

def Test_on_Map2():
	map2 = Map("Map2.txt")
	window = Window()
	window.DrawGrid(map2)


def Test_on_Map3():
	map3 = Map("Map3.txt")
	window = Window()
	window.DrawGrid(map3)

Test_on_Map1()
print("...")