from ..api import (
    entityModule as _entityModule,
    item as _itemModule,
)
import PyMCBridge.ModLoader as _ModLoader # type: ignore
import PyMCBridge.Math as _Math # type: ignore
from .item import Item
lambda: "By Zero123"

class _PositionComp:
    def __init__(self, entityId):
        self._entityId = entityId

    def getPos(self) -> tuple | None:
        """ 获取当前实体位置 """
        if not self._entityId:
            return None
        if _ModLoader.isClientThread():
            return _entityModule._clientGetEntityPos(self._entityId)
        return _entityModule._serverGetEntityPos(self._entityId)

    def setPos(self, value: tuple):
        """
        设置当前实体位置
        :param value: (x, y, z) 坐标元组
        """
        if _ModLoader.isClientThread():
            return None
        return _entityModule._serverSetEntityPos(self._entityId, value)

class _RotationComp:
    def __init__(self, entityId):
        self._entityId = entityId

    def getRotation(self) -> tuple | None:
        """ 获取当前实体旋转 """
        if not self._entityId:
            return None
        if _ModLoader.isClientThread():
            return _entityModule._clientGetEntityRot(self._entityId)
        return _entityModule._serverGetEntityRot(self._entityId)

    def setRotation(self, value: tuple):
        """
        设置当前实体旋转
        :param value: (yaw, pitch) 旋转元组
        """
        if _ModLoader.isClientThread():
            return None
        return None

    def getRotDir(self) -> tuple | None:
        """
        获取当前实体旋转朝向
        :return: (x, y, z)
        """
        rot = self.getRotation()
        if not rot:
            return None
        return _Math._entityRotToDir(rot[0], rot[1])

    def getBodyRotDir(self) -> tuple | None:
        """
        获取当前实体身体旋转朝向
        :return: (x, y, z)
        """
        rot = self.getRotation()
        if not rot:
            return None
        return _Math._entityRotToDir(0, rot[1])

class Entity:
    def __init__(self, entityId: str, isClientSide: bool=False):
        self.entityId = entityId
        self._isClientSide = isClientSide
        self._position = None
        self._rotation = None

    def __eq__(self, value):
        return isinstance(value, Entity) and self.entityId == value.entityId

    def __hash__(self):
        return hash(self.entityId)

    @property
    def position(self):
        """ 实体位置管理 """
        if self._position is None:
            self._position = _PositionComp(self.entityId)
        return self._position

    @property
    def rotation(self):
        """ 实体旋转管理 """
        if self._rotation is None:
            self._rotation = _RotationComp(self.entityId)
        return self._rotation

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

    @property
    def identifier(self):
        """
        实体命名标识符
        """
        return self.getTypeName()

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

    def sendMessage(self, msg: str):
        """
        向当前玩家发送消息(仅对玩家生效)
        """
        if not self.entityId:
            return
        if _ModLoader.isClientThread():
            if self.entityId != _entityModule._clientGetLocalPlayerId():
                raise RuntimeError("客户端实体只能向本地玩家发送消息")
            _entityModule._clientSendMessage(msg)
            return
        _entityModule._serverSendMessage(self.entityId, msg)

    def asServerEntity(self) -> 'ServerEntity':
        return self
    
    def asClientEntity(self) -> 'ClientEntity':
        return self

    @staticmethod
    def getWorldEntities() -> list['Entity']:
        raise RuntimeError("This method should be overridden in subclasses")
    
    @staticmethod
    def getAllPlayer() -> list['Entity']:
        raise RuntimeError("This method should be overridden in subclasses")

class ClientEntity(Entity):
    def __init__(self, entityId):
        super().__init__(entityId, True)

    def getTypeName(self):
        if not self.entityId:
            return ""
        return _entityModule._clientGetEntityTypeName(self.entityId)

    def isAlive(self):
        if not self.entityId:
            return False
        return _entityModule._clientCheckEntityAlive(self.entityId)

    def hasEntity(self):
        return self.isAlive()

    def isPlayer(self):
        if not self.entityId:
            return False
        return _entityModule._clientCheckIsPlayer(self.entityId)

    @staticmethod
    def getWorldEntities() -> list['ClientEntity']:
        """ 获取客户端世界中的所有实体(渲染区块内的) """
        return [ClientEntity(entityId) for entityId in _entityModule._clientGetWorldEntityList()]

    @staticmethod
    def getAllPlayer() -> list['ClientEntity']:
        raise RuntimeError("客户端尚且不支持此功能")

    @staticmethod
    def getLocalPlayer() -> 'ClientEntity':
        """ 获取本地玩家实体对象"""
        return ClientEntity(_entityModule._clientGetLocalPlayerId())

class ProjectileOptions:
    """
    抛射物配置类
    :param position: 抛射物初始位置 (x, y, z)
    :param direction: 抛射物初始方向 (x, y, z)
    :param power: 抛射物的初始力量
    :param isDamageOwner: 是否伤害创建者(默认False)
    """
    def __init__(
        self,
        identifier: str,
        position: tuple[float, float, float],
        direction: tuple[float, float, float],
        power: float = 1.0,
        isDamageOwner: bool = False
    ):
        self.identifier = identifier
        self.position = position
        self.direction = direction
        self.power = power
        self.isDamageOwner = isDamageOwner

    def packData(self) -> dict:
        """
        将配置打包成字典
        :return: 配置字典
        """
        return {
            "position": self.position,
            "direction": self.direction,
            "power": self.power,
            "isDamageOwner": self.isDamageOwner
        }
    
    def setIdentifier(self, identifier: str):
        """
        设置抛射物标识符
        :param identifier: 抛射物标识符字符串
        """
        self.identifier = identifier
        return self

    def setPosition(self, position: tuple[float, float, float]):
        """
        设置抛射物初始位置
        :param position: (x, y, z) 坐标元组
        """
        self.position = position
        return self
    
    def setDirection(self, direction: tuple[float, float, float]):
        """
        设置抛射物初始方向
        :param direction: (x, y, z) 方向元组
        """
        self.direction = direction
        return self
    
    def setPower(self, power: float):
        """
        设置抛射物的初始力量
        :param power: 力量值
        """
        self.power = power
        return self
    
    def setDamageOwner(self, isDamageOwner: bool):
        """
        设置是否伤害创建者
        :param isDamageOwner: 是否伤害创建者
        """
        self.isDamageOwner = isDamageOwner
        return self

class _ProjectileComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def create(self, options: ProjectileOptions) -> bool:
        """
        创建抛射物
        :param options: ProjectileOptions对象
        :return: 是否创建成功
        """
        if not self.entityId:
            return False
        return _entityModule._serverShootProjectile(self.entityId, options.identifier, options.packData())

class ServerEntity(Entity):
    def __init__(self, entityId):
        super().__init__(entityId, False)
        self._projectileComp = None

    @property
    def projectile(self) -> _ProjectileComp:
        """
        获取抛射物组件
        :return: ProjectileComp对象
        """
        if self._projectileComp is None:
            self._projectileComp = _ProjectileComp(self.entityId)
        return self._projectileComp

    def getTypeName(self):
        if not self.entityId:
            return ""
        return _entityModule._serverGetEntityTypeName(self.entityId)

    def isAlive(self):
        if not self.entityId:
            return False
        return _entityModule._serverCheckEntityAlive(self.entityId)

    def kill(self):
        if not self.entityId:
            return False
        return _entityModule._serverKillEntity(self.entityId)

    def destroy(self):
        if not self.entityId:
            return False
        return _entityModule._serverDestroyEntity(self.entityId)

    def isPlayer(self):
        if not self.entityId:
            return False
        return _entityModule._serverCheckIsPlayer(self.entityId)

    def setCommand(self, command: str, showOutput: bool=False):
        """
        设置实体执行命令(仅限服务端)
        :param command: 命令字符串
        """
        if not self.entityId:
            return False
        if command.startswith("/"):
            command = command[1:]
        return _entityModule._setCommand(command, self.entityId, showOutput)

    def getTargetEntity(self):
        # type: () -> 'ServerEntity | None'
        """
        获取实体的目标实体
        :return: 目标实体对象或None
        """
        if not self.entityId:
            return None
        targetId = _entityModule._serverGetEntityTargetId(self.entityId)
        if not targetId:
            return None
        return ServerEntity(targetId)

    def getDimensionId(self) -> int:
        """
        获取实体所在维度ID, 异常返回-1, 原版维度返回0-2, 三方JE自定义维度返回其他映射负数值(仅运行时临时分配)
        :return: 维度ID
        """
        if not self.entityId:
            return -1
        return _entityModule._serverGetEntityDmId(self.entityId)

    @staticmethod
    def getWorldEntities() -> list['ServerEntity']:
        """ 获取服务端世界中的所有实体 """
        return [ServerEntity(entityId) for entityId in _entityModule._serverGetWorldEntityList()]

    @staticmethod
    def getAllPlayer() -> list['ServerEntity']:
        return [ServerEntity(entityId) for entityId in _entityModule._serverGetAllPlayerId()]

    def getMainHandItem(self) -> Item:
        """ 获取实体主手物品 """
        itemInfo = _itemModule._serverGetEntityHandItemInfo(self.entityId)
        if not itemInfo:
            return Item()
        return Item(itemInfo["newItemName"])

    def _toServerPlayer(self) -> 'ServerPlayer':
        """
        转换为服务端玩家实体对象(不会检查是否真是玩家实体)
        :return: ServerPlayer对象
        """
        return ServerPlayer(self.entityId)

    def toServerPlayer(self) -> 'ServerPlayer':
        """
        转换为服务端玩家实体对象
        :return: ServerPlayer对象
        """
        if not self.isPlayer():
            raise RuntimeError("当前实体不是玩家实体")
        return self._toServerPlayer()

class PlayerAction:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def destroyBlock(self, pos: tuple[int, int, int]) -> bool:
        """
        尝试破坏特定位置的方块
        :param pos: 方块位置 (x, y, z)
        :return: 是否成功破坏方块
        """
        return _entityModule._serverPlayerDestroyBlock(self.entityId, pos)

class ServerPlayer(ServerEntity):
    """
    服务端玩家实体类
    """
    def __init__(self, entityId: str):
        super().__init__(entityId)
        self._playerAction: PlayerAction | None = None

    @property
    def action(self) -> PlayerAction:
        """
        获取玩家行为组件
        :return: PlayerAction对象
        """
        if not self._playerAction:
            self._playerAction = PlayerAction(self.entityId)
        return self._playerAction

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