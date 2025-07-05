from ...systemManager import BaseSystem, SystemManager
from ...eventManager import EngineEventManager

class ClientSystem(BaseSystem):
    def NotifyToServer(self, eventName: str, sendData: dict):
        """
        广播服务器事件
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        pass

    def ListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        return ClientSystemManager.getInstance().listenForEvent((namespace, systemName, eventName), func, priority)

    def UnListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        return ClientSystemManager.getInstance().unListenForEvent((namespace, systemName, eventName), func, priority)
    
    def _onSystemInit(self):
        self.ListenForEvent("Minecraft", "Engine", "OnScriptTickClient", self, self.Update)

class EventBus(EngineEventManager):
    def _initNativeEventListener(self, eventId=-1):
        import PyMCBridge.EventListener as EventListener # type: ignore
        def nativeCallHandler(*args):
            self.callEvent(eventId, *args)
        EventListener.listenForClientEvent(eventId, nativeCallHandler)

class ClientSystemManager(SystemManager):
    _INSTANCE = None

    @staticmethod
    def getInstance():
        if not ClientSystemManager._INSTANCE:
            ClientSystemManager._INSTANCE = ClientSystemManager()
        return ClientSystemManager._INSTANCE

    def __init__(self):
        super().__init__()
        self._eventBus = EventBus()

    def initNetworkEvent(self):
        """
        初始化网络事件监听
        """
        self._eventBus.regEventFuncHandler(-1, self.networkPacketReceived)
        self._eventBus.nativeEventUpdate(-1)

    def networkPacketReceived(self, packet: str):
        """
        网络包接收事件
        :param packet: 网络包对象
        """
        pass

    def listenForEvent(self, eventName: object, callback: 'function', priority: int = 0):
        """
        监听事件
        :param eventName: 事件名称
        :param callback: 回调函数
        """
        return self._eventBus.regEventFuncHandler(eventName, callback, priority)

    def unListenForEvent(self, eventName: object, callback: 'function', priority: int = 0):
        """
        取消监听事件
        :param eventName: 事件名称
        :param callback: 回调函数
        """
        return self._eventBus.unRegEventFuncHandler(eventName, callback, priority)