# -*- coding: utf-8 -*-
import PyMCBridge.ModLoader as ModLoader # type: ignore
from ..utils import Version, TRY_EXEC_FUNC
lambda: "mod.common.mod 网易MOD_SDK加载器兼容层 By Zero123"

_MOD_CLS_LIST = []  # type: list[type]

class ModScanner:
    """ MOD扫描器 """
    def __init__(self, bindCls):
        self.bindCls = bindCls
        self._version = None
        self._name = None
        self._initAnnotationMetadata = False
        self._serverInit = []
        self._clientInit = []
        self._serverDestroy = []
        self._clientDestroy = []

    def getModName(self):
        if self._name is None:
            self._name = getattr(self.bindCls, "MOD_NAME", "")
        return self._name

    def getVersion(self):
        if self._version is None:
            self._version = Version(getattr(self.bindCls, "VERSION", "1.0.0"))
        return self._version

    def tryInitAnnotationMetadata(self):
        """ 尝试初始化注解元数据 """
        if self._initAnnotationMetadata:
            return
        # 反射搜索注解方法
        bindObj = self.bindCls()
        for attrName in dir(bindObj):
            metObj = getattr(bindObj, attrName)
            if not callable(metObj):
                continue
            if hasattr(metObj, "INIT_SERVER"):
                self._serverInit.append(metObj)
            if hasattr(metObj, "INIT_CLIENT"):
                self._clientInit.append(metObj)
            if hasattr(metObj, "DESTROY_SERVER"):
                self._serverDestroy.append(metObj)
            if hasattr(metObj, "DESTROY_CLIENT"):
                self._clientDestroy.append(metObj)

    def onServerInit(self):
        """ 服务端初始化 """
        ModLoader.regServerDestroyHandler(self.onServerDestroy)
        self.tryInitAnnotationMetadata()
        for met in self._serverInit:
            TRY_EXEC_FUNC(met)

    def onClientInit(self):
        """ 客户端初始化 """
        ModLoader.regClientDestroyHandler(self.onClientDestroy)
        self.tryInitAnnotationMetadata()
        for met in self._clientInit:
            TRY_EXEC_FUNC(met)

    def onServerDestroy(self):
        """ 服务端销毁 """
        for met in self._serverDestroy:
            TRY_EXEC_FUNC(met)

    def onClientDestroy(self):
        """ 客户端销毁 """
        for met in self._clientDestroy:
            TRY_EXEC_FUNC(met)

class Mod:
    IS_MC_BINDER = True

    @staticmethod
    def Binding(name="", version="1.0.0"):
        def _Binder(cls):
            cls.MOD_NAME = name
            cls.VERSION = version
            _MOD_CLS_LIST.append(cls)
            return cls
        return _Binder

    @staticmethod
    def InitServer():
        def _Binder(cls):
            cls.INIT_SERVER = True
            return cls
        return _Binder

    @staticmethod
    def InitClient():
        def _Binder(cls):
            cls.INIT_CLIENT = True
            return cls
        return _Binder
    
    @staticmethod
    def DestroyServer():
        def _Binder(cls):
            cls.DESTROY_SERVER = True
            return cls
        return _Binder
    
    @staticmethod
    def DestroyClient():
        def _Binder(cls):
            cls.DESTROY_CLIENT = True
            return cls
        return _Binder

def SCANNER_LOAD():
    """ 扫描器加载 """
    modInfoMap = {}     # type: dict[str, ModScanner]
    for cls in _MOD_CLS_LIST:
        try:
            modObj = ModScanner(cls)
            modName = modObj.getModName()
            if not modName in modInfoMap:
                modInfoMap[modName] = modObj
                continue
            # 高版本覆盖
            if modObj.getVersion().newerThan(modInfoMap[modName].getVersion()):
                modInfoMap[modName] = modObj
        except Exception:
            import traceback
            traceback.print_exc()
    for modObj in modInfoMap.values():
        yield modObj

def ON_SERVER_INIT():
    for obj in SCANNER_LOAD():
        TRY_EXEC_FUNC(obj.onServerInit)

def ON_CLIENT_INIT():
    for obj in SCANNER_LOAD():
        TRY_EXEC_FUNC(obj.onClientInit)

ModLoader.regServerLoaderHandler(ON_SERVER_INIT)
ModLoader.regClientLoaderHandler(ON_CLIENT_INIT)