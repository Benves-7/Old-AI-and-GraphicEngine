from MapLoader import *
from Window import *
from PathFinder import *
from JsonLoader import *
from Entitys import *
from os import system


JsonLoader.LoadInJson()
map = Map("Karta Laboration 2.txt")
window = Window("map")
window.DrawGrid(map)
BaseGameEntityClass.BindWindow(map, window)
BaseGameEntityClass.PlaceStatic()
ResourceManager.FindTreeNodes()
#window.window.autoflush = True
drawnow = True
tick = 0
tickstart = 0
workers = []
explorers = []
builders = []
fineworkers = []
t = perf_counter() - t
print("explorer time: " + str(t))



i = 0
while i < 25:
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
tickstart = perf_counter()

while True:
	tick = perf_counter()

	for x in EntityManager.explorers:
		x.Update()

	for x in EntityManager.workers:
		x.Update()

	for x in EntityManager.builders:
		x.Update()

	for x in EntityManager.fineworkers:
		x.Update()

	ResourceManager.searchForTrees()

	if tick - tickstart > 4:
		window.window.update()

	clear = lambda: system('cls')
	clear()
