from ..api.entityModule import (
    _serverCheckIsPlayer,
    _serverCheckEntityAlive,
    _serverDestroyEntity,
    _serverKillEntity,
    _serverGetEntityTypeName,
)

class Entity:
    def __init__(self, entityId: str, isClientSide: bool=False):
        self.entityId = entityId
        self._isClientSide = isClientSide

    def getIsClientSide(self):
        """
        返回当前实体对象是否来自客户端
        """
        return self._isClientSide

    def getIsServerSide(self):
        """
        返回当前实体对象是否来自服务端
        """
        return not self._isClientSide

    def getTypeName(self):
        """
        获取实体类型名(如: minecraft:zombie)
        """
        return "Unknow"
    
    def isAlive(self):
        """
        检查当前实体是否存活
        """
        return False
    
    def isPlayer(self):
        """
        判断当前实体是否为玩家
        """
        return False
    
    def asServerEntity(self) -> 'ServerEntity':
        return self
    
    def asClientEntity(self) -> 'ClientEntity':
        return self

class ClientEntity(Entity):
    def __init__(self, entityId):
        super().__init__(entityId, True)

    def getTypeName(self):
        if not self.entityId:
            return ""
        return ""

    def isAlive(self):
        if not self.entityId:
            return False
        return False

    def isPlayer(self):
        if not self.entityId:
            return False
        return False

class ServerEntity(Entity):
    def __init__(self, entityId):
        super().__init__(entityId, False)

    def getTypeName(self):
        if not self.entityId:
            return ""
        return _serverGetEntityTypeName(self.entityId)

    def isAlive(self):
        if not self.entityId:
            return False
        return _serverCheckEntityAlive(self.entityId)

    def kill(self):
        return _serverKillEntity(self.entityId)

    def destroy(self):
        return _serverDestroyEntity(self.entityId)

    def isPlayer(self):
        if not self.entityId:
            return False
        return _serverCheckIsPlayer(self.entityId)

def CREATE_SIDE_ENTITY(entityId: str, isClientSide: bool=False) -> Entity:
    """
    创建一个实体对象
    :param entityId: 实体ID
    :param isClientSide: 是否为客户端实体
    :return: Entity对象
    """
    if isClientSide:
        return ClientEntity(entityId)
    else:
        return ServerEntity(entityId)