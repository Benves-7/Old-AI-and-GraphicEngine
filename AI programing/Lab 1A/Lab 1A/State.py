import time
import os

class State():
    
    def Enter(self):
        assert 0, "Error in Enter"
    def Execute(self):
        assert 0, "Error in Execute"
    def Exit(self):
        assert 0, "Error in Exit"

class Working(State):

    def Enter(miner):
        print("Entering Mine")
        miner.ChangeLocation("Mine")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

    def Execute(miner):
        miner.m_iFatige += 5
        miner.m_iGoldCarried += 1

        if miner.m_iGoldCarried >= 10:
            miner.ChangeState(Banking)

        if miner.m_iFatige >= 40:
            miner.ChangeState(Sleeping)

        if miner.m_iThirst >= 40:
            miner.ChangeState(Drinking)

    def Exit():
        miner.m_Doing = "Leaving Mine!"

class Sleeping(State):
    def Enter(miner):
        miner.m_Doing = "Entering Home"
        miner.ChangeLocation("Home")

    def Execute(miner):
        miner.m_iFatige -= 10
        if miner.m_iFatige <= 0:
            miner.m_iFatige = 0

        if miner.m_iFatige == 0 and miner.m_iGoldCarried < 10:
            clear = lambda: os.system('cls')
            clear()
            miner.ChangeState(Working)

    def Exit():
        miner.m_Doing = "Leaving Home!"
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

class Banking(State):
    def Enter(miner):
        print("Entering Bank")
        miner.ChangeLocation("Bank")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

    def Execute(miner):
        print(miner.m_Name + " stats:")
        print("Gold -> Money:   " + str(miner.m_iGoldCarried) + " -> " + str(miner.m_iMoneyInBank))
        miner.m_iMoneyInBank += miner.m_iGoldCarried
        miner.m_iGoldCarried = 0
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print(miner.m_Name + " stats:")
        print("Gold -> Money:   " + str(miner.m_iGoldCarried) + " -> " + str(miner.m_iMoneyInBank))
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        miner.ChangeState(Working)

    def Exit():
        print("Leaving Bank!")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

class Drinking(State):
    def Enter(self):
        print("Entering Bar")
        miner.ChangeLocation("Bar")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

    def Execute(self):
        return 0

    def Exit(self):
        print("Leaving Bank!")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()

class Home(State):
    def Exit(self):
        print("Leaving Home!")
        time.sleep(2)
        clear = lambda: os.system('cls')
        clear()
    def Execute(self, miner):
        miner.ChangeState(Working)

#class Citylife(State):

#class Buying(State):
