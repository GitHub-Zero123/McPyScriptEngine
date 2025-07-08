from ..utils import importModule, entityRotToDir
from .system.clientSystem import (
    ClientSystem,
    ClientSystemManager,
)
from functools import lru_cache
lambda: "Extra Client API"

def RegisterSystem(namespace: str, systemName: str, clsPath: str) -> object:
    return ClientSystemManager.getInstance().registerClsPath(namespace, systemName, clsPath)

def GetSystem(namespace: str, systemName: str) -> object:
    return ClientSystemManager.getInstance().getSystem((namespace, systemName))

def GetLocalPlayerId() -> str:
    """ 获取本地玩家ID """
    return ""

def GetLevelId() -> str:
    return ""

@lru_cache(1)
def GetEngineCompFactory():
    """ 获取引擎组件工厂 """
    from .compFactory import EngineCompFactory
    return EngineCompFactory()

def GetClientSystemCls():
    """ 获取客户端系统类 """
    return ClientSystem

def GetEngineNamespace() -> str:
    """ 获取引擎命名空间 """
    return "Minecraft"

def GetEngineSystemName() -> str:
    """ 获取引擎系统名称 """
    return "Engine"

def ImportModule(filePath: str) -> object:
    """ 客户端文件导入 """
    return importModule(filePath)

def GetDirFromRot(rot: tuple) -> tuple:
    return entityRotToDir(rot)

def GetIntPos(pos: tuple) -> tuple:
    """ 获取整数位置 """
    from math import floor
    return (floor(pos[0]), floor(pos[1]), floor(pos[2]))