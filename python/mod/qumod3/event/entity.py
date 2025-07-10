from .base import BaseServerEvent, BaseClientEvent, SERVER_EVENT, CLIENT_EVENT
from ..entity import ServerEntity, ClientEntity
lambda: "By Zero123"

class _ENTITY_JOIN_LEVEL:
    def __init__(self, dic: dict):
        self.args = dic
        self.entityId = dic.get("id", "")
        self.posX: float = dic.get("posX", 0.0)
        self.posY: float = dic.get("posY", 0.0)
        self.posZ: float = dic.get("posZ", 0.0)
    
    def getPos(self) -> tuple:
        """
        获取实体位置
        :return: (x, y, z)
        """
        return (self.posX, self.posY, self.posZ)

    def getDimensionId(self) -> int:
        """
        获取实体所在维度ID
        :return: 维度ID
        """
        return self.args.get("dimensionId", 0)
    
    def getEntityIsBaby(self) -> bool:
        """
        获取实体是否为幼年
        :return: 幼年状态
        """
        return self.args.get("isBaby", False)

    def getEngineTypeStr(self):
        """
        获取实体引擎类型字符串
        :return: 引擎类型字符串(实体identifier)
        """
        return self.args.get("engineTypeStr", "")

    def getItemName(self):
        """
        获取实体物品名称(仅当为物品时存在)
        :return: 物品identifier
        """
        return self.args.get("itemName", "")

class AddEntityServerEvent(BaseServerEvent, _ENTITY_JOIN_LEVEL):
    """
    服务端实体加入世界事件
    """
    _NATIVE_ID = SERVER_EVENT.ENTITY_JOIN_LEVEL

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ServerEntity:
        if self._entityObj is None:
            self._entityObj = ServerEntity(self.entityId)
        return self._entityObj

class AddEntityClientEvent(BaseClientEvent, _ENTITY_JOIN_LEVEL):
    """
    客户端实体加入世界事件
    """
    _NATIVE_ID = CLIENT_EVENT.ENTITY_JOIN_LEVEL

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ClientEntity:
        if self._entityObj is None:
            self._entityObj = ClientEntity(self.entityId)
        return self._entityObj

class _ENTITY_LEAVE_LEVEL:
    def __init__(self, dic: dict):
        self.entityId = dic.get("id", "")

class EntityRemoveEvent(BaseServerEvent, _ENTITY_LEAVE_LEVEL):
    """
    服务端实体移除事件(析构)
    """
    _NATIVE_ID = SERVER_EVENT.ENTITY_LEAVE_LEVEL

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ServerEntity:
        if self._entityObj is None:
            self._entityObj = ServerEntity(self.entityId)
        return self._entityObj

class RemoveEntityClientEvent(BaseClientEvent, _ENTITY_LEAVE_LEVEL):
    """
    客户端实体移除事件(析构)
    """
    _NATIVE_ID = CLIENT_EVENT.ENTITY_LEAVE_LEVEL

    def __init__(self, dic):
        super().__init__(dic)
        self._entityObj = None

    def getEntity(self) -> ClientEntity:
        if self._entityObj is None:
            self._entityObj = ClientEntity(self.entityId)
        return self._entityObj