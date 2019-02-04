from EntityManager import *
from collections import *

class MessageDispatcher:

	def DispatchMessage(sender, receiver, delay, message):
		Ids = EntityManager.EntityDictionary.keys()
		senderEntity = EntityManager.getEntityFromId(sender)
		if receiver == "all":
			for id in Ids:
				if id == sender:
					pass
				else:
					telegram = {"header" : {"sender" : senderEntity, "receiver":EntityManager.getEntityFromId(id),"delay" : delay}, "message" : message}
					MessageDispatcher.send(telegram, EntityManager.getEntityFromId(id))
		else:
			receiverEntity = EntityManager.getEntityFromId(receiver)
			telegram = {"header" : {"sender" : senderEntity, "receiver": receiverEntity, "delay" : delay}, "message" : message}
			MessageDispatcher.send(telegram, receiverEntity)
	def DispatchDelayedMessages():
		return

	def send(telegram, receiver):
		receiver.m_pCurrentState.MessageRecieved(receiver, telegram)

