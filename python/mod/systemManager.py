from .utils import TRY_EXEC_FUNC, importChild

class BaseSystem:
    def __init__(self, namespace: str, systemName: str):
        self._namespace = namespace
        self._systemName = systemName

    def ListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        pass

    def UnListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        pass

    def Update(self):
        pass

    def _onSystemInit(self):
        pass

    def _Destroy(self):
        return self.Destroy()

    def Destroy(self):
        pass

    def BroadcastEvent(self, eventName: str, sendData: dict):
        """
        本地广播事件, 仅本地其他系统端能够接收到
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        raise NotImplementedError("BroadcastEvent method must be implemented in subclass")

    # 无用设计, 仅作兼容
    def DefineEvent(self, *_):
        pass

    def UnDefineEvent(self, *_):
        pass

    def CreateEventData(self) -> dict:
        return {}

class SystemManager:
    def __init__(self):
        self.systemMap = {} # type: dict[object, BaseSystem]

    def getSystem(self, systemKey=""):
        """ 获取系统实例 """
        return self.systemMap.get(systemKey, None)

    def regSystem(self, systemKey, system: BaseSystem):
        """ 注册系统实例 """
        if systemKey in self.systemMap:
            return False
        self.systemMap[systemKey] = system
        TRY_EXEC_FUNC(system._onSystemInit)
        return True
    
    def hasSystem(self, systemKey):
        """ 检查系统实例是否存在 """
        return systemKey in self.systemMap

    def clear(self):
        """ 清除所有系统实例 """
        for system in self.systemMap.values():
            TRY_EXEC_FUNC(system._Destroy)
        self.systemMap.clear()

    def registerClsPath(self, namespace: str, systemName: str, clsPath: str) -> object:
        """ 注册系统类路径并返回系统实例 """
        systemKey = (namespace, systemName)
        system = self.getSystem(systemKey)
        if system:
            return system
        newSystem = importChild(clsPath)(namespace, systemName)
        self.regSystem(systemKey, newSystem)
        return newSystem

    def listenForEvent(self, eventName: object, callback: 'function', priority: int = 0):
        """
        监听事件
        :param eventName: 事件名称
        :param callback: 回调函数
        """
        pass

    def unListenForEvent(self, eventName: object, callback: 'function', priority: int = 0):
        """
        取消监听事件
        :param eventName: 事件名称
        :param callback: 回调函数
        """
        pass