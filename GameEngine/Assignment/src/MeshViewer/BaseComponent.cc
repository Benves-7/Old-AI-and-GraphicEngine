#pragma once
#include "glm/mat4x4.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtx/polar_coordinates.hpp"
#include "glm/gtx/transform.hpp"
#include "Modules/Gfx/GfxTypes.h"

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

struct ModelMesh
{
	int curMeshIndex;
	glm::mat4 transform;
	glm::vec3 transformvec3;
	Oryol::DrawState drawstate;
	int numMaterials;
	enum {
		Normals = 0,
		Lambert,
		Phong
	};
	struct Material {
		int shaderIndex = Phong;
		Oryol::Id pipeline;
		glm::vec4 diffuse = glm::vec4(0.0f, 0.24f, 0.64f, 1.0f);
		glm::vec4 specular = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
		float specPower = 32.0f;
	} material;
};

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