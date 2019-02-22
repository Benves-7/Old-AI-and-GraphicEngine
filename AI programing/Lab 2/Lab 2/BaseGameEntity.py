class BaseGameEntityClass():
	m_ID = None
	iNextValidID = 0

	def SetID(self):
		self.m_ID = BaseGameEntityClass.iNextValidID
		BGE.iNextValidID += 1

	def Update(self):
		return 0 # FILLER, does nothing so far.

	def ID(self):
		return str(self.m_ID)

	def HandelMessage(self, telegram):
	    return self.FSM.HandelMessage(telegram)

class EntityManager():
	
	entitys = {}

	def RegisterEntity(newEntity):
		EntityManager.entitys[newEntity.id] = newEntity

	def GetEntityFromId(id):
		return EntityManager.entitys[id]

	def RemoveEntity(entityToDel):
		EntityManager.entitys.pop[entityToDel.id]

from time import *

class MessageDispatcher():
    
	PriorityQ = []
	
	def DispatchMessage(sender, receiver, delay, message):
		senderEntity = EntityManager.GetEntityFromId(sender)
		receiverEntity = EntityManager.GetEntityFromId(receiver)
		telegram = {"header":{"sender" : senderEntity, "reciever": receiverEntity, "DispatchTime": delay}, "message" : message}
		if delay == 0:
			MessageDispatcher.Send(telegram)
		else:
			CurrentTime = time()
			telegram["header"]["DispatchTime"] = CurrentTime + delay
			if MessageDispatcher.PriorityQ.count(telegram) < 1:
				for x in MessageDispatcher.PriorityQ:
					if(x["header"]["DispatchTime"] > telegram["header"]["DispatchTime"]):
						 MessageDispatcher.PriorityQ.insert(MessageDispatcher.PriorityQ.index(x))

	def DispatchDelayedMessage():
		CurrentTime = time()
		while (MessageDispatcher.PriorityQ[0]["header"]["DispatchTime"] < CurrentTime and MessageDispatcher.PriorityQ[0]["header"]["DispatchTime"] > 0):
			telegram = MessageDispatcher.PriorityQ[0]
			MessageDispatcher.Send(telegram)
			MessageDispatcher.PriorityQ.remove(telegram)

	def Send(telegram):
		telegram["header"]["reciever"].HandelMessage(telegram)