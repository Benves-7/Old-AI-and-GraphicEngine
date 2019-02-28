from MapLoader import *
from Window import *
from PathFinder import *
from JsonLoader import *
from Entitys import *


JsonLoader.LoadInJson()
map = Map("Karta Laboration 2.txt")
window = Window("map")
BaseGameEntityClass.BindWindow(map, window)
ResourceManager.FindTreeNodes()
window.DrawGrid(map)
BaseGameEntityClass.PlaceStatic()
window.window.autoflush = True
workers = []
explorers = []
i = 0
#map.find_error_node(window, 5850)



while i < 10:
	workers.append(Worker())
	i+=1

i = 0
while i < 3:
	explorers.append(Explorer(workers.pop(0)))
	i += 1
EntityManager.add_list(explorers, workers)

while True:
	for x in EntityManager.explorers:
	    x.Update()
	for x in EntityManager.workers:
		x.Update()