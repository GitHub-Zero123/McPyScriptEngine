# PyScriptEngine
为 Minecraft Java MOD 提供嵌入式 Python 支持，允许直接使用Python开发MOD脚本。

> ⚠️ 该项目为实验性功能，主要用于功能验证和技术探索。部分功能可能会根据实际需求进行调整，仅供参考和学习。

## 目录结构说明

- `cpp/*`: C++ 部分的实现细节，包括底层接口与 Python 的集成方式。
- `python/*`: Python 脚本Demo 及相关接口封装。
- `java/*`: Java 端与 MOD 相关的集成和调用方式。

如需了解各部分的具体实现和用法，请参考对应子目录下的 README 文件以及其源代码实现。

![Main](images/img1.jpg)

## PyMods 加载说明
引擎会自动加载 Minecraft 目录下 `pyMods` 文件夹内的Mod包。
```
.minecraft/
├─ mods/PyScriptEngine.jar
├─ pyMods/
│  └─ {ModName}/
│     └─ modMain.py
|      ...
```

### 游戏日志
如果使用正式环境的jar包引擎开发测试，请在modMain.py文件启用局内游戏日志支持。
```python
# modMain.py
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

try:
    # 启用游戏内日志支持(仅限PyScriptEngine, 官方Modsdk中并未提供此模块)
    import mod.gameLog
except:
    pass

@Mod.Binding("testMod1", "1.0.0")
class TestMod1(object):
    @Mod.InitServer()
    def initServer(self):
        serverApi.RegisterSystem("TestMod1", "TestServerSystem", "testMod_1.Server.TestSystem")

    @Mod.InitClient()
    def initClient(self):
        clientApi.RegisterSystem("TestMod1", "TestClientSystem", "testMod_1.Client.TestSystem")

    @Mod.DestroyServer()
    def serverDestroy(self):
        print("服务端销毁")

    @Mod.DestroyClient()
    def clientDestroy(self):
        print("客户端销毁")
```

**[By Zero123](https://space.bilibili.com/456549011)**  