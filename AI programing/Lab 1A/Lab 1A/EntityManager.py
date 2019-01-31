class EntityManager:
	EntityDictionary = {}

	def __init__(self):
		pass

	def addEntity(Entity):
		EntityManager.EntityDictionary[Entity.entity_ID] = Entity

	def getEntityFromId(id):
		return EntityManager.EntityDictionary[id]

	def removeEntity(Entity):
		EntityManager.EntityDictionary.pop[Entity.entity_ID]


