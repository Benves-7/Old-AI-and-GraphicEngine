#pragma once
#include "cJSON.h"
#include <fstream>
#include <iostream>
#include "Core/Containers/Array.h"
#include "Modules/Gfx/GfxTypes.h"
#include "Gfx/Gfx.h"
#include "Assets/Gfx/MeshLoader.h"
#include "glm/mat4x4.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtx/polar_coordinates.hpp"
#include "glm/gtx/transform.hpp"
#include "shaders.h"

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


class GraphicsManager
{
public:
	GraphicsManager();
	~GraphicsManager();

	void Init();

	static Oryol::Array<ModelMesh> models;

private:

};

inline GraphicsManager::GraphicsManager()
{
}

inline GraphicsManager::~GraphicsManager()
{
}

inline void GraphicsManager::Init()
{
	std::ifstream ifs("D:/GIT/D0012D/GameEngine/Assignment/src/MeshViewer/config.json");
	bool test = ifs.good();
	std::string content((std::istreambuf_iterator<char>(ifs)), (std::istreambuf_iterator<char>()));
	std::printf(content.c_str(),"\n");
	cJSON *json = cJSON_Parse(content.c_str());

	cJSON * graphicsEntities = cJSON_GetObjectItem(json, "graphicsEntities");
	for (int i = 0; i < cJSON_GetArraySize(graphicsEntities);  i++)
	{
		cJSON *entity = cJSON_GetArrayItem(graphicsEntities, i);
		char* name = cJSON_GetObjectItem(entity, "name")->valuestring;
		char* path = cJSON_GetObjectItem(entity, "path")->valuestring;
		char* shader = cJSON_GetObjectItem(entity, "shader")->valuestring;
		cJSON*  material = cJSON_GetObjectItem(entity, "material");
		cJSON* diff = cJSON_GetObjectItem(material, "diffuse");
		cJSON* spec = cJSON_GetObjectItem(material, "specular");
		glm::vec4 diffuse = glm::vec4(cJSON_GetArrayItem(diff, 0)->valuedouble, cJSON_GetArrayItem(diff, 1)->valuedouble, cJSON_GetArrayItem(diff, 2)->valuedouble, cJSON_GetArrayItem(diff, 3)->valuedouble);
		glm::vec4 specular = glm::vec4(cJSON_GetArrayItem(spec, 0)->valuedouble, cJSON_GetArrayItem(spec, 1)->valuedouble, cJSON_GetArrayItem(spec, 2)->valuedouble, cJSON_GetArrayItem(spec, 3)->valuedouble);
		float specularPower = (float)cJSON_GetObjectItem(material, "specularPower")->valuedouble;

		ModelMesh &object = GraphicsManager::models.Add(ModelMesh());

		object.curMeshIndex = i;
		object.material.diffuse = diffuse;
		object.transform = glm::translate(glm::mat4(), glm::vec3(0,0,0));
		object.transformvec3 = glm::vec3(0,0,0);

		object.drawstate.Mesh[0] = Oryol::Gfx::LoadResource(Oryol::MeshLoader::Create(Oryol::MeshSetup::FromFile(path), [&object](Oryol::MeshSetup& setup)
		{
			auto ps = Oryol::PipelineSetup::FromLayoutAndShader(setup.Layout, Oryol::Gfx::CreateResource(PhongShader::Setup()));
			ps.DepthStencilState.DepthWriteEnabled = true;
			ps.DepthStencilState.DepthCmpFunc = Oryol::CompareFunc::LessEqual;
			ps.RasterizerState.CullFaceEnabled = true;
			ps.RasterizerState.SampleCount = 4;
			object.numMaterials = setup.NumPrimitiveGroups();
			object.drawstate.Pipeline = Oryol::Gfx::CreateResource(ps);
		}));
	}

}