class BaseGameEntity:
    m_ID = None
    iNextValidID = 0

    def __init__(self, id):
        SetID(id)
        
    def SetID(self):
        self.m_ID = BaseGameEntity.iNextValidID
        BaseGameEntity.iNextValidID += 1

    def Update(self):
        return 0 # FILLER, does nothing so far.

    def ID(self):
        return str(self.m_ID)
