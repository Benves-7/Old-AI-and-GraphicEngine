from EntityManager import *
from collections import *

class MessageDispatcher:

	def __init__(self):
		pass

	def DispatchMessage(sender, receiver, delay, message):

		Entity = EntityManager.getEntityFromId(receiver)
		senderEntity = EntityManager.getEntityFromId(sender)

		telegram = {"header" : {"sender" : senderEntity, "receiver": Entity, "delay" : delay}, "message" : message}

		MessageDispatcher.send(telegram, Entity)

	def DispatchDelayedMessages():
		return

	def send(telegram, receiver):
		receiver.receiveMessage(telegram)
