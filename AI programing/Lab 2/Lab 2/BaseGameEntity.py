from time import *
from Vector import *
from math import *
from JsonLoader import *
import Entitys

class BaseGameEntityClass():
	iNextValidID = 0
	map = None
	window = None
	data = None
	townHall = None

	def SetID(self):
		self.id = BaseGameEntityClass.iNextValidID
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
		BaseGameEntityClass.data = JsonLoader.Data["entitys"]

	def PlaceStatic():
		for node in BaseGameEntityClass.map.grid:
			if node.isSpawn:
				BaseGameEntityClass.townHall = Entitys.TownHall(node.id)
			if node.numTrees > 0:
				for x in range(0, node.numTrees):
					tree = Entitys.Tree(x, node.id)
					node.trees.append(tree)

class EntityManager():
	
	entitys = {}

	explorers = []
	workers = []

	def RegisterEntity(newEntity):
		EntityManager.entitys[newEntity.id] = newEntity

	def GetEntityFromId(id):
		return EntityManager.entitys[id]

	def RemoveEntity(entity):
		try:
			del EntityManager.entitys[entity.id]
		except :
		    print("error - entity not found for delete")

	def add_list(explorers, workers):
		EntityManager.explorers = explorers
		EntityManager.workers = workers

	def Del(id):
		EntityManager.explorers.remove(EntityManager.GetEntityFromId(id))

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
			distX = (self.circle.getCenter().getX() - self.map.grid[self.path[0]].center.getX())
			distY = (self.circle.getCenter().getY() - self.map.grid[self.path[0]].center.getY())
		except :
		    return False


		v = atan2(distY, distX)
		
		dx = -cos(v)*self.speed*self.map.grid[self.path[0]].speed
		dy = -sin(v)*self.speed*self.map.grid[self.path[0]].speed
		
		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		self.circle.move(dx, dy)
		try:
			self.searchRectangel.move(dx, dy)
		except :
		    pass
		return self.circle.getCenter().getX() ==  self.map.grid[self.path[0]].center.getX() and self.circle.getCenter().getY() == self.map.grid[self.path[0]].center.getY()

class StaticEntity(BaseGameEntityClass):
	def function(args):
		pass