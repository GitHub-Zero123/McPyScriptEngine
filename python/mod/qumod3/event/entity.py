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

class _SERVER_DAMAGE_PRE(BaseServerEvent):
    def __init__(self, dic: dict):
        super().__init__()
        self.entityId = dic.get("entityId", "")
        self.srcId = dic.get("srcId", "")
        self._srcObj = None
        self._projectileObj = None
        self._entityObj = None
        self.args = dic

    def getEntity(self) -> ServerEntity:
        if self._entityObj is None:
            self._entityObj = ServerEntity(self.entityId)
        return self._entityObj

    def getAttacker(self) -> ServerEntity | None:
        if not self.srcId:
            return None
        if self._srcObj is None:
            self._srcObj = ServerEntity(self.srcId)
        return self._srcObj

    def getDamage(self) -> float:
        """
        获取受伤的伤害值
        :return: 伤害值
        """
        return self.args.get("damage", 0.0)

    def setDamage(self, damage: float):
        """
        设置受伤的伤害值
        :param damage: 伤害值
        """
        self.args["damage"] = damage

    def getProjectile(self) -> ServerEntity | None:
        """
        获取投射物实体(如果存在)
        :return: 投射物实体或None
        """
        projectileId = self.args.get("projectileId", "")
        if not projectileId:
            return None
        if self._projectileObj is None:
            self._projectileObj = ServerEntity(projectileId)
        return self._projectileObj

class DamageEvent(_SERVER_DAMAGE_PRE):
    """
    服务端实体受伤事件
    """
    _NATIVE_ID = SERVER_EVENT.LIVING_INCOMING_DAMAGE

    def isFireDamage(self) -> bool:
        """
        获取是否为火焰伤害
        :return: 是否为火焰伤害
        """
        return self.args.get("ignite", False)

    def setCanceled(self):
        """
        设置事件为取消状态
        """
        self.args["knock"] = False
        self.args["damage"] = 0.0

class ActuallyHurtServerEvent(_SERVER_DAMAGE_PRE):
    """
    服务端实体实际受伤事件，在此事件下可以拿到经过护甲计算后的伤害值
    """
    _NATIVE_ID = SERVER_EVENT.LIVING_DAMAGE_PRE

class ActorHurtServerEvent(BaseServerEvent):
    """
    服务端实体最终伤害事件，此时伤害已经产生，为只读数据
    """
    _NATIVE_ID = SERVER_EVENT.LIVING_DAMAGE_POST

    def __init__(self, dic: dict):
        super().__init__()
        self.entityId = dic.get("entityId", "")
        self._entityObj = None
        self.args = dic

    def getEntity(self) -> ServerEntity:
        if self._entityObj is None:
            self._entityObj = ServerEntity(self.entityId)
        return self._entityObj

    def getDamage(self) -> float:
        """
        获取最终伤害值
        :return: 最终伤害值
        """
        return self.args.get("damage", 0.0)