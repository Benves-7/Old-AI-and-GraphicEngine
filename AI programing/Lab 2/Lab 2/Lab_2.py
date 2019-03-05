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
drawnow = True
tick = 0
workers = []
explorers = []
builders = []
fineworkers = []

i = 0
while i < 50:
	workers.append(Worker())
	i+=1

i = 0
while i < JsonLoader.Data["entitys"]["explorer"]["goalnumber"]:
	explorers.append(Explorer(workers.pop()))
	i += 1

i = 0
while i < 1:
	builders.append(Builder(workers.pop()))
	fineworkers.append(FineWorker(workers.pop()))
	i += 1

EntityManager.add_list(explorers, workers, builders, fineworkers)

while True:
	t = time()
	if drawnow:

		for x in EntityManager.explorers:
		    x.Update()
		for x in EntityManager.workers:
			x.Update()
		for x in EntityManager.builders:
			x.Update()
		for x in EntityManager.fineworkers:
		    x.Update()

		ResourceManager.searchForTrees()

		t = time() - t
		if t > 1:
			window.window.autoflush = False
			drawnow = False

	else:
		for x in EntityManager.explorers:
		    x.Update()
		for x in EntityManager.workers:
			x.Update()
		for x in EntityManager.builders:
			x.Update()
		for x in EntityManager.fineworkers:
		    x.Update()

		ResourceManager.searchForTrees()
		tick = time  ##make a tick based update..

		window.window.update()


	print("wood in kingdom: " + str(BaseGameEntityClass.townHall.wood))
	print("coal in kingdom: " + str(BaseGameEntityClass.townHall.charcoal))