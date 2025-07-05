#include "EntityModule.h"
#include <iostream>
#include <vector>

// EntityModule注册
void QPyMCBridge::API::EntityModule::_ModuleReg(pybind11::module_* m)
{
	pybind11::module_ entityModule = m->def_submodule("EntityModule", "实体模块");
	// Server, Client字段的方法为对应端独占，请勿跨线程调用
	entityModule.def("getClientPlayerId", []() -> std::string {
		return "-1";
	});

	entityModule.def("getServerPlayerList", []() -> std::vector<std::string> {
		return {};
	});
}

// VM析构
void QPyMCBridge::API::EntityModule::_VMDestroy()
{

}