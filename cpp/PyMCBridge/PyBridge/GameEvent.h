#pragma once
#include <pybind11/embed.h>

namespace QPyMCBridge
{
	void PyEventEngineModuleReg(pybind11::module_*);
	void PyEventEngineDestroy();

	// native事件广播
	void callArgsServerEvent(int eventId, pybind11::object&);
	void callArgsClientEvent(int eventId, pybind11::object&);
	void callServerEvent(int eventId);
	void callClientEvent(int eventId);
	bool hasServerEventHandler(int eventId);
	bool hasClientEventHandler(int eventId);
}