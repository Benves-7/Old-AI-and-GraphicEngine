import State
import BaseGameEntity
import time
import os


print("hej");
Bob = BaseGameEntity.Miner("Bob", 0, State.Home(), "Home", 9, 30, 0, 15)
#Jon = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Billy = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Konny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Lonny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)
#Ronny = BaseGameEntity.Miner(0, "state", "location", 10, 30, 0, 15)

print("Bob id: " + str(Bob.m_ID) )
#print("Jon id: " + str(Jon.m_ID) )
#print("Billy id: " + str(Billy.m_ID) )
#print("Konny id: " + str(Konny.m_ID) )
#print("Lonny id: " + str(Lonny.m_ID) )
#print("Ronny id: " + str(Ronny.m_ID) )

while True:
    time.sleep(1.5)
    clear = lambda: os.system('cls')
    clear()

    Bob.Update()
    #Jon.Update()
    #Billy.Update()
    #Konny.Update()
    #Lonny.Update()
    #Ronny.Update()
