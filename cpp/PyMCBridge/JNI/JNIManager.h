#pragma once
#include <jni.h>
#include <pybind11/embed.h>

namespace QPyMCBridge
{
	namespace JNI
	{
		// 获取当前线程的JNI环境
		JNIEnv* getJNIEnv();
		// 获取JVM存活状态
		bool getJVMLiveState();
		// JNI模块注册
		void _JNIModuleReg(pybind11::module_*);
	}
}