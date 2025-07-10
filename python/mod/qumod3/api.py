from .event.base import BaseEvent
import PyMCBridge.ModLoader as _ModLoader # type: ignore
lambda: "By Zero123"

def SubscribeEvent(func: 'function'):
    """
        装饰器 注册事件总线事件
    """
    eventTypeCls = next(iter(func.__annotations__.values()))
    if not issubclass(eventTypeCls, BaseEvent):
        raise TypeError(f"EventBus only accepts subclasses of BaseEvent, got {eventTypeCls.__name__}")
    eventTypeCls._regListen(func)
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