import time
import os

class State():
    
    def Enter(self):
        assert 0, "Error in Enter"
    def Execute(self):
        assert 0, "Error in Execute"
    def Exit(self):
        assert 0, "Error in Exit"

class Home(State):
    def Exit(self, miner):
        miner.m_Doing = "Leaving Home!"

    def Execute(self, miner):
        miner.ChangeState(Working)

class Working(State):

    def Enter(miner):
        miner.m_Doing = "Moving"
        miner.ChangeLocation("Mine")

    def Execute(miner):
        miner.m_Doing = "Mining"
        miner.m_iFatige += 5
        miner.m_iGoldCarried += 2

        if miner.m_iGoldCarried >= 10:
            miner.ChangeState(Banking)

        if miner.m_iFatige >= 40:
            miner.ChangeState(Sleeping)

        if miner.m_iThirst >= 40:
            miner.ChangeState(Drinking)

        if miner.m_iHunger >= 20:
            miner.ChangeState(Eating)

    def Exit(miner):
        miner.m_Doing = "Leaving Mine!"

class Sleeping(State):
    def Enter(miner):
        miner.m_Doing = "Moving"
        miner.ChangeLocation("Home")

    def Execute(miner):
        miner.m_Doing = "Sleeping (zZz)"
        miner.m_iFatige -= 10
        if miner.m_iFatige <= 0:
            miner.m_iFatige = 0

        if miner.m_iFatige == 0 and miner.m_iGoldCarried < 10:
            miner.ChangeState(Working)
        if miner.m_iFatige == 0 and miner.m_iGoldCarried >= 10:
            miner.ChangeState(Banking)

    def Exit(miner):
        miner.m_Doing = "Leaving Home!"

class Banking(State):
    def Enter(miner):
        miner.m_Doing = "Moving"
        miner.ChangeLocation("Bank")

    def Execute(miner):
        miner.m_Doing = "Banking"
        miner.m_iMoneyInBank += miner.m_iGoldCarried
        miner.m_iGoldCarried = 0

        miner.ChangeState(Working)

    def Exit(miner):
        miner.m_Doing = "Leaving Bank!"

class Drinking(State):
    def Enter(miner):
        miner.m_Doing = "Moving"
        miner.ChangeLocation("Bar")

    def Execute(miner):
        miner.m_Doing = "Drinking"
        if miner.m_iMoneyInBank - 1 >= 0:
            miner.m_iThirst -= 10
            miner.m_iMoneyInBank -= 1
        if miner.m_iThirst < 0:
            miner.m_iThirst = 0
        if miner.m_iThirst == 0 and miner.m_iGoldCarried < 10:
            miner.ChangeState(Working)
        if miner.m_iThirst == 0 and miner.m_iGoldCarried >= 10:
            miner.ChangeState(Banking)
        if miner.m_iMoneyInBank <= 0:
            miner.ChangeState(Working)

    def Exit(miner):
        miner.m_Doing = "Leaving Bar!"

class Eating(State):
    def Enter(miner):
        miner.m_Doing = "Moving"
        miner.ChangeLocation("Home")

    def Execute(miner):
        miner.m_Doing = "Eating"
        if miner.m_iMoneyInBank - 4 >= 0:
            miner.m_iHunger -= 5
            miner.m_iThirst -= 1
            miner.m_iMoneyInBank -= 4

        if miner.m_iHunger <= 0:
            miner.m_iHunger = 0
            miner.ChangeState(Working)
        if miner.m_iMoneyInBank <= 3:
            miner.ChangeState(Working)

    def Exit(miner):
        miner.m_Doing = "Leaving Home"

class Dead(State):
    def Enter(miner):
        miner.m_Doing = "Collapsing"
        miner.ChangeLocation("Ground")

    def Execute(miner):
        miner.m_Doing = "Dying"

    def Exit(miner):
        miner.m_Doint = "Dying"
#class Citylife(State):

#class Buying(State):
