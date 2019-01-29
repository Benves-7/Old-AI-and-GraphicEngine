from BaseGameEntity import *
from State import *
from Positions import *
from Graphics import *

class Miner(BaseGameEntity):
	m_ID = 0
	m_Name = ""
	m_Doing = ""
	m_pCurrentState = State
	m_pPreviousState = State
	m_iSpeed = 2
	m_Location = "Home"
	m_tPos = Position.pos.get(m_Location)
	m_PTpos = Point(m_tPos[0], m_tPos[1])
	m_Text = Text(m_PTpos, m_Name)

	m_iGoldCarried = 0
	m_iMoneyInBank = 0
	m_iThirst = 0
	m_iFatige = 0
	m_iSocial = 0
	m_iHunger = 0


	def __init__(self, name, window, newState, location, goldCarried, moneyInBank, thirst, fatige):
		self.m_Name = name
		BaseGameEntity.SetID(self)
		self.m_gWindow = window
		self.SetState(newState)
		self.m_iGoldCarried = goldCarried
		self.m_iMoneyInBank = moneyInBank
		self.m_iThirst = thirst
		self.m_iFatige = fatige


	def Update(self):
		if self.m_iHunger >= 2000 or self.m_iThirst >= 3000:
			self.ChangeState(Dead)
			self.m_pCurrentState.Execute(self)
			return
		self.m_iThirst += 1
		self.m_iHunger += 1
		self.m_pCurrentState.Execute(self)

	def ChangeState(self, newState):
		self.m_pCurrentState.Exit(self)
		self.m_pCurrentState = newState
		self.m_pCurrentState.Enter(self)

	def SetState(self, newState):
		self.m_pCurrentState = newState

	def ChangeLocation(self, newLocation):
		self.m_Location = newLocation
