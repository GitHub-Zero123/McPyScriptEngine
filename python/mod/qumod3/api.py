from .event.base import BaseEvent

def EventBus(func: 'function'):
    """
        装饰器 注册事件总线事件
    """
    eventTypeCls = next(iter(func.__annotations__.values()))
    if not issubclass(eventTypeCls, BaseEvent):
        raise TypeError(f"EventBus only accepts subclasses of BaseEvent, got {eventTypeCls.__name__}")
    eventTypeCls._regListen(func)
    return func