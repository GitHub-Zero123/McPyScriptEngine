#pragma once
#include <pybind11/embed.h>

namespace QPyMCBridge
{
	namespace Utils
	{
		namespace Math
		{
			void _RegModule(pybind11::module_*);
		}
	}
}