# MODSDK 兼容层
提供了对于 `网易我的世界` MODSDK 的兼容层，可通过 `mod` 模块访问和调用相关功能。

## 特性差异
由于其实现于原版架构差异较大，部分参数细节可能存在差异，如：实体ID在JE版将以UUID字符串返回。

## 测试 Demo
- `testMod_0`：`QuModLibs` 的移植测试，实现了一组基础玩法。
- `testMod_1`：`ModSdk` 系统与组件工厂的移植测试。
- `testMod_2`: `QuMod3` 独立API测试（仅限PyScriptEngine）。

每个 Demo 文件夹均包含相应功能的示例代码，便于参考和测试。