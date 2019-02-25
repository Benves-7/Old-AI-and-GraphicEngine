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
Bob = Worker(map)
Bob = Explorer(Bob)


while True:
    Bob.Update()

