from ..utils import importModule, entityRotToDir
from .system.serverSystem import (
    ServerSystem,
    ServerSystemManager,
)
from functools import lru_cache
lambda: "Extra Server API"

def RegisterSystem(namespace: str, systemName: str, clsPath: str) -> object:
    return ServerSystemManager.getInstance().registerClsPath(namespace, systemName, clsPath)

def GetSystem(namespace: str, systemName: str) -> object:
    return ServerSystemManager.getInstance().getSystem((namespace, systemName))

def GetLevelId() -> str:
    return ""

@lru_cache(1)
def GetEngineCompFactory():
    """ 获取引擎组件工厂 """
    from .compFactory import EngineCompFactory
    return EngineCompFactory()

def GetServerSystemCls():
    """ 获取服务端系统类 """
    return ServerSystem

def GetEngineNamespace() -> str:
    """ 获取引擎命名空间 """
    return "Minecraft"

def GetEngineSystemName() -> str:
    """ 获取引擎系统名称 """
    return "Engine"

def ImportModule(filePath: str) -> object:
    """ 服务端文件导入 """
    return importModule(filePath)

def GetDirFromRot(rot: tuple) -> tuple:
    """ 从欧拉角旋转获取方向 """
    return entityRotToDir(rot)

def GetEngineActor() -> dict:
    """ 获取所有实体 暂不支持详细value数据 """
    from ..api.entityModule import _serverGetWorldEntityList
    return {k: {} for k in _serverGetWorldEntityList()}

def GetPlayerList() -> list:
    """ 获取玩家列表 """
    from ..api.entityModule import _serverGetAllPlayerId
    return _serverGetAllPlayerId()

def GetIntPos(pos: tuple) -> tuple:
    """ 获取整数位置 """
    from math import floor
    return (floor(pos[0]), floor(pos[1]), floor(pos[2]))