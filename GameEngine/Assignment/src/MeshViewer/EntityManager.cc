#pragma once
#include "Core/Containers/Array.h"
#include "GameEntity.cc"

class EntityManager
{
public:
	EntityManager();
	~EntityManager();
	void Update();
	void Shutdown();
	void Init();

	static Oryol::Array<GameEntity> entitys;

private:

};

inline EntityManager::EntityManager()
{
}

inline EntityManager::~EntityManager()
{
}

inline void EntityManager::Init()
{
	GameEntity &newEntity = EntityManager::entitys.Add(GameEntity());
	newEntity.Init();
}

inline void EntityManager::Update()
{

}

inline void EntityManager::Shutdown()
{

}