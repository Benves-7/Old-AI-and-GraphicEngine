import BaseGameEntity
import State

class Miner(BaseGameEntity.BaseGameEntity):
    m_ID = 0
    m_Name = ""
    m_Doing = ""
    m_pCurrentState = State.State
    m_pPreviousState = State.State
    m_Location = "Mine"
    m_iGoldCarried = 0
    m_iMoneyInBank = 0
    m_iThirst = 0
    m_iFatige = 0
    m_iSocial = 0
    m_iHunger = 0


    def __init__(self, name, id, newState, location, goldCarried, moneyInBank, thirst, fatige):
        self.m_Name = name
        BaseGameEntity.BaseGameEntity.SetID(self, id)
        self.SetState(newState)
        self.m_iGoldCarried = goldCarried
        self.m_iMoneyInBank = moneyInBank
        self.m_iThirst = thirst
        self.m_iFatige = fatige

    def Update(self):
        self.m_iThirst += 1
        self.m_iHunger += 1
        if self.m_iThirst >= 25 or self.m_iThirst >= 45:
            self.ChangeState(State.Dead)
        self.m_pCurrentState.Execute(self)
    
    def ChangeState(self, newState):
        self.m_pCurrentState.Exit(self)
        self.m_pCurrentState = newState
        self.m_pCurrentState.Enter(self)

    def SetState(self, newState):
        self.m_pCurrentState = newState

    def ChangeLocation(self, newLocation):
        self.m_Location = newLocation