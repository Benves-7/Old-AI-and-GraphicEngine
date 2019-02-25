from time import *
from Vector import *
from math import *

class BaseGameEntityClass():
	m_ID = None
	iNextValidID = 0
	map = None
	window = None

	def SetID(self):
		self.m_ID = BaseGameEntityClass.iNextValidID
		BaseGameEntityClass.iNextValidID += 1

	def Update(self):
		return 0 # FILLER, does nothing so far.

	def ID(self):
		return str(self.m_ID)

	def HandelMessage(self, telegram):
	    return self.FSM.HandelMessage(telegram)

	def BindWindow(map, window):
		BaseGameEntityClass.map = map
		BaseGameEntityClass.window = window

class EntityManager():
	
	entitys = {}

	def RegisterEntity(newEntity):
		EntityManager.entitys[newEntity.id] = newEntity

	def GetEntityFromId(id):
		return EntityManager.entitys[id]

	def RemoveEntity(entityToDel):
		EntityManager.entitys.pop[entityToDel.id]

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

class MovingEntity(BaseGameEntityClass):

	def GoTowards(self):
		
		# walks toward pos, returns whether person is at pos.
		try:
			distX = (self.pos.getCenter().getX() - self.map.grid[self.path[1]].center.getX())
			distY = (self.pos.getCenter().getY() - self.map.grid[self.path[1]].center.getY())
		except :
		    return True


		v = atan2(distY, distX)
		
		dx = -cos(v)*self.speed*self.map.grid[self.path[0]].speed
		dy = -sin(v)*self.speed*self.map.grid[self.path[0]].speed
		
		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		self.pos.move(dx, dy)
		return self.pos.getCenter().getX() ==  self.map.grid[self.path[1]].center.getX() and self.pos.getCenter().getY() == self.map.grid[self.path[1]].center.getY()
