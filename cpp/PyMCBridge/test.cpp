#include <iostream>
#include <filesystem>
#include <fstream>
#include <format>
#include <pybind11/embed.h>
#include <vector>
#include <thread>
#include <unordered_map>
#include "utils/EnvEncode.h"

namespace py = pybind11;

static std::string readFileRaw(const std::string& filepath)
{
	std::ifstream file(filepath, std::ios::binary);  // 二进制模式打开，避免任何换行转换
	if (!file)
	{
		throw std::runtime_error("Failed to open file");
	}

	file.seekg(0, std::ios::end);
	std::streamsize size = file.tellg();
	file.seekg(0, std::ios::beg);

	std::string buffer(size, '\0');
	if (!file.read(&buffer[0], size))
	{
		throw std::runtime_error("Failed to read file");
	}

	return buffer;
}

enum THREAD_TYPE
{
	UNKNOWN = -1,
	CLIENT = 0,
	SERVER = 1,
};

static thread_local THREAD_TYPE _threadType = THREAD_TYPE::UNKNOWN;

static THREAD_TYPE getThreadTypeId()
{
	return _threadType;
}

static bool isServerThread()
{
	return getThreadTypeId() == THREAD_TYPE::SERVER;
}

static bool isClientThread()
{
	return getThreadTypeId() == THREAD_TYPE::CLIENT;
}

static std::vector<py::function> serverInitHandlers;
static std::vector<py::function> clientInitHandlers;
static std::vector<py::function> serverDestroyHandlers;
static std::vector<py::function> clientDestroyHandlers;
static std::unordered_map<int, std::vector<py::function>> serverEventHandlers;
static std::unordered_map<int, std::vector<py::function>> clientEventHandlers;

PYBIND11_EMBEDDED_MODULE(PyMCBridge, m)
{
	pybind11::module_ modLoader = m.def_submodule("ModLoader", "Mod加载器模块");
	modLoader.def("getThreadTypeId", []() { return static_cast<int>(getThreadTypeId()); });
	modLoader.def("isServerThread", &isServerThread);
	modLoader.def("isClientThread", &isClientThread);
	modLoader.def("regServerLoaderHandler", [](py::object&& pyo) {
		serverInitHandlers.push_back(std::move(pyo));
	});
	modLoader.def("regClientLoaderHandler", [](py::object&& pyo) {
		clientInitHandlers.push_back(std::move(pyo));
	});
	modLoader.def("regServerDestroyHandler", [](py::object&& pyo) {
		serverDestroyHandlers.push_back(std::move(pyo));
	});
	modLoader.def("regClientDestroyHandler", [](py::object&& pyo) {
		clientDestroyHandlers.push_back(std::move(pyo));
	});

	pybind11::module_ eventListener = m.def_submodule("EventListener", "Mod事件监听器");
	eventListener.def("listenForServerEvent", [](int eventId, py::object&& pyo) {
		auto it = serverEventHandlers.find(eventId);
		if (it == serverEventHandlers.end())
		{
			serverEventHandlers[eventId] = std::vector<py::function>();
			it = serverEventHandlers.find(eventId);
		}
		it->second.push_back(std::move(pyo));
	});
	eventListener.def("listenForClientEvent", [](int eventId, py::object&& pyo) {
		auto it = clientEventHandlers.find(eventId);
		if (it == clientEventHandlers.end())
		{
			clientEventHandlers[eventId] = std::vector<py::function>();
			it = clientEventHandlers.find(eventId);
		}
		it->second.push_back(std::move(pyo));
	});
}

static void TRY_EXEC_LIST_PY_FUNC(const std::vector<py::function>& funcs)
{
	for (const auto& f : funcs)
	{
		try
		{
			f();
		}
		catch (const std::exception& e)
		{
			std::cout << e.what() << "\n";
		}
	}
}

static void PY_ADD_ENV_PATH(const std::filesystem::path& p)
{
	py::exec(std::format(R"(import sys
sys.path.append('{}')
)", p.generic_string()));
}

static void LOAD_MOD_MAIN(const std::string& modPackName)
{
	std::string fullName = std::format("{}.modMain", modPackName);
	py::module_::import(fullName.c_str());
}

static void SERVER_THREAD_LOOP()
{
	_threadType = THREAD_TYPE::SERVER;
	py::gil_scoped_acquire gil;
	LOAD_MOD_MAIN("testMod_1");
	TRY_EXEC_LIST_PY_FUNC(serverInitHandlers);
	
	for (int i = 0; i < 300; i++)
	{
		auto it = serverEventHandlers.find(1);
		if(it != serverEventHandlers.end())
		{
			for (const auto& f : it->second)
			{
				try
				{
					f();
				}
				catch (const std::exception& e)
				{
					std::cout << e.what() << "\n";
				}
			}
		}
		py::gil_scoped_release rel;
		std::this_thread::sleep_for(std::chrono::milliseconds(33));
	}

	TRY_EXEC_LIST_PY_FUNC(serverDestroyHandlers);
}

static void CLIENT_THREAD_LOOP()
{
	_threadType = THREAD_TYPE::CLIENT;
	py::gil_scoped_acquire gil;
	LOAD_MOD_MAIN("testMod_1");
	TRY_EXEC_LIST_PY_FUNC(clientInitHandlers);
	TRY_EXEC_LIST_PY_FUNC(clientDestroyHandlers);
}

int main()
{
	Encoding::initEnvcode();
	py::scoped_interpreter guard{};
	PY_ADD_ENV_PATH("D:/Zero123/Minecraft/MODSDK_ENV");
	py::exec(R"(
import sys
import threading
sys.dont_write_bytecode = True
)");
	{
		py::gil_scoped_release rel;
		std::thread ser([]() {
			try
			{
				SERVER_THREAD_LOOP();
			}
			catch (const std::exception& e)
			{
				std::cerr << e.what() << "\n";
			}
			});

		std::thread cli([]() {
			try
			{
				CLIENT_THREAD_LOOP();
			}
			catch (const std::exception& e)
			{
				std::cerr << e.what() << "\n";
			}
			});

		ser.join();
		cli.join();
	}
	serverInitHandlers.clear();
	clientInitHandlers.clear();
	serverDestroyHandlers.clear();
	clientDestroyHandlers.clear();
	serverEventHandlers.clear();
	clientEventHandlers.clear();
	std::cout << "END\n";
	return 0;
}