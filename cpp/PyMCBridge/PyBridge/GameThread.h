#pragma once

namespace QPyMCBridge
{
	// 游戏线程类型
	enum THREAD_TYPE
	{
		UNKNOWN = -1,
		CLIENT = 0,
		SERVER = 1,
	};
	// 游戏线程管理
	void loadServerThread();
	void loadClientThread();
	void destroyServerThread();
	void destroyClientThread();
	THREAD_TYPE getThreadType();
	// 设置游戏线程初始化函数 通常用于加载mod(客户端与服务端均会执行)
	void setGameThreadInitHandler(void (*handler)());

	bool getServerThreadLiveState();
	bool getClientThreadLiveState();
}