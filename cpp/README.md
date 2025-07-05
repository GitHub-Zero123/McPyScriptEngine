# PyMCBridge
`PyMCBridge` 为 Python 提供了 Java 版 Minecraft（基于 NeoForge）的绑定接口。

## 虚拟机差异
- 原版：基于 Python 2.7.18
- PyMCBridge：基于 Python 3.12.x

## NativeAPI
您可以通过 `org.zero123.PyMcBridge` 包找到提供的`CPP扩展`API，提供了PythonVM，MOD加载器，事件系统的功能。