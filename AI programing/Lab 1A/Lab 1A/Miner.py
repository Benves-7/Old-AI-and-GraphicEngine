from BaseGameEntity import *
from State import *
from Positions import *
from Graphics import *

class Miner(BaseGameEntity):

	# Id, Name and a current activity.
	m_ID = 0
	m_Name = ""
	m_Doing = ""
	
	# Current- and previous-State
	m_pCurrentState = State
	m_pPreviousState = State
	
	# Used to make miner move between locations.
	m_Location = "Home"
	m_tPos = Position.pos.get(m_Location)	# Tuple (x,y) of the position m_Location.
	m_PTpos = Point(m_tPos[0], m_tPos[1])	# make a graphic point with the position.
	m_Text = Text(m_PTpos, m_Name)			# makes a grapic tect with point and the m_Name.
	m_iSpeed = 2							# the speed of the miner.

	# Variables that is used in AI-decisions.
	m_iGoldCarried	= 0
	m_iMoneyInBank	= 0
	
	m_iFatige		= 0
	m_iHunger		= 0
	m_iThirst		= 0
	m_iSocial		= 0

	m_iFood			= 0
	m_bSpade		= False

	# Needs
	m_bHungry = False
	m_bThirsty = False
	m_bTired = False
	m_bLonely = False
	m_bGotFood = False
	m_bGotMoney = False
	m_bPocketsFull = False

	def __init__(self, name, window, thirst = 0, fatige = 0, hunger = 0, goldCarried = 0, moneyInBank = 0):
		self.m_Name = name
		BaseGameEntity.SetID(self)
		self.m_gWindow = window
		self.SetState(Home())
		self.m_iGoldCarried = goldCarried
		self.m_iMoneyInBank = moneyInBank
		self.m_iThirst = thirst
		self.m_iFatige = fatige
		self.m_iHunger = hunger


	def Update(self):
		if self.m_iHunger >= 2000 or self.m_iThirst >= 3000:
			self.ChangeState(Dead)
			self.m_pCurrentState.Execute(self)
			return
		self.CheckNeeds()
		self.m_iThirst += 1
		self.m_iHunger += 1
		self.m_iSocial += 1
		self.m_pCurrentState.Execute(self)

	def ChangeState(self, newState):
		self.m_pCurrentState.Exit(self)
		self.m_pCurrentState = newState
		self.m_pCurrentState.Enter(self)

	def SetState(self, newState):
		self.m_pCurrentState = newState

	def GoTowards(self):
		# walks toward pos, returns whether person is at pos.
		x = Position.pos.get(self.m_Location)[0]
		y = Position.pos.get(self.m_Location)[1]

		distX = (self.m_tPos[0] - Position.pos.get(self.m_Location)[0])
		distY = (self.m_tPos[1] - Position.pos.get(self.m_Location)[1])
		v = atan2(distY, distX)
		dx = -cos(v)*self.m_iSpeed
		dy = -sin(v)*self.m_iSpeed
		
		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		tPos = None
		tPos = (self.m_tPos[0] + dx, self.m_tPos[1] + dy)
		self.m_tPos = tPos
		self.m_Text.undraw()
		self.m_PTpos = Point(tPos[0], tPos[1])
		self.m_Text = Graphics.Text(self.m_PTpos, self.m_Name)
		self.m_Text.draw(self.m_gWindow)
		
		return self.m_tPos[0] ==  Positions.Position.pos.get(self.m_Location)[0] and self.m_tPos[1] == Positions.Position.pos.get(self.m_Location)[1]

	def CheckNeeds(self):
		if not self.m_bHungry and self.m_iHunger >= 1000:
		    self.m_bHungry = True

		if not self.m_bThirsty and self.m_iThirst >= 2000:
			self.m_bThirsty = True

		if not self.m_bTired and self.m_iFatige >= 800:
		    self.m_bTired = True

		if not self.m_bLonely and self.m_iSocial >= 1500:
			self.m_bLonely = True

		if not self.m_bGotFood and self.m_iFood >= 10:
			self.m_bGotFood = True
		elif self.m_bGotFood and self.m_iFood <= 0:
			self.m_bGotFood = False

		if not self.m_bGotMoney and self.m_iMoneyInBank > 100:
			self.m_bGotMoney = True
		elif self.m_bGotMoney and self.m_iMoneyInBank < 50:
			self.m_bGotMoney = False

		if not self.m_bPocketsFull and self.m_iGoldCarried >= 200:
			self.m_bPocketsFull = True