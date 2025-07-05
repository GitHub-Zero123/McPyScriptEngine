#include "ModLoader.h"
#include "../Core/EventSystem.hpp"
#include "GameThread.h"
// By Zero123
namespace py = pybind11;

static QPyMCBridge::EventManager<py::function> serverInitHandlers;
static QPyMCBridge::EventManager<py::function> clientInitHandlers;
static QPyMCBridge::EventManager<py::function> serverDestroyHandlers;
static QPyMCBridge::EventManager<py::function> clientDestroyHandlers;

namespace QPyMCBridge
{
	// MOD加载器导出Native模块
	void PyModLoaderModuleReg(pybind11::module_* m)
	{
		pybind11::module_ modLoader = m->def_submodule("ModLoader", "Mod加载器模块");
		// 线程查询
		modLoader.def("getThreadTypeId", []() { return static_cast<int>(getThreadType()); });
		modLoader.def("isServerThread", []() { return getThreadType() == THREAD_TYPE::SERVER; });
		modLoader.def("isClientThread", []() { return getThreadType() == THREAD_TYPE::CLIENT; });

		// 加载器事件注册
		modLoader.def("regServerLoaderHandler", [](py::object&& pyo) {
			serverInitHandlers.addHandler(std::move(pyo));
		});
		modLoader.def("regClientLoaderHandler", [](py::object&& pyo) {
			clientInitHandlers.addHandler(std::move(pyo));
		});
		modLoader.def("regServerDestroyHandler", [](py::object&& pyo) {
			serverDestroyHandlers.addHandler(std::move(pyo));
		});
		modLoader.def("regClientDestroyHandler", [](py::object&& pyo) {
			clientDestroyHandlers.addHandler(std::move(pyo));
		});
	}

	void PyModLoaderDestroy()
	{
		serverInitHandlers.clear();
		clientInitHandlers.clear();
		serverDestroyHandlers.clear();
		clientDestroyHandlers.clear();
	}

	void PyCallServerInitEvent()
	{
		serverInitHandlers.call();
	}

	void PyCallServerDestroyEvent()
	{
		serverDestroyHandlers.call();
	}

	void PyCallClientInitEvent()
	{
		clientInitHandlers.call();
	}

	void PyCallClientDestroyEvent()
	{
		clientDestroyHandlers.call();
	}
}