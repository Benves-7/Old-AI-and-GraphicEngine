#pragma once
#include "BaseComponent.cc"
#include "Core/Containers/Array.h"

class GameEntity
{
public:
	GameEntity();
	~GameEntity();
	
	void Init();
	void UpdateComponents();
	void ShutdownComponents();
	static Oryol::Array<BaseComponent> components;

private:


};


inline GameEntity::GameEntity()
{
}

inline GameEntity::~GameEntity()
{
}

inline void GameEntity::Init()
{
	BaseComponent &component = GameEntity::components.Add(GraphicsComponent());
	component.Update();
}

inline void GameEntity::UpdateComponents()
{
	for (int i = 0; i < GameEntity::components.Size(); i++)
	{
		GameEntity::components[i].Update();
	}
}

inline void GameEntity::ShutdownComponents()
{
	for (int i = 0; i < GameEntity::components.Size(); i++)
	{
		GameEntity::components[i].Shutdown();
	}
}