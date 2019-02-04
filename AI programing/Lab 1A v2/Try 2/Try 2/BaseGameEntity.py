class BGE:
    m_ID = None
    iNextValidID = 0
        
    def SetID(self):
        self.m_ID = BGE.iNextValidID
        BGE.iNextValidID += 1

    def Update(self):
        return 0 # FILLER, does nothing so far.

    def ID(self):
        return str(self.m_ID)
