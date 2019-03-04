from MapLoader import *
from Window import *
from PathFinder import *
from JsonLoader import *
from Entitys import *


JsonLoader.LoadInJson()
map = Map("Karta Laboration 2.txt")
window = Window("map")
window.DrawGrid(map)
BaseGameEntityClass.BindWindow(map, window)
BaseGameEntityClass.PlaceStatic()
ResourceManager.FindTreeNodes()
window.window.autoflush = True
workers = []
explorers = []
builders = []
#map.find_error_node(window, 5850)



i = 0
while i < 25:
	workers.append(Worker())
	i+=1

i = 0
while i < 3:
	explorers.append(Explorer(workers.pop()))
	i += 1

i = 0
while i < 1:
	builders.append(Builder(workers.pop()))
	i += 1

EntityManager.add_list(explorers, workers, builders)

while True:
	for x in EntityManager.explorers:
	    x.Update()
	for x in EntityManager.workers:
		x.Update()
	for x in EntityManager.builders:
		x.Update()

	ResourceManager.searchForTrees()

	print("wood in kingdom: " + str(BaseGameEntityClass.townHall.wood))