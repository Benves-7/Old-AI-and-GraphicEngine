import Positions
import Graphics
import State
import Miner
import time
import os


m_lPos = Positions.Position.pos.keys()
Window = Graphics.GraphWin("Window", 500, 500)
for name in m_lPos:
	point = Graphics.Point(Positions.Position.pos.get(name)[0],Positions.Position.pos.get(name)[1])
	Graphics.Text(point, name).draw(Window)

Bob = Miner.Miner("Bob",Window, State.Home(), "Home", 0, 0, 0, 0)
#Jon = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Billy = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Konny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Lonny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Ronny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)

while True:

	clear = lambda: os.system('cls')
	clear()
	print(Bob.m_Name + " stats:	")
	print("Doing:       " + str(Bob.m_Doing))
	print("Location:    " + str(Bob.m_tPos))
	print("Gold:        " + str(Bob.m_iGoldCarried))
	print("Money:       " + str(Bob.m_iMoneyInBank))
	print("Thirst:      " + str(Bob.m_iThirst))
	print("Fatige:      " + str(Bob.m_iFatige))
	print("Social:      " + str(Bob.m_iSocial))
	print("Hunger:      " + str(Bob.m_iHunger))


	Bob.Update()
	#Jon.Update()
	#Billy.Update()
	#Konny.Update()
	#Lonny.Update()
	#Ronny.Update()