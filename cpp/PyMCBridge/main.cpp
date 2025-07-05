#include <iostream>
#include <pybind11/embed.h>
#include "PyBridge/GameThread.h"
#include "PyBridge/VMManager.h"
#include "PyBridge/GameEvent.h"
#include "Utils/EnvEncode.h"
#include <thread>
#include <vector>

namespace py = pybind11;

static void threadInitHandler()
{
	try
	{
		QPyMCBridge::loadMod("testMod_1");
	}
	catch (const std::exception& e)
	{
		std::cerr << e.what() << "\n";
	}
}

int main()
{
	Encoding::initEnvcode();
	std::vector<std::thread> threads;
	QPyMCBridge::setGameThreadInitHandler(threadInitHandler);
	QPyMCBridge::addEnvPath(std::string("D:/Zero123/Minecraft/MODSDK_ENV"));
	// QPyMCBridge::initVM();

	// 服务端线程
	threads.emplace_back([]() {
		QPyMCBridge::loadServerThread();

		{
			py::gil_scoped_acquire gil;
			// 触发tick事件 且不提供dict参数
			QPyMCBridge::callServerEvent(1);
		}
		
		std::this_thread::sleep_for(std::chrono::milliseconds(500));
		QPyMCBridge::destroyServerThread();
		});

	std::chrono::milliseconds(50);

	// 客户端线程
	threads.emplace_back([]() {
		QPyMCBridge::loadClientThread();
		std::this_thread::sleep_for(std::chrono::milliseconds(800));
		QPyMCBridge::destroyClientThread();
		});

	for (auto& thread : threads)
	{
		thread.join();
	}
	
	while (QPyMCBridge::getVMLiveState())
	{
		std::this_thread::sleep_for(std::chrono::milliseconds(50));
	}
	std::cout << "All threads have finished execution.\n";
	return 0;
}

//int main()
//{
//	Encoding::initEnvcode();
//	std::thread([]() {
//		std::cout << "VM测试\n";
//		QPyMCBridge::initVM();
//		std::cout << "获取GIL\n";
//		{
//			py::gil_scoped_acquire gil;
//			py::exec("print(111)");
//		}
//		std::cout << "end\n";
//		QPyMCBridge::destroyVM();
//		}).join();
//	return 0;
//}