from MapLoader import *
from Window import *
from PathFinder import *
from JsonLoader import *


JsonLoader.LoadInJson()
map = Map("Karta Laboration 2.txt")
window = Window("map")
window.DrawGrid(map)

