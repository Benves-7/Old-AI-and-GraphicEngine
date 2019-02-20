from MapLoader import *
from Window import *
from PathFinder import *



map = Map("Karta Laboration 2.txt")
window = Window("map")
window.DrawGrid(map)
path = A_Star(map, window)
window.DrawPath(path)
