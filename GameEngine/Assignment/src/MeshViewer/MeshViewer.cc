//-----------------------------------------------------------------------------
//  MeshViewer.cc
//-----------------------------------------------------------------------------
#pragma once
#pragma warning(disable:4996)
#include "Pre.h"
#include "Core/Main.h"
#include "Core/String/StringBuilder.h"
#include "Gfx/Gfx.h"
#include "IO/IO.h"
#include "IMUI/IMUI.h"
#include "Input/Input.h"
#include "HttpFS/HTTPFileSystem.h"
#include "LocalFS/LocalFileSystem.h"
#include "Assets/Gfx/MeshLoader.h"
#include "glm/mat4x4.hpp"
#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtx/polar_coordinates.hpp"
#include "glm/gtx/transform.hpp"
#include "shaders.h"
#include "pybind11/pybind11.h"
#include "pybind11/embed.h"
#include "Python.h"


//#include "EntityManager.cc"
#include "GraphicsManager.cc"

using namespace Oryol;
namespace py = pybind11;
//struct ModelMesh
//{
//	int curMeshIndex;
//	glm::mat4 transform;
//	glm::vec3 transformvec3;
//	DrawState drawstate;
//	int numMaterials;
//	enum {
//		Normals = 0,
//		Lambert,
//		Phong
//	};
//	struct Material {
//		int shaderIndex = Phong;
//		Id pipeline;
//		glm::vec4 diffuse = glm::vec4(0.0f, 0.24f, 0.64f, 1.0f);
//		glm::vec4 specular = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
//		float specPower = 32.0f;
//	} material;
//};

class MeshViewerApp : public App {
public:
    AppState::Code OnInit();
    AppState::Code OnRunning();
    AppState::Code OnCleanup();
	// own funk
	static void CreateObject(int curMeshIndex, glm::vec3 transform, glm::vec4 color);
	static void MakeDrawStates();
	static void setPosition(int index, glm::vec3 transform);
	void TryAgain(ModelMesh &object);
	void ChangeMesh(int curMeshIndex);
	static Array<ModelMesh> models;
	static Array<DrawState> drawStates;
    static int numMaterials;
	//EntityManager manager;
	GraphicsManager graphics;


private:
    void handleInput();
    void updateCamera();
    void updateLight();
    void drawUI();
    void applyVariables(int materialIndex);

    int frameCount = 0;
    ResourceLabel curMeshLabel;
    MeshSetup curMeshSetup;
    Id mesh;

    glm::vec3 eyePos;
    glm::mat4 view;
    glm::mat4 proj;
    glm::mat4 model;
    glm::mat4 modelViewProj;

	int selectedID = 0;
	int numWantedInstances;
	int MaxNumInstances = 10;
    int curMeshIndex = 0;
	int numOfShape = 2;

    static const int numMeshes = 3;
    static const char* meshNames[numMeshes];
    static const char* meshPaths[numMeshes];
    static const int numShaders = 3;
    static const char* shaderNames[numShaders];
    enum {
        Normals = 0,
        Lambert,
        Phong
    };
    Id shaders[numShaders];
    ResourceLabel curMaterialLabel;
    struct Material {
        int shaderIndex = Phong;
        Id pipeline;
        glm::vec4 diffuse = glm::vec4(0.0f, 0.24f, 0.64f, 1.0f);
        glm::vec4 specular = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
        float specPower = 32.0f;
    } materials[GfxConfig::MaxNumPrimGroups];
    bool gammaCorrect = true;

    struct CameraSetting {
        float dist = 8.0f;
        glm::vec2 orbital = glm::vec2(glm::radians(25.0f), 0.0f);
        float height = 1.0f;
        glm::vec2 startOrbital;
        float startDistance = 0.0f;
    } camera;
    bool camAutoOrbit = false;
    struct CameraSetting cameraSettings[numMeshes];

    glm::vec2 lightOrbital = glm::vec2(glm::radians(25.0f), 0.0f);
    glm::vec3 lightDir;
    glm::vec4 lightColor = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
    float lightIntensity = 1.0f;
    bool lightAutoOrbit = false;
    bool dragging = false;

    StringBuilder strBuilder;

    const float minCamDist = 0.5f;
    const float maxCamDist = 20.0f;
    const float minLatitude = -85.0f;
    const float maxLatitude = 85.0f;
    const float minCamHeight = -2.0f;
    const float maxCamHeight = 5.0f;
};
Array<ModelMesh> MeshViewerApp::models;
Array<ModelMesh> GraphicsManager::models;
Array<DrawState> MeshViewerApp::drawStates;
int MeshViewerApp::numMaterials;

OryolMain(MeshViewerApp);

const char* MeshViewerApp::meshNames[numMeshes] = {
    "Tiger",
    "Blitz",
    "Teapot"
};
const char* MeshViewerApp::meshPaths[numMeshes] = {
    "root:tiger.omsh.txt",
    "root:opelblitz.omsh.txt",
    "root:teapot.omsh.txt"
};

const char* MeshViewerApp::shaderNames[numShaders] = {
    "Normals",
    "Lambert",
    "Phong"
};

int Add(int i, int j)
{
	return i + j;
}
PYBIND11_EMBEDDED_MODULE(scripting, m)
{
	py::class_<glm::vec3>(m, "vec3")
		.def(py::init<float, float, float>());
	py::class_ < glm::vec4 >(m, "vec4")
		.def(py::init<float, float, float, float>());


	m.def("createModel", &MeshViewerApp::CreateObject, py::return_value_policy::reference);
	m.def("setPosition", &MeshViewerApp::setPosition, py::return_value_policy::reference);

}

//-----------------------------------------------------------------------------
AppState::Code
MeshViewerApp::OnInit() {

	AllocConsole();
	std::freopen("conin$", "r", stdin);
	std::freopen("conout$", "w", stdout);
	std::freopen("conout$", "w", stderr);
	std::printf("Debugging Window:\n");

	py::initialize_interpreter();
    // setup IO system
    IOSetup ioSetup;
	ioSetup.FileSystems.Add("file", LocalFileSystem::Creator());
    IO::Setup(ioSetup);

	//manager.Init();
	graphics.Init();


    // setup rendering and input system
    auto gfxSetup = GfxSetup::WindowMSAA4(800, 512, "Oryol Mesh Viewer");
    gfxSetup.HighDPI = true;
    gfxSetup.DefaultPassAction = PassAction::Clear(glm::vec4(0.5f, 0.5f, 0.5f, 1.0f));
    Gfx::Setup(gfxSetup);
    Input::Setup();
    Input::SetPointerLockHandler([this] (const InputEvent& event) -> PointerLockMode::Code {
        if (event.Button == MouseButton::Left) {
            if (event.Type == InputEvent::MouseButtonDown) {
                if (!ImGui::IsMouseHoveringAnyWindow()) {
                    this->dragging = true;
                    return PointerLockMode::Enable;
                }
            }
            else if (event.Type == InputEvent::MouseButtonUp) {
                if (this->dragging) {
                    this->dragging = false;
                    return PointerLockMode::Disable;
                }
            }
        }
        return PointerLockMode::DontCare;
    });

    // setup IMUI ui system
    IMUI::Setup();
    ImGuiStyle& style = ImGui::GetStyle();
    style.WindowRounding = 0.0f;
    style.TouchExtraPadding.x = 5.0f;
    style.TouchExtraPadding.y = 5.0f;
    ImVec4 defaultBlue(0.0f, 0.5f, 1.0f, 0.7f);
    style.Colors[ImGuiCol_TitleBg] = defaultBlue;
    style.Colors[ImGuiCol_TitleBgCollapsed] = defaultBlue;
    style.Colors[ImGuiCol_SliderGrab] = defaultBlue;
    style.Colors[ImGuiCol_SliderGrabActive] = defaultBlue;
    style.Colors[ImGuiCol_Button] = defaultBlue;
    style.Colors[ImGuiCol_ButtonHovered] = ImVec4(0.0f, 0.5f, 1.0f, 0.3f);
    style.Colors[ImGuiCol_ButtonActive] = ImVec4(0.0f, 0.5f, 1.0f, 1.0f);
    style.Colors[ImGuiCol_ScrollbarGrab] = ImVec4(0.0f, 0.5f, 1.0f, 0.5f);
    style.Colors[ImGuiCol_ScrollbarGrabActive] = ImVec4(0.0f, 0.5f, 1.0f, 1.0f);
    style.Colors[ImGuiCol_ScrollbarGrabHovered] = ImVec4(0.0f, 0.5f, 1.0f, 0.3f);
    style.Colors[ImGuiCol_Header] = defaultBlue;
    style.Colors[ImGuiCol_HeaderHovered] = defaultBlue;
    style.Colors[ImGuiCol_HeaderActive] = defaultBlue;

    this->shaders[Normals] = Gfx::CreateResource(NormalsShader::Setup());
    this->shaders[Lambert] = Gfx::CreateResource(LambertShader::Setup());
    this->shaders[Phong]   = Gfx::CreateResource(PhongShader::Setup());

    // setup projection and view matrices
    const float fbWidth = (const float) Gfx::DisplayAttrs().FramebufferWidth;
    const float fbHeight = (const float) Gfx::DisplayAttrs().FramebufferHeight;
    this->proj = glm::perspectiveFov(glm::radians(60.0f), fbWidth, fbHeight, 0.01f, 100.0f);

    // non-standard camera settings when switching objects
    // teapot:
    this->cameraSettings[2].dist = 0.8f;
    this->cameraSettings[2].height = 0.0f;

	try
	{
		py::exec(R"(
			from scripting import *

			createModel(0, vec3(0, 0, 0), vec4(0, 255, 0, 0))
			createModel(0, vec3(4, 0, 0), vec4(0, 0, 255, 0))

			)");
	}
	catch (const std::exception e)
	{
		fprintf(stderr, "%s/n", e.what());
	}
    return App::OnInit();
}

//-----------------------------------------------------------------------------
AppState::Code
MeshViewerApp::OnRunning() {

    this->frameCount++;
    this->handleInput();
    this->updateCamera();
    this->updateLight();

    Gfx::BeginPass();
	int size = MeshViewerApp::models.Size();
	this->drawUI();
	for (int i = 0; i < size; i++)
	{
 		if (MeshViewerApp::models[i].drawstate.Pipeline.IsValid())
		{
			Gfx::ApplyDrawState(MeshViewerApp::models[i].drawstate);
		}
		else
		{
			MeshViewerApp::TryAgain(MeshViewerApp::models[i]);
		}
		this->applyVariables(i);
		for (int j = 0; j < 3; j++)
		{
		Gfx::Draw(j);
		}
	}
    ImGui::Render();
    Gfx::EndPass();
    Gfx::CommitFrame();
    return Gfx::QuitRequested() ? AppState::Cleanup : AppState::Running;
}

//-----------------------------------------------------------------------------
AppState::Code
MeshViewerApp::OnCleanup() {
    IMUI::Discard();
    Input::Discard();
    Gfx::Discard();
    IO::Discard();
    return App::OnCleanup();
}

//-----------------------------------------------------------------------------
void 
MeshViewerApp::CreateObject(int curMeshIndex, glm::vec3 transform, glm::vec4 color)
{
	if (MeshViewerApp::drawStates.Size() == 0)
	{
		MeshViewerApp::MakeDrawStates();
	}
	ModelMesh &object = MeshViewerApp::models.Add(ModelMesh());
	object.curMeshIndex = curMeshIndex;
	object.material.diffuse = color;
	object.transform = glm::translate(glm::mat4(), transform);
	object.transformvec3 = transform;
	object.drawstate = MeshViewerApp::drawStates[curMeshIndex];
}

void
MeshViewerApp::MakeDrawStates()
{
	for (int i = 0; i < MeshViewerApp::numMeshes; i++)
	{
		DrawState &object = MeshViewerApp::drawStates.Add(DrawState());
		object.Mesh[0] = Gfx::LoadResource(MeshLoader::Create(MeshSetup::FromFile(MeshViewerApp::meshPaths[i]), [&object](MeshSetup& setup)
		{
			auto ps = PipelineSetup::FromLayoutAndShader(setup.Layout, Gfx::CreateResource(PhongShader::Setup()));
			ps.DepthStencilState.DepthWriteEnabled = true;
			ps.DepthStencilState.DepthCmpFunc = CompareFunc::LessEqual;
			ps.RasterizerState.CullFaceEnabled = true;
			ps.RasterizerState.SampleCount = 4;
			MeshViewerApp::numMaterials = setup.NumPrimitiveGroups();
			object.Pipeline = Gfx::CreateResource(ps);
		}));
	}
}

void MeshViewerApp::setPosition(int index, glm::vec3 transform)
{
	MeshViewerApp::models[index].transformvec3 = transform;
	MeshViewerApp::models[index].transform = glm::translate(glm::mat4(), transform);
}

void
MeshViewerApp::TryAgain(ModelMesh &object)
{
	object.drawstate = MeshViewerApp::drawStates[object.curMeshIndex];
}

void
MeshViewerApp::ChangeMesh(int curMeshIndex)
{
	MeshViewerApp::models[this->selectedID].drawstate = MeshViewerApp::drawStates[curMeshIndex];
}



//-----------------------------------------------------------------------------
void
MeshViewerApp::handleInput() {

    // rotate camera with mouse if not UI-dragging
    if (Input::TouchpadAttached()) {
        if (!ImGui::IsMouseHoveringAnyWindow()) {
            if (Input::TouchPanningStarted()) {
                this->camera.startOrbital = this->camera.orbital;
            }
            if (Input::TouchPanning()) {
                glm::vec2 diff = (Input::TouchPosition(0) - Input::TouchStartPosition(0)) * 0.01f;
                this->camera.orbital.y = this->camera.startOrbital.y - diff.x;
                this->camera.orbital.x = glm::clamp(this->camera.startOrbital.x + diff.y, glm::radians(minLatitude), glm::radians(maxLatitude));
            }
            if (Input::TouchPinchingStarted()) {
                this->camera.startDistance = this->camera.dist;
            }
            if (Input::TouchPinching()) {
                float startDist = glm::length(glm::vec2(Input::TouchStartPosition(1) - Input::TouchStartPosition(0)));
                float curDist   = glm::length(glm::vec2(Input::TouchPosition(1) - Input::TouchPosition(0)));
                this->camera.dist = glm::clamp(this->camera.startDistance - (curDist - startDist) * 0.01f, minCamDist, maxCamDist);
            }
        }
    }
    if (Input::MouseAttached()) {
        if (this->dragging) {
            if (Input::MouseButtonPressed(MouseButton::Left)) {
                this->camera.orbital.y -= Input::MouseMovement().x * 0.01f;
                this->camera.orbital.x = glm::clamp(
                    this->camera.orbital.x + Input::MouseMovement().y * 0.01f,
                    glm::radians(minLatitude),
                    glm::radians(maxLatitude));
            }
        }
        this->camera.dist = glm::clamp(this->camera.dist + Input::MouseScroll().y * 0.1f, minCamDist, maxCamDist);
    }
}

//------------------------------------------------------------------------------
void
MeshViewerApp::updateCamera() {
    if (this->camAutoOrbit) {
        this->camera.orbital.y += 0.01f;
        if (this->camera.orbital.y > glm::radians(360.0f)) {
            this->camera.orbital.y = 0.0f;
        }
    }
    this->eyePos = glm::euclidean(this->camera.orbital) * this->camera.dist;
    glm::vec3 poi  = glm::vec3(0.0f, this->camera.height, 0.0f);
    this->view = glm::lookAt(this->eyePos + poi, poi, glm::vec3(0.0f, 1.0f, 0.0f));
    this->modelViewProj = this->proj * this->view;
}

//-----------------------------------------------------------------------------
void
MeshViewerApp::updateLight() {
    if (this->lightAutoOrbit) {
        this->lightOrbital.y += 0.01f;
        if (this->lightOrbital.y > glm::radians(360.0f)) {
            this->lightOrbital.y = 0.0f;
        }
    }
    this->lightDir = glm::euclidean(this->lightOrbital);
}

//-----------------------------------------------------------------------------
void
MeshViewerApp::drawUI() {
	//const char* state;
	//switch (Gfx::QueryResourceInfo(MeshViewerApp::models[0].drawstate.Mesh[0]).State) 
	//{
	//case ResourceState::Valid: state = "Loaded"; break;
	//case ResourceState::Failed: state = "Load Failed"; break;
	//case ResourceState::Pending: state = "Loading..."; break;
	//default: state = "Invalid"; break;
	//}
	IMUI::NewFrame();
	ImGui::Begin("Mesh Viewer", nullptr, ImVec2(240, 300), 0.25f, 0);
	ImGui::PushItemWidth(130.0f);

	//ImGui::Text("state: %s\n", state);
	if (this->curMeshSetup.NumPrimitiveGroups() > 0) {
		ImGui::Text("primitive groups:\n");
		for (int i = 0; i < this->curMeshSetup.NumPrimitiveGroups(); i++) {
			ImGui::Text("%d: %d triangles\n", i, this->curMeshSetup.PrimitiveGroup(i).NumElements / 3);
		}
	}
	if (ImGui::SliderInt("num instances", &this->numWantedInstances, 1, MaxNumInstances))
	{

	}
	ImGui::SliderInt("id", &selectedID, 0, MeshViewerApp::models.Size() - 1);
	if (ImGui::Combo("##mesh", (int*)&this->curMeshIndex, this->meshNames, numMeshes)) 
	{
		this->ChangeMesh(this->curMeshIndex);
	}
	if (ImGui::CollapsingHeader("Camera")) {
		ImGui::SliderFloat("Dist##cam", &this->camera.dist, minCamDist, maxCamDist);
		ImGui::SliderFloat("Height##cam", &this->camera.height, minCamHeight, maxCamHeight);
		ImGui::SliderAngle("Long##cam", &this->camera.orbital.y, 0.0f, 360.0f);
		ImGui::SliderAngle("Lat##cam", &this->camera.orbital.x, minLatitude, maxLatitude);
		ImGui::Checkbox("Auto Orbit##cam", &this->camAutoOrbit);
		if (ImGui::Button("Reset##cam")) {
			this->camera.dist = 8.0f;
			this->camera.height = 1.0f;
			this->camera.orbital = glm::vec2(0.0f, 0.0f);
			this->camAutoOrbit = false;
		}
	}
	if (ImGui::CollapsingHeader("Light")) {
		ImGui::SliderAngle("Long##light", &this->lightOrbital.y, 0.0f, 360.0f);
		ImGui::SliderAngle("Lat##light", &this->lightOrbital.x, minLatitude, maxLatitude);
		ImGui::ColorEdit3("Color##light", &this->lightColor.x);
		ImGui::SliderFloat("Intensity##light", &this->lightIntensity, 0.0f, 5.0f);
		ImGui::Checkbox("Auto Orbit##light", &this->lightAutoOrbit);
		ImGui::Checkbox("Gamma Correct##light", &this->gammaCorrect);
		if (ImGui::Button("Reset##light")) {
			this->lightOrbital = glm::vec2(glm::radians(25.0f), 0.0f);
			this->lightColor = glm::vec4(1.0f, 1.0f, 1.0f, 1.0f);
			this->lightIntensity = 1.0f;
			this->lightAutoOrbit = false;
		}
	}
	if (ImGui::CollapsingHeader("Transform"))
	{
		if (ImGui::SliderFloat("Transform X", &MeshViewerApp::models[this->selectedID].transformvec3[0],-10, 10))
		{
			MeshViewerApp::models[this->selectedID].transform = glm::translate(glm::mat4(), MeshViewerApp::models[this->selectedID].transformvec3);
		}
		if (ImGui::SliderFloat("Transform Y", &MeshViewerApp::models[this->selectedID].transformvec3[1], -10, 10))
		{
			MeshViewerApp::models[this->selectedID].transform = glm::translate(glm::mat4(), MeshViewerApp::models[this->selectedID].transformvec3);
		}
		if (ImGui::SliderFloat("Transform Z", &MeshViewerApp::models[this->selectedID].transformvec3[2],-10, 10))
		{
			MeshViewerApp::models[this->selectedID].transform = glm::translate(glm::mat4(), MeshViewerApp::models[this->selectedID].transformvec3);
		}
	}
	if (ImGui::CollapsingHeader("Material")) {
		if ((Lambert == MeshViewerApp::models[this->selectedID].material.shaderIndex) || (Phong == MeshViewerApp::models[this->selectedID].material.shaderIndex)) {
			this->strBuilder.Format(32, "diffuse##%d", 0);
			ImGui::ColorEdit3(this->strBuilder.AsCStr(), &MeshViewerApp::models[this->selectedID].material.diffuse.x);
		}
		if (Phong == this->materials[0].shaderIndex) {
			this->strBuilder.Format(32, "specular##%d", 0);
			ImGui::ColorEdit3(this->strBuilder.AsCStr(), &MeshViewerApp::models[this->selectedID].material.specular.x);
			this->strBuilder.Format(32, "power##%d", 0);
			ImGui::SliderFloat(this->strBuilder.AsCStr(), &MeshViewerApp::models[this->selectedID].material.specPower, 1.0f, 512.0f);
		}
	}
	ImGui::PopItemWidth();
	ImGui::End();
}

//-----------------------------------------------------------------------------
void
MeshViewerApp::applyVariables(int matIndex) {
    switch (MeshViewerApp::models[matIndex].material.shaderIndex) {
        case Normals:
            // Normals shader
            {
                NormalsShader::vsParams vsParams;
                vsParams.mvp = this->modelViewProj * MeshViewerApp::models[matIndex].transform;
                Gfx::ApplyUniformBlock(vsParams);
            }
            break;
        case Lambert:
            // Lambert shader
            {
                LambertShader::vsParams vsParams;
                vsParams.mvp = this->modelViewProj * MeshViewerApp::models[matIndex].transform;
                vsParams.model = this->model;
                Gfx::ApplyUniformBlock(vsParams);

                LambertShader::fsParams fsParams;
                fsParams.lightColor = this->lightColor * this->lightIntensity;
                fsParams.lightDir = this->lightDir;
                fsParams.matDiffuse = this->materials[matIndex].diffuse;
                fsParams.gammaCorrect = this->gammaCorrect ? 1.0f : 0.0f;
                Gfx::ApplyUniformBlock(fsParams);
            }
            break;
        case Phong:
            // Phong shader
            {
                PhongShader::vsParams vsParams;
                vsParams.mvp = this->modelViewProj * MeshViewerApp::models[matIndex].transform;
                vsParams.model = this->model;
                Gfx::ApplyUniformBlock(vsParams);

                PhongShader::fsParams fsParams;
                fsParams.eyePos = this->eyePos;
                fsParams.lightColor = this->lightColor * this->lightIntensity;
                fsParams.lightDir = this->lightDir;
                fsParams.matDiffuse = MeshViewerApp::models[matIndex].material.diffuse;
                fsParams.matSpecular = MeshViewerApp::models[matIndex].material.specular;
                fsParams.matSpecularPower = MeshViewerApp::models[matIndex].material.specPower;
                fsParams.gammaCorrect = this->gammaCorrect ? 1.0f : 0.0f;
                Gfx::ApplyUniformBlock(fsParams);
            }
            break;
            
        default:
            o_error("Unknown shader index, FIXME!");
            break;
    }
}
