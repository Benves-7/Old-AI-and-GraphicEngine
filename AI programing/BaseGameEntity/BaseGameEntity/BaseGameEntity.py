import State

class BaseGameEntity:
    m_ID = None
    iNextValidID = 0

    def __init__(self, id):
        SetID(id)
        
    def SetID(self, id):
        if id >= BaseGameEntity.iNextValidID:
            BaseGameEntity.iNextValidID = id
        self.m_ID = BaseGameEntity.iNextValidID
        BaseGameEntity.iNextValidID += 1

    def Update(self):
        return 0 # FILLER, does nothing so far.

    def ID(self):
        return str(self.m_ID)

class Miner(BaseGameEntity):
    m_ID = 0
    m_Name = ""
    m_Doing = ""
    m_pCurrentState = State.Home
    m_Location = "Mine"
    m_iGoldCarried = 0
    m_iMoneyInBank = 0
    m_iThirst = 0
    m_iFatige = 0


    def __init__(self, name, id, newState, location, goldCarried, moneyInBank, thirst, fatige):
        self.m_Name = name
        BaseGameEntity.SetID(self, id)
        self.SetState(newState)
        self.m_iGoldCarried = goldCarried
        self.m_iMoneyInBank = moneyInBank
        self.m_iThirst = thirst
        self.m_iFatige = fatige

    def Update(self):
        self.m_iThirst += 1
        self.m_pCurrentState.Execute(self)
    
    def ChangeState(self, newState):
        self.m_pCurrentState.Exit()
        self.m_pCurrentState = newState
        self.m_pCurrentState.Enter(self)

    def SetState(self, newState):
        self.m_pCurrentState = newState

    def ChangeLocation(self, newLocation):
        self.m_Location = newLocation