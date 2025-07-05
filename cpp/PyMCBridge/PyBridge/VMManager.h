#pragma once
#include <iostream>
#include <filesystem>

namespace QPyMCBridge
{
	// 是否初始化Py线程
	extern bool INIT_PY_THREAD;

	// 初始化PyVM
	void initVM();

	// 销毁PyVM
	void destroyVM();

	// VM存活状态
	bool getVMLiveState();

	// 添加环境路径
	void addEnvPath(const std::filesystem::path&);

	void addEnvPath(const std::string&);

	void addEnvPath(const char*);

	// 加载特定MOD(需要获取GIL)
	void loadMod(const std::string& name);

	void setUseUTF8(bool);

	// 刷新py标准输出流
	void flushPyStdout();

	// 设置py标准根据行刷新标准输出流
	void setPyLineFlushMode(bool enable);
}