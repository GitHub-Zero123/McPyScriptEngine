from .base import BaseServerEvent, BaseClientEvent, SERVER_EVENT, CLIENT_EVENT
from ..entity import ServerEntity, ClientEntity

class _RIGHT_CLICK_ITEM:
    def __init__(self, dic: dict):
        self.playerId: str = dic.get("playerId", "")
        self.itemDict: dict = dic.get("itemDict", {})

    def getItemName(self) -> str:
        """
        获取玩家右键使用的物品名称
        :return: 物品名称
        """
        return self.itemDict.get("newItemName", "")

class ServerItemTryUseEvent(BaseServerEvent, _RIGHT_CLICK_ITEM):
    """
    服务端玩家尝试使用物品事件
    """
    _NATIVE_ID = SERVER_EVENT.RIGHT_CLICK_ITEM

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ServerEntity:
        if self._entityObj is None:
            self._entityObj = ServerEntity(self.playerId)
        return self._entityObj

class ClientItemTryUseEvent(BaseClientEvent, _RIGHT_CLICK_ITEM):
    """
    客户端玩家尝试使用物品事件
    """
    _NATIVE_ID = CLIENT_EVENT.RIGHT_CLICK_ITEM

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ClientEntity:
        if self._entityObj is None:
            self._entityObj = ClientEntity(self.playerId)
        return self._entityObj