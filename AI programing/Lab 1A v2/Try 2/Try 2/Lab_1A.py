import Positions
import Graphics
import State
from Miner import *
import time
import os
from math import *
from TimeManager import *

# Making the map.
m_lPos = Positions.Position.pos.keys()
Window = Graphics.GraphWin("Window", 300, 250)
Window.master.geometry("+2200+42")
for name in m_lPos:
	point = Graphics.Point(Positions.Position.pos.get(name)[0],Positions.Position.pos.get(name)[1])
	Graphics.Text(point, name).draw(Window)

# Making miners.
miners = [ 
	Miner("Bob", Window, 1480),
	Miner("Jonny", Window, 0, 800, 0, 1000),
	Miner("Billy", Window, 1100, 0, 0, 0),
	Miner("Konny", Window, 0, 0, 0, 800, 0, 200)
	]

# Update loop (Game loop)
while True:
	if not TimeManager.isPaused:
		for miner in miners:
			miner.Update()
		TimeManager.tick += 1
	time.sleep(TimeManager.UpdateDelay)