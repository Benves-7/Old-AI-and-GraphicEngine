import Positions
import time
import os
import Graphics
import BaseGameEntity
from EntityManager import *
from MessageDispatcher import *
from math import *

class State():

	def Enter(self):
		return 0
	def Execute(self):
		return 0
	def Exit(self):
		return 0

	def MessageRecieved(self, message):
		
		#Another agent wants to meet with this agent
		if message["message"]["call"] == "meet":
			#If the agent is lonely enought it will accept the request
			#The agent wants to meet, starts walking to the destination depending on other needs.
			if message["header"]["receiver"].m_iSocial > 1000 and not message["header"]["receiver"].m_bTired:
				print(message["header"]["sender"].m_Name + ": hej " + message["header"]["receiver"].m_Name + " vill du träffas?")
				print(message["header"]["receiver"].m_Name + ": Ja, kanske på resturangen?")
				message["header"]["receiver"].m_Location = "Diner"
				message["header"]["receiver"].ChangeState(Meeting)
				message["header"]["receiver"].m_bGoingToMeeting = True
				message["header"]["receiver"].m_bLonely = True
				#Sends a message to the sender to confirm that the agent wants to meet.
				MessageDispatcher.DispatchMessage(message["header"]["receiver"].m_ID, message["header"]["sender"].m_ID, 0, {"call" : "anwser", "place" : "Diner"})
				return
			else:
				pass


		elif message["message"]["call"] == "anwser":
			if message["header"]["receiver"].m_bGoingToMeeting or message["header"]["receiver"].m_bAtMeeting:
				if not message["header"]["receiver"].m_Location == message["message"]["place"]:
					print(message["header"]["receiver"].m_Name + ": påväg till " + message["header"]["receiver"].m_Location + " för att umgås, kom dit!" )
				MessageDispatcher.DispatchMessage(message["header"]["receiver"].m_ID, message["header"]["sender"].m_ID, 0, {"call" : "correction", "place" : message["header"]["receiver"].m_Location})
				return
			#The other agent want's to meet. Starts walking to the destination.
			message["header"]["receiver"].m_Location = message["message"]["place"]
			message["header"]["receiver"].ChangeState(Meeting)
			message["header"]["receiver"].m_bGoingToMeeting = True
			return

		elif message["message"]["call"] == "correction":
			message["header"]["receiver"].m_Location = message["message"]["place"]
			message["header"]["receiver"].m_bGoingToMeeting = True

		elif message["message"]["call"] == "arrived":
			# Tells the other agent that you have arrived. 
			# If the other agent have arrived, start talking.
		    # Othervise wait until the other agent arrives or 
		    # cancels the meeting or if you the current agent needs to do something else.
			return

		elif message["message"]["call"] == "leaving":
			message["header"]["receiver"].ChangeState(Working)
			return


class Home(State):
	def Exit(self, miner):
		miner.m_Doing = "Leaving Home!"

	def Execute(self, miner):
		miner.ChangeState(Working)

class Meeting(State):

	peopleHere = {}


	def Enter(miner):
		miner.m_Doing = "Moving to " + miner.m_Location + " - Meeting"
		miner.m_bGoingToMeeting = True


	def Execute(miner):
		if miner.GoTowards():
			miner.m_bGoingToMeeting = False
			miner.m_bAtMeeting = True
			if miner.m_ID not in Meeting.peopleHere:
				Meeting.peopleHere[miner.m_ID] = EntityManager.getEntityFromId(miner.m_ID)
			miner.m_Doing = "Meeting friends."
			if len(Meeting.peopleHere) > 1:
				miner.m_iSocial -= 10
			if miner.m_bHungry and miner.m_iHunger - 150 >= 0:
				miner.m_iHunger -= 150
				miner.m_bHungry = False
			if miner.m_bThirsty and miner.m_iThirst - 25 >= 0:
				miner.m_iThirst -= 25
				miner.m_bThirsty = False
			if miner.m_iSocial <= 0:
				miner.m_iSocial = 0
				miner.m_bLonely = False

		if not miner.m_bLonely:
			miner.ChangeState(Working)
			return

	def Exit(miner):
		if miner.m_ID in Meeting.peopleHere:
			Meeting.peopleHere.pop(miner.m_ID)
			if len(Meeting.peopleHere) < 2 and not len(Meeting.peopleHere) == 0:
				i = 0
				peoplehere = list(Meeting.peopleHere.keys())
				for people in peoplehere:
					MessageDispatcher.DispatchMessage(miner.m_ID, Meeting.peopleHere[people].m_ID, 0, {"call" : "leaving"})

				while i < len(Meeting.peopleHere):
					i += 1
		if miner.m_iSocial < 1500:
			miner.m_bLonely = False
		miner.m_bAtMeeting = False
		miner.m_bGoingToMeeting = False


class Working(State):

	def Enter(miner):
		if miner.m_bSpade:
			miner.m_Location = "Mine"
			miner.m_Doing = "Moving to Mine"
		else:
			miner.m_Location = "Field"
			miner.m_Doing = "Moving to Field"

	def Execute(miner):
		if miner.GoTowards():
			if miner.m_bSpade:
				miner.m_Doing = "Mining"
				miner.m_iFatige += 4
				miner.m_iGoldCarried += 5
			else:
				miner.m_Doing = "Working the fields (of golden)"
				miner.m_iFatige += 2
				miner.m_iGoldCarried += 2

		if miner.m_iMoneyInBank >= 700 and not miner.m_bSpade:
			miner.ChangeState(Shopping)
			return 0
		
		if miner.m_bPocketsFull:
			miner.ChangeState(Banking)
			return 0

		if miner.m_bTired and not (miner.m_bHungry or miner.m_bThirsty):
			miner.ChangeState(Sleeping)
			return 0
			
		if miner.m_bThirsty and miner.m_bGotMoney:
			miner.ChangeState(Drinking)
			return 0

		if miner.m_bHungry and miner.m_bGotFood:
			miner.ChangeState(Eating)
			return 0
		elif miner.m_bHungry and not miner.m_bGotFood and miner.m_bGotMoney:
			miner.ChangeState(Shopping)
			return 0

	
	def Exit(miner):
		miner.m_Doing = "Leaving Work!"

class Shopping(State):
	def Enter(miner):
		miner.m_Location = "Store"
		miner.m_Doing = "Moving to Store"

	def Execute(miner):
		if miner.GoTowards():
			if miner.m_bHungry and miner.m_bGotMoney:
				miner.m_iFood += 10
				miner.m_iMoneyInBank -= 75
				miner.ChangeState(Eating)
				return 0

			if not miner.m_bSpade and miner.m_iMoneyInBank > 500:
				miner.m_bSpade = True
				miner.m_iMoneyInBank -= 500
				miner.ChangeState(Working)
				return 0

	def Exit(miner):
		miner.m_Doing = "Leaving Store!"

class Sleeping(State):
	def Enter(miner):
		miner.m_Location = "Home"
		miner.m_Doing = "Moving to Home"

	def Execute(miner):
		if miner.GoTowards():
			miner.m_Doing = "Sleeping (zZz)"
			miner.m_iFatige -= 25

		if miner.m_iFatige <= 0:
			miner.m_iFatige = 0
			miner.m_bTired = False

		if not miner.m_bTired and miner.m_iGoldCarried < 200:
			miner.ChangeState(Working)
			return 0

	def Exit(miner):
		miner.m_Doing = "Leaving Home!"

class Banking(State):
	def Enter(miner):
		miner.m_Location = "Bank"
		miner.m_Doing = "Moving to Bank"

	def Execute(miner):
		if miner.GoTowards():
			miner.m_Doing = "Banking"
			miner.m_iMoneyInBank += miner.m_iGoldCarried
			miner.m_iGoldCarried = 0
			miner.m_bPocketsFull = False
			miner.ChangeState(Working)
			return 0

	def Exit(miner):
		miner.m_Doing = "Leaving Bank!"

class Drinking(State):
	def Enter(miner):
		miner.m_Location = "Bar"
		miner.m_Doing = "Moving to Bar"

	def Execute(miner):
		if miner.GoTowards():
			miner.m_Doing = "Drinking"
			if miner.m_bGotMoney:
				miner.m_iThirst -= 25
				miner.m_iMoneyInBank -= 10
			if miner.m_iThirst <= 0:
				miner.m_iThirst = 0
				miner.m_bThirsty = False

		if not miner.m_bThirsty:
			miner.ChangeState(Working)
			return 0
		if not miner.m_bGotMoney:
			miner.ChangeState(Working)
			return 0

	def Exit(miner):
		miner.m_Doing = "Leaving Bar!"

class Eating(State):
	def Enter(miner):
		miner.m_Location = "Home"
		miner.m_Doing = "Moving to Home"

	def Execute(miner):
		if miner.GoTowards():
			miner.m_Doing = "Eating"
			if miner.m_bGotFood:
				miner.m_iHunger -= 150
				miner.m_iFood -= 1

		if miner.m_iHunger <= 0:
			miner.m_iHunger = 0
			miner.m_bHungry = False

		if not miner.m_bHungry:
			miner.ChangeState(Working)
			return 0

		if not miner.m_bGotFood:
			miner.ChangeState(Working)
			return 0

	def Exit(miner):
		miner.m_Doing = "Leaving Home"

class Dead(State):
	def Enter(miner):
		print(miner.m_Name + ": dead!")
		miner.m_Location = "Ground"
		miner.m_Doing = "Dying"

	def Execute(miner):
		miner.m_Doing = "Dying"

	def Exit(miner):
		miner.m_Doint = "Dying"