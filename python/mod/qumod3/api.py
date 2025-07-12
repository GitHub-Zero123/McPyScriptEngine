from .event.base import BaseEvent
from ..common.timer import TimerManager
import PyMCBridge.ModLoader as _ModLoader # type: ignore
lambda: "By Zero123"

def getFuncBindEvent(func: 'function') -> type[BaseEvent]:
    EventTypeCls = next(iter(func.__annotations__.values()))
    if not issubclass(EventTypeCls, BaseEvent):
        raise TypeError(f"EventBus only accepts subclasses of BaseEvent, got {EventTypeCls.__name__}")
    return EventTypeCls

def SubscribeEvent(func: 'function'):
    """
        装饰器 注册事件总线事件
    """
    getFuncBindEvent(func)._regListen(func)
    return func

def ServerInit(func):
    """ 注册服务端初始化函数(仅在modMain生效) """
    _ModLoader.regServerLoaderHandler(func)
    return func

def ClientInit(func):
    """ 注册客户端初始化函数(仅在modMain生效) """
    _ModLoader.regClientLoaderHandler(func)
    return func

def ServerDestroy(func):
    """ 注册服务端销毁函数(支持动态注册) """
    _ModLoader.regServerDestroyHandler(func)
    return func

def ClientDestroy(func):
    """ 注册客户端销毁函数(支持动态注册) """
    _ModLoader.regClientDestroyHandler(func)
    return func

def getThreadLocalTimer() -> TimerManager:
    """ 获取全局定时管理器(在不同线程下获取返回不同实例) """
    if _ModLoader.isServerThread():
        from ..common.timer import ServerTimerManager
        return ServerTimerManager.getInstance()
    else:
        from ..common.timer import ClientTimerManager
        return ClientTimerManager.getInstance()

def regFuncListener(func: 'function'):
    """ 动态注册事件监听函数 """
    getFuncBindEvent(func)._regListen(func)

def unRegFuncListener(func: 'function'):
    """ 动态取消注册事件监听函数 """
    getFuncBindEvent(func)._unRegListen(func)