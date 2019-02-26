from MapLoader import *
from Window import *
from PathFinder import *
from JsonLoader import *
from Worker import *


JsonLoader.LoadInJson()
map = Map("Karta Laboration 2.txt")
window = Window("map")
BaseGameEntityClass.BindWindow(map, window)
window.DrawGrid(map)
window.window.autoflush = True
workers = []
explorers = []
i = 0
while i < 50:
	workers.append(Worker())
	i+=1
for x in workers:
    explorers.append(Explorer(x))

i = 0
while True:
	for x in explorers:
	    x.Update()