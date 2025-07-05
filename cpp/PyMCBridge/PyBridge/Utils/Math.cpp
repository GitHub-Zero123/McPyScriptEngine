#include "Math.h"
#include <tuple>
#include <cmath>

static constexpr float _PI = 3.1415f;

void QPyMCBridge::Utils::Math::_RegModule(pybind11::module_* m)
{
	pybind11::module_ mathModule = m->def_submodule("Math");
	mathModule.def("_entityRotToDir", [](float pitchDeg, float yawDeg) -> std::tuple<float, float, float> {
        float pitch = pitchDeg * _PI / 180.0f;
        float yaw = yawDeg * _PI / 180.0f;

        float x = -std::sin(yaw) * std::cos(pitch);
        float y = -std::sin(pitch);
        float z = std::cos(yaw) * std::cos(pitch);

        return std::make_tuple(x, y, z);
	});
}
