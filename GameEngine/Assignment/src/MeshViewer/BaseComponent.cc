#pragma once
#include "cJSON.h"
class BaseComponent
{
public:
	BaseComponent();
	~BaseComponent();

	void Update();
	void Shutdown();

private:

};

inline BaseComponent::BaseComponent()
{
}

inline BaseComponent::~BaseComponent()
{
}

inline void BaseComponent::Update()
{
	
}

inline void BaseComponent::Shutdown()
{

}

class GraphicsComponent : public BaseComponent
{
public:
	GraphicsComponent();
	~GraphicsComponent();

private:

};

inline GraphicsComponent::GraphicsComponent()
{

}
inline GraphicsComponent::~GraphicsComponent()
{

}