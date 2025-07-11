#include "org_zero123_PyMcBridge_EventManager.h"
#include <pybind11/embed.h>
#include "../PyBridge/GameEvent.h"
#include "../Utils/JNIConv.hpp"
// JNI游戏事件管理器
namespace py = pybind11;

static py::dict parseJsonString(const std::string& jsonStr)
{
	// 由于CPython内部使用哈希表处理属性 因此不需要缓存也有不错的性能
	try
	{
		py::object json = py::module_::import("json");
		py::dict result = json.attr("loads")(jsonStr);
		return result;
	}
	catch (const std::exception& e)
	{
		std::cout << e.what() << "\n";
	}
	return py::dict();
}

// 无参数事件广播 性能极高 适用于tick/fps事件
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_EventManager_callServerEvent(JNIEnv*, jclass, jint eventId)
{
	if (!QPyMCBridge::hasServerEventHandler(eventId))
	{
		return;
	}
	py::gil_scoped_acquire gil;
	QPyMCBridge::callServerEvent(eventId);
}

JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_EventManager_callClientEvent(JNIEnv*, jclass, jint eventId)
{
	if (!QPyMCBridge::hasClientEventHandler(eventId))
	{
		return;
	}
	py::gil_scoped_acquire gil;
	QPyMCBridge::callClientEvent(eventId);
}

// 性能问题: 受JNI反射效率低下以及二进制缓冲区不利于维护综合考虑 此处直接使用JSON字符串传递参数 适用于低频率事件
JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_EventManager_callServerJsonEvent(JNIEnv* env, jclass, jint eventId, jstring json)
{
	if (!QPyMCBridge::hasServerEventHandler(eventId))
	{
		return;
	}
	py::gil_scoped_acquire gil;
	auto pyDict = parseJsonString(QPyMCBridge::JNI::jStringToStdString(env, json));
	QPyMCBridge::callArgsServerEvent(eventId, pyDict);
}

JNIEXPORT void JNICALL Java_org_zero123_PyMcBridge_EventManager_callClientJsonEvent(JNIEnv* env, jclass, jint eventId, jstring json)
{
	if (!QPyMCBridge::hasClientEventHandler(eventId))
	{
		return;
	}
	py::gil_scoped_acquire gil;
	auto pyDict = parseJsonString(QPyMCBridge::JNI::jStringToStdString(env, json));
	QPyMCBridge::callArgsClientEvent(eventId, pyDict);
}

template <typename HasHandlerFunc, typename CallEventFunc>
jstring callEventCapTemplate(
	JNIEnv* env,
	jint eventId,
	jstring json,
	jobjectArray capKeys,
	HasHandlerFunc hasHandler,
	CallEventFunc callEvent)
{
	if (!hasHandler(eventId))
	{
		return env->NewStringUTF("{}");
	}

	py::gil_scoped_acquire gil;
	auto pyDict = parseJsonString(QPyMCBridge::JNI::jStringToStdString(env, json));
	std::vector<std::string> targetCapKey = QPyMCBridge::JNI::convertJStringArray(env, capKeys);
	std::unordered_map<std::string, py::object> capMap;	// 捕获初始值Map
	for (const auto& key : targetCapKey)
	{
		if (pyDict.contains(key.c_str()))
		{
			capMap[key] = pyDict[key.c_str()];
		}
	}

	// 广播事件
	callEvent(eventId, pyDict);

	py::dict capChanges;
	for (const auto& it : capMap)
	{
		// 检查变化情况
		if (pyDict.contains(it.first.c_str()) &&
			!pyDict[it.first.c_str()].cast<py::object>().equal(it.second))
		{
			capChanges[it.first.c_str()] = pyDict[it.first.c_str()];
		}
	}

	if (capChanges.empty())
	{
		return env->NewStringUTF("{}");
	}

	py::object joModule = py::module_::import("json");
	std::string result = joModule.attr("dumps")(capChanges).cast<std::string>();
	return env->NewStringUTF(result.c_str());
}

jstring JNICALL Java_org_zero123_PyMcBridge_EventManager_callServerEventCap(JNIEnv* env, jclass, jint eventId, jstring json, jobjectArray capKeys)
{
	return callEventCapTemplate(env, eventId, json, capKeys, QPyMCBridge::hasServerEventHandler, QPyMCBridge::callArgsServerEvent);
}

jstring JNICALL Java_org_zero123_PyMcBridge_EventManager_callClientEventCap(JNIEnv* env, jclass, jint eventId, jstring json, jobjectArray capKeys)
{
	return callEventCapTemplate(env, eventId, json, capKeys, QPyMCBridge::hasClientEventHandler, QPyMCBridge::callArgsClientEvent);
}
