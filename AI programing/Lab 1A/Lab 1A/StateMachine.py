import Miner
import State

class StateMachine:
    
    #a pointer to the agent that owns this instance
    m_pOwner = Miner.Miner
    m_pCurrentState = State.State

    #a recort of the last state the agent was in
    m_pPreviousState = State.State

    #this state logic is called every time the FSM is updated
    m_pGlobalState = State.State

    def __init__(self, miner):
        self.m_pOwner = miner
        self.m_pCurrentState = miner.m_pCurrentState
        self.m_pPreviousState = miner.m_pPreviousState

