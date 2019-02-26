# not working yet. don't know what i what it to do yet...

class EntityManager():
	
	entitys = {}

	def RegisterEntity(self, newEntity):
		entitys[newEntity.id] = newEntity

	def GetEntityFromId(self, id):
		return entitys[id]

	def RemoveEntity(self, entity):
		self.entitys
