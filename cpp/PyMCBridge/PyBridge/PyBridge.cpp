#include "PyBridge.h"
#include <pybind11/embed.h>
#include "ModLoader.h"
#include "GameEvent.h"
#include "Utils/Math.h"
#include "../JNI/JNIManager.h"

// By Zero123
namespace py = pybind11;

// PyNative模块绑定
PYBIND11_EMBEDDED_MODULE(PyMCBridge, m)
{
	QPyMCBridge::PyEventEngineModuleReg(&m);
	QPyMCBridge::PyModLoaderModuleReg(&m);
	// QPyMCBridge::API::EntityModule::_ModuleReg(&m);
	QPyMCBridge::Utils::Math::_RegModule(&m);
	QPyMCBridge::JNI::_JNIModuleReg(&m);
}

// VM析构处理
void QPyMCBridge::PyVMDestroyHandler()
{
	QPyMCBridge::PyEventEngineDestroy();
	QPyMCBridge::PyModLoaderDestroy();
	// QPyMCBridge::API::EntityModule::_VMDestroy();
}
