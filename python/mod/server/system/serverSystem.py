from ...systemManager import BaseSystem, SystemManager
from ...eventManager import EngineEventManager

class ServerSystem(BaseSystem):
    def BroadcastToAllClient(self, eventName: str, sendData: dict):
        """
        广播事件到所有客户端
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        pass

    def NotifyToClient(self, playerId: str, eventName: str, sendData: dict):
        """
        通知特定客户端
        :param playerId: 玩家ID
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        pass

    def NotifyToMultiClients(self, playerListId: list, eventName: str, sendData: dict):
        """
        通知多个客户端
        :param playerListId: 玩家ID列表
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        pass

    def ListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        return ServerSystemManager.getInstance().listenForEvent((namespace, systemName, eventName), func, priority)

    def UnListenForEvent(self, namespace: str, systemName: str, eventName: str, parent: object, func: 'function', priority: int = 0):
        return ServerSystemManager.getInstance().unListenForEvent((namespace, systemName, eventName), func, priority)
    
    def DestroyEntity(self, entityId: str) -> bool:
        from ...api.entityModule import _serverDestroyEntity
        return _serverDestroyEntity(entityId)

    def _onSystemInit(self):
        self.ListenForEvent("Minecraft", "Engine", "OnScriptTickServer", self, self.Update)

class EventBus(EngineEventManager):
    def _initNativeEventListener(self, eventId=-1):
        import PyMCBridge.EventListener as EventListener # type: ignore
        def nativeCallHandler(*args):
            return self.callEvent(eventId, *args)
        EventListener.listenForServerEvent(eventId, nativeCallHandler)

class ServerSystemManager(SystemManager):
    _INSTANCE = None

    @staticmethod
    def getInstance():
        if not ServerSystemManager._INSTANCE:
            ServerSystemManager._INSTANCE = ServerSystemManager()
        return ServerSystemManager._INSTANCE

    def __init__(self):
        super().__init__()
        self._eventBus = EventBus()
        self.initNetworkEvent()
        import PyMCBridge.ModLoader as ModLoader # type: ignore
        ModLoader.regServerDestroyHandler(self.onDestroy)
    
    def onDestroy(self):
        self.clear()
    
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