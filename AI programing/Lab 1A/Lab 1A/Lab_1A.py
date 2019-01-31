import Positions
import Graphics
import State
from Miner import *
import time
import os
from math import *

# Making the map.
m_lPos = Positions.Position.pos.keys()
Window = Graphics.GraphWin("Window", 250, 180)
Window.master.geometry("+2200+42")
for name in m_lPos:
	point = Graphics.Point(Positions.Position.pos.get(name)[0],Positions.Position.pos.get(name)[1])
	Graphics.Text(point, name).draw(Window)

# Making miners.
miners = [ 
	Miner("Bob", Window, 1480),
	Miner("Jonny", Window, 0, 800, 0, 1000),
	Miner("Billy", Window, 1100, 0, 800, 0),
	Miner("Konny", Window, 0, 0, 0, 800, 0, 200)
	]

# Update loop (Game loop)
while True:

	clear = lambda: os.system('cls')
	clear()
	for miner in miners:
		print(miner.m_Name + " stats: ")
		print("Doing:		" + str(miner.m_Doing)) 
		print("Location:	" + str(ceil(miner.m_tPos[0])) + "," + str(ceil(miner.m_tPos[1])))
		print("Gold:		" + str(miner.m_iGoldCarried))
		print("Money:		" + str(miner.m_iMoneyInBank))
		print("Food:		" + str(miner.m_iFood))
		print("Thirst:		" + str(miner.m_bThirsty) + " : " + str(miner.m_iThirst))
		print("Fatige:		" + str(miner.m_bTired) +  " : " + str(miner.m_iFatige))
		print("Social:		" + str(miner.m_bLonely) +  " : " + str(miner.m_iSocial))
		print("Hunger:		" + str(miner.m_bHungry) +  " : " + str(miner.m_iHunger))
		print("Spade:		" + str(miner.m_bSpade))

		print("-------------------------------------")

	for miner in miners:
		miner.Update()