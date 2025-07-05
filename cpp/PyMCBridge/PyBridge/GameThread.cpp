#include "GameThread.h"
#include "VMManager.h"
#include "ModLoader.h"
#include "../Utils/Log.hpp"
#include <iostream>
#include <mutex>
#include <optional>
// By Zero123
namespace py = pybind11;

// 不同线程对vm的依赖引用计数
static int vmRefCount = 0;
static std::mutex vmMutex;
static thread_local auto _threadType = QPyMCBridge::THREAD_TYPE::UNKNOWN;
static void(*_gameThreadInitHandler)() = nullptr;

static void _threadEnvInit()
{
	std::lock_guard<std::mutex> lock(vmMutex);
	if (vmRefCount == 0)
	{
		QPyMCBridge::initVM();
	}
	++vmRefCount;
}

static void _threadEnvDestroy()
{
	std::lock_guard<std::mutex> lock(vmMutex);
	--vmRefCount;
	if (vmRefCount == 0)
	{
		QPyMCBridge::destroyVM();
	}
}

// 记录线程存活状态
static bool _serverLive;
static bool _clientLive;

class CLThread
{
private:
	static std::optional<CLThread> _instance;
public:
	static CLThread& getInstance()
	{
		if (!_instance)
		{
			_instance.emplace();
		}
		return *_instance;
	}

	static void destroyInstance()
	{
		_instance.reset();
	}

	CLThread()
	{
		_threadType = QPyMCBridge::THREAD_TYPE::CLIENT;
		_clientLive = true;
		_threadEnvInit();
		// 触发客户端初始化事件
		py::gil_scoped_acquire gil;
		if (_gameThreadInitHandler != nullptr)
		{
			_gameThreadInitHandler();
		}
		QPyMCBridge::PyCallClientInitEvent();
	}

	~CLThread()
	{
		// 触发客户端销毁事件
		{
			// DEBUG_LOG("试图获取GIL");
			py::gil_scoped_acquire gil;
			// DEBUG_LOG("GIL获取成功");
			QPyMCBridge::PyCallClientDestroyEvent();
		}
		_threadEnvDestroy();
		_clientLive = false;
		DEBUG_LOG("[CPP] 客户端析构\n");
	}
};

class SERThread
{
private:
	static std::optional<SERThread> _instance;
public:
	static SERThread& getInstance()
	{
		if (!_instance)
		{
			_instance.emplace();
		}
		return *_instance;
	}

	static void destroyInstance()
	{
		_instance.reset();
	}

	SERThread()
	{
		_threadType = QPyMCBridge::THREAD_TYPE::SERVER;
		_serverLive = true;
		_threadEnvInit();
		// 触发服务器初始化事件
		py::gil_scoped_acquire gil;
		if (_gameThreadInitHandler != nullptr)
		{
			_gameThreadInitHandler();
		}
		QPyMCBridge::PyCallServerInitEvent();
	}

	~SERThread()
	{
		// 触发服务器销毁事件
		{
			py::gil_scoped_acquire gil;
			QPyMCBridge::PyCallServerDestroyEvent();
		}
		_threadEnvDestroy();
		_serverLive = false;
		DEBUG_LOG("[CPP] 服务端析构\n");
	}
};

std::optional<SERThread> SERThread::_instance;
std::optional<CLThread> CLThread::_instance;

namespace QPyMCBridge
{
	void loadServerThread()
	{
		SERThread::getInstance();
	}

	void loadClientThread()
	{
		CLThread::getInstance();
	}

	void destroyServerThread()
	{
		SERThread::destroyInstance();
	}

	void destroyClientThread()
	{
		CLThread::destroyInstance();
	}

	THREAD_TYPE getThreadType()
	{
		return _threadType;
	}

	void setGameThreadInitHandler(void(*handler)())
	{
		_gameThreadInitHandler = handler;
	}

	bool getServerThreadLiveState()
	{
		
		return _serverLive;
	}

	bool getClientThreadLiveState()
	{
		return _clientLive;
	}
}