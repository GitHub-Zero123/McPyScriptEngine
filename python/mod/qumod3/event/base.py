from ...eventManager import EventGroup, EventHandler, SERVER_EVENT, CLIENT_EVENT
from ...server.system.serverSystem import ServerSystemManager
from ...client.system.clientSystem import ClientSystemManager
lambda: "By Zero123"

class BaseEvent:
    @classmethod
    def _regListen(cls, func: 'function'):
        pass

    @classmethod
    def _unRegListen(cls, func: 'function'):
        pass

_BASIC_EVENT_GROUPS = {}    # type: dict[type[BasicEvent], EventGroup]

class BasicEvent(BaseEvent):
    _EVENT_THREAD_TYPE = 0  # 0客户端 1服务端
    _NATIVE_ID = 0  # 原生事件ID

    @classmethod
    def _regListen(cls, func):
        if cls is BasicEvent:
            raise TypeError("BasicEvent cannot be used directly, please subclass it.")
        if not cls in _BASIC_EVENT_GROUPS:
            group = EventGroup()
            _BASIC_EVENT_GROUPS[cls] = group
            cls._initEventListener(group)
        _BASIC_EVENT_GROUPS[cls].add(EventHandler(func))

    @classmethod
    def _initEventListener(cls, group: EventGroup = None):
        """
        初始化事件监听器
        """
        NATIVE_ID = cls._NATIVE_ID
        if cls._EVENT_THREAD_TYPE == 0:
            ClientSystemManager.getInstance()._eventBus.nativeListen(NATIVE_ID, lambda *args: cls._eventHandler(group, *args))
        elif cls._EVENT_THREAD_TYPE == 1:
            ServerSystemManager.getInstance()._eventBus.nativeListen(NATIVE_ID, lambda *args: cls._eventHandler(group, *args))

    @classmethod
    def _eventHandler(cls, groupRef: EventGroup, *args):
        return groupRef.call(cls(*args))

class BaseClientEvent(BasicEvent):
    _EVENT_THREAD_TYPE = 0  # 客户端事件
    _NATIVE_ID = SERVER_EVENT.UNKNOWN

class BaseServerEvent(BasicEvent):
    _EVENT_THREAD_TYPE = 1  # 服务端事件
    _NATIVE_ID = CLIENT_EVENT.UNKNOWN