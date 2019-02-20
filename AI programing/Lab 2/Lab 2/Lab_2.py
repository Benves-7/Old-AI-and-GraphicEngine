from MapLoader import *
from Window import *
from PathFinder import *


map = Map("Map4.txt")
window = Window("map")
window.DrawGrid(map)
path = A_star(map, window)
window.DrawPath(path)
