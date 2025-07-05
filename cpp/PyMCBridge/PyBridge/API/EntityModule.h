#pragma once
#include <pybind11/embed.h>

namespace QPyMCBridge
{
	namespace API
	{
		namespace EntityModule
		{
			void _ModuleReg(pybind11::module_*);
			void _VMDestroy();
		}
	}
}