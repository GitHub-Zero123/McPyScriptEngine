from ...systemManager import BaseSystem, SystemManager
from ...eventManager import EngineEventManager
from ...utils import packSystemPacket, decodeJsonPacket
from ...api import network

class ClientSystem(BaseSystem):
    def NotifyToServer(self, eventName: str, sendData: dict):
        """
        广播服务器事件
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        return ClientSystemManager.getInstance().sendToServer((self._namespace, self._systemName, eventName), sendData)

    def BroadcastEvent(self, eventName: str, sendData: dict):
        """ 本地广播事件 """
        return ClientSystemManager.getInstance()._eventBus.callEvent((self._namespace, self._systemName, eventName), sendData)
    
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
        import PyMCBridge.ModLoader as ModLoader # type: ignore
        ModLoader.regClientDestroyHandler(self.onDestroy)
        self.initNetworkEvent()
    
    def onDestroy(self):
        self.clear()

    def initNetworkEvent(self):
        """
        初始化网络事件监听
        """
        self._eventBus.nativeListen(-1, self.networkPacketReceived)
        # self._eventBus.regEventFuncHandler(-1, self.networkPacketReceived)
        # self._eventBus.nativeEventUpdate(-1)

    def sendToServer(self, eventData: object, sendData: dict):
        """
        发送事件到服务器
        :param eventName: 事件名称
        :param sendData: 数据参数
        """
        return network._clientSendMsgToServer(packSystemPacket(eventData, sendData))

    def networkPacketReceived(self, packet: dict):
        """
        网络包接收事件
        :param packet: 网络包对象
        """
        packetDict = decodeJsonPacket(packet)
        eventData = packetDict.get("msg")
        if not isinstance(eventData, dict):
            return
        if eventData.get("typeId", -1) != 0:
            # 忽略处理非系统事件
            return
        event = eventData["event"]
        data = eventData["data"]
        # 调用事件总线处理事件
        self._eventBus.callEvent(event, data)

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