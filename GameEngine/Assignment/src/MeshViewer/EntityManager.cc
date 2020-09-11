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

	Oryol::Array<GameEntity> entitys;

private:

};
Oryol::Array<BaseComponent> GameEntity::components;

inline EntityManager::EntityManager()
{
}

inline EntityManager::~EntityManager()
{
}

inline void EntityManager::Init()
{
	GameEntity &newEntity = this->entitys.Add(GameEntity());
	newEntity.Init();
}

inline void EntityManager::Update()
{

}

inline void EntityManager::Shutdown()
{

}