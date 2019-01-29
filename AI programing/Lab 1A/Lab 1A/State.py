import Positions
import time
import os
import Graphics
from math import *

#Bilip was here (:

class State():
    
    def Enter(self):
        return 0
    def Execute(self):
        return 0
    def Exit(self):
        return 0

def GoTowards(miner, pos):
    # walks toward pos, returns whether person is at pos.
	distX = miner.m_tPos[0] - Positions.Position.pos.get(pos)[0]
	distY = miner.m_tPos[1] - Positions.Position.pos.get(pos)[1]
	v = atan2(distX, distY)
	dx = -cos(v)*miner.m_iSpeed
	dy = -sin(v)*miner.m_iSpeed

	if abs(dx) > abs(distX):
		dx = -distX
	if abs(dy) > abs(distY):
		dy = -distY

	tPos = (miner.m_tPos[0] + dx, miner.m_tPos[1] + dy)
	miner.m_tPos = tPos
	miner.m_Text.undraw()
	miner.m_PTpos.move(dx,dy)
	miner.m_Text = Graphics.Text(miner.m_PTpos, miner.m_Name)
	miner.m_Text.draw(miner.m_gWindow)
	if miner.m_tPos[0] ==  Positions.Position.pos.get(pos)[0] and miner.m_tPos[1] == Positions.Position.pos.get(pos)[1]:
		return True
	else:
		return False

class Home(State):
    def Exit(self, miner):
        miner.m_Doing = "Leaving Home!"

    def Execute(self, miner):
        miner.ChangeState(Working)

class Working(State):

	def Enter(miner):
		miner.m_Location = "Mine"
		miner.m_Doing = "Moving to Mine"

	def Execute(miner):
		if GoTowards(miner, miner.m_Location):
			miner.m_Doing = "Mining"
			miner.m_iFatige += 5
			miner.m_iGoldCarried += 2

		if miner.m_iGoldCarried >= 200:
			miner.ChangeState(Banking)

		if miner.m_iFatige >= 1000:
			miner.ChangeState(Sleeping)
			
		if miner.m_iThirst >= 2000:
			miner.ChangeState(Drinking)

		if miner.m_iHunger >= 1000:
			miner.ChangeState(Eating)
	
	def Exit(miner):
		miner.m_Doing = "Leaving Mine!"

class Sleeping(State):
	def Enter(miner):
		miner.m_Location = "Home"
		miner.m_Doing = "Moving to Home"

	def Execute(miner):
		if GoTowards(miner, miner.m_Location):
			miner.m_Doing = "Sleeping (zZz)"
			miner.m_iFatige -= 25

		if miner.m_iFatige <= 0:
			miner.m_iFatige = 0

		if miner.m_iFatige == 0 and miner.m_iGoldCarried < 200:
			miner.ChangeState(Working)
		if miner.m_iFatige == 0 and miner.m_iGoldCarried >= 200:
			miner.ChangeState(Banking)

	def Exit(miner):
		miner.m_Doing = "Leaving Home!"

class Banking(State):
	def Enter(miner):
		miner.m_Location = "Bank"
		miner.m_Doing = "Moving to Bank"

	def Execute(miner):
		if GoTowards(miner, miner.m_Location):
			miner.m_Doing = "Banking"
			miner.m_iMoneyInBank += miner.m_iGoldCarried
			miner.m_iGoldCarried = 0
			miner.ChangeState(Working)

	def Exit(miner):
		miner.m_Doing = "Leaving Bank!"

class Drinking(State):
	def Enter(miner):
		miner.m_Location = "Bar"
		miner.m_Doing = "Moving to Bar"

	def Execute(miner):
		if GoTowards(miner, miner.m_Location):
			miner.m_Doing = "Drinking"
			if miner.m_iMoneyInBank - 1 >= 0:
				miner.m_iThirst -= 25
				miner.m_iMoneyInBank -= 10
			if miner.m_iThirst < 0:
				miner.m_iThirst = 0
		if miner.m_iThirst == 0 and miner.m_iGoldCarried < 100:
			miner.ChangeState(Working)
		if miner.m_iThirst == 0 and miner.m_iGoldCarried >= 100:
			miner.ChangeState(Banking)
		if miner.m_iMoneyInBank <= 0:
			miner.ChangeState(Working)

	def Exit(miner):
		miner.m_Doing = "Leaving Bar!"

class Eating(State):
	def Enter(miner):
		miner.m_Location = "Home"
		miner.m_Doing = "Moving to Home"

	def Execute(miner):
		if GoTowards(miner, miner.m_Location):
			miner.m_Doing = "Eating"
			if miner.m_iMoneyInBank - 5 >= 0:
				miner.m_iHunger -= 50
				miner.m_iThirst -= 10
				miner.m_iMoneyInBank -= 5

		if miner.m_iHunger <= 0:
			miner.m_iHunger = 0
			miner.ChangeState(Working)

	def Exit(miner):
		miner.m_Doing = "Leaving Home"

class Dead(State):
    def Enter(miner):
        miner.m_Location = "Ground"
        miner.m_Doing = "Dying"

    def Execute(miner):
        miner.m_Doing = "Dying"

    def Exit(miner):
        miner.m_Doint = "Dying"