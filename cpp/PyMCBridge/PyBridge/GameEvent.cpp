#include "GameEvent.h"
#include <iostream>
#include "../Core/EventSystem.hpp"
// By Zero123
namespace py = pybind11;

static QPyMCBridge::MapEventManager<int, py::function> serverEventMap;
static QPyMCBridge::MapEventManager<int, py::function> clientEventMap;

namespace QPyMCBridge
{
	void PyEventEngineModuleReg(py::module_* m)
	{
		pybind11::module_ eventListener = m->def_submodule("EventListener", "Mod事件监听器");
		eventListener.def("listenForServerEvent", [](int eventId, py::function&& pyo) {
			serverEventMap.regHandler(eventId, pyo);
		});
		eventListener.def("listenForClientEvent", [](int eventId, py::function&& pyo) {
			clientEventMap.regHandler(eventId, pyo);
		});
	}

	void PyEventEngineDestroy()
	{
		serverEventMap.clear();
		clientEventMap.clear();
	}

	void callArgsServerEvent(int eventId, pybind11::object& args)
	{
		serverEventMap.call(eventId, args);
	}

	void callArgsClientEvent(int eventId, pybind11::object& args)
	{
		clientEventMap.call(eventId, args);
	}

	void callServerEvent(int eventId)
	{
		serverEventMap.call(eventId);
	}

	void callClientEvent(int eventId)
	{
		clientEventMap.call(eventId);
	}

	bool hasServerEventHandler(int eventId)
	{
		return serverEventMap.hasEvent(eventId);
	}

	bool hasClientEventHandler(int eventId)
	{
		return clientEventMap.hasEvent(eventId);
	}
}