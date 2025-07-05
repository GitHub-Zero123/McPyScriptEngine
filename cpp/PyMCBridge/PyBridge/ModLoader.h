#pragma once
#include <pybind11/embed.h>

namespace QPyMCBridge
{
	void PyModLoaderModuleReg(pybind11::module_*);
	void PyModLoaderDestroy();

	// MOD加载器管理
	void PyCallServerInitEvent();
	void PyCallServerDestroyEvent();
	void PyCallClientInitEvent();
	void PyCallClientDestroyEvent();
}