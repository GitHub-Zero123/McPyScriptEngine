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

class LoadServerAddonScriptsAfter(BaseServerEvent):
    """
    服务端MOD加载完成事件
    """
    _NATIVE_ID = SERVER_EVENT.MOD_LOAD_FINISH

class LoadClientAddonScriptsAfter(BaseClientEvent):
    """
    客户端MOD加载完成事件
    """
    _NATIVE_ID = CLIENT_EVENT.MOD_LOAD_FINISH