from .base import BaseServerEvent, BaseClientEvent, SERVER_EVENT, CLIENT_EVENT

class OnScriptTickServer(BaseServerEvent):
    """
    服务端脚本Tick事件
    """
    _NATIVE_ID = SERVER_EVENT.SERVER_TICK_POST

class OnScriptTickClient(BaseClientEvent):
    """
    客户端脚本Tick事件
    """
    _NATIVE_ID = CLIENT_EVENT.CLIENT_TICK_POST