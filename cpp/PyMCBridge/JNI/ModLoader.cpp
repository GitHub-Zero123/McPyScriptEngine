#include "org_zero123_PyMcBridge_ModLoader.h"
#include "../Utils/JNIConv.hpp"
#include "../PyBridge/GameThread.h"
#include "../PyBridge/VMManager.h"
#include "../PyBridge/ModLoader.h"

namespace py = pybind11;

// 加载服务端线程
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_loadServerThread(JNIEnv*, jclass)
{
	try
	{
		QPyMCBridge::loadServerThread();
	}
	catch (const std::exception& e)
	{
		std::cerr << "[CPP] 服务端线程加载失败: " << e.what() << "\n";
	}
}

// 加载客户端线程
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_loadClientThread(JNIEnv*, jclass)
{
	try
	{
		QPyMCBridge::loadClientThread();
	}
	catch (const std::exception& e)
	{
		std::cerr << "[CPP] 客户端线程加载失败: " << e.what() << "\n";
	}
}

// 析构服务端线程
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_destroyServerThread(JNIEnv*, jclass)
{
	QPyMCBridge::destroyServerThread();
}

// 析构客户端线程
JNIEXPORT void Java_org_zero123_PyMcBridge_ModLoader_destroyClientThread(JNIEnv*, jclass)
{
	QPyMCBridge::destroyClientThread();
}

// 添加环境变量
JNIEXPORT void Java_org_zero123_PyMcBridge_ModLoader_addEnvPath(JNIEnv* env, jclass, jstring path)
{
	QPyMCBridge::addEnvPath(QPyMCBridge::JNI::jStringToStdString(env, path));
}

static std::vector<std::string> _modList;
// static std::mutex _modListMutex;

static void gameThreadInitHandler()
{
	//std::vector<std::string> localModList;
	//{
	//	std::lock_guard<std::mutex> lock(_modListMutex);
	//	localModList = _modList;
	//}
	for (const auto& mod : _modList)
	{
		QPyMCBridge::loadMod(mod);
	}
}

// 设置目标加载的mod列表
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_setTargetMods(JNIEnv* env, jclass, jobjectArray mods)
{
	//{
	//	std::lock_guard<std::mutex> lock(_modListMutex);
	//	_modList = QPyMCBridge::JNI::convertJStringArray(env, mods);
	//}
	_modList = QPyMCBridge::JNI::convertJStringArray(env, mods);
	QPyMCBridge::setGameThreadInitHandler(gameThreadInitHandler);
}

JNIEXPORT jint JNICALL Java_org_zero123_PyMcBridge_ModLoader_getPyServerLiveState(JNIEnv*, jclass)
{
	return static_cast<jint>(QPyMCBridge::getServerThreadLiveState());
}

JNIEXPORT jint JNICALL Java_org_zero123_PyMcBridge_ModLoader_getPyClientLiveState(JNIEnv*, jclass)
{
	return static_cast<jint>(QPyMCBridge::getClientThreadLiveState());
}

void JNICALL Java_org_zero123_PyMcBridge_ModLoader_flushPyStdout(JNIEnv*, jclass)
{
	QPyMCBridge::flushPyStdout();
}

// 动态执行Python代码
void JNICALL Java_org_zero123_PyMcBridge_ModLoader_execPyCode(JNIEnv* env, jclass, jstring code)
{
	pybind11::gil_scoped_acquire gil;
	pybind11::exec(QPyMCBridge::JNI::jStringToStdString(env, code));
	return;
}

JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_setPyForceUseUTF8(JNIEnv*, jclass, jint i)
{
	QPyMCBridge::setUseUTF8(static_cast<bool>(i));
}

static std::wstring glPythonHomePath;

#ifdef _WIN32
#include <windows.h>
static std::wstring utf8ToWstring(const std::string& str)
{
	if (str.empty())
	{
		return std::wstring();
	}
	int wideSize = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, nullptr, 0);
	std::wstring wstr(wideSize, 0);
	MultiByteToWideChar(CP_UTF8, 0, str.c_str(), -1, &wstr[0], wideSize);
	wstr.pop_back(); // 去除 null terminator
	return wstr;
}

JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_setPythonHome(JNIEnv* env, jclass, jstring path)
{
	auto u8Path = QPyMCBridge::JNI::jStringToStdString(env, path);
	glPythonHomePath = utf8ToWstring(u8Path);
	//SetDefaultDllDirectories(LOAD_LIBRARY_SEARCH_DEFAULT_DIRS);
	//AddDllDirectory(glPythonHomePath.c_str());
	// 设置 Python 解释器路径
	Py_SetPythonHome(const_cast<wchar_t*>(glPythonHomePath.c_str()));
}

#else
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_ModLoader_setPythonHome(JNIEnv* env, jclass, jstring path)
{
	auto u8Path = QPyMCBridge::JNI::jStringToStdString(env, path);
	std::cerr << "解释器路径设置失败, 暂未适配当前平台: " << u8Path << "\n";
}

#endif

void JNICALL Java_org_zero123_PyMcBridge_ModLoader_setPyLineFlushMode(JNIEnv*, jclass, jboolean state)
{
	QPyMCBridge::setPyLineFlushMode(state);
}