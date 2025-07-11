from ..api import (
    entityModule as _entityModule,
    world as _worldModule
)
from ..common.timer import ServerTimerManager, TimerTask
from functools import lru_cache
lambda: "By Zero123"

class EntityPosComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def SetPos(self, value: tuple):
        """ 设置实体位置 """
        return _entityModule._serverSetEntityPos(self.entityId, value)

    def GetPos(self):
        """ 获取实体位置 """
        return _entityModule._serverGetEntityPos(self.entityId)

class EntityRotComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetRot(self):
        """ 获取实体旋转欧拉角 """
        return _entityModule._serverGetEntityRot(self.entityId)

class ProjectileComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def CreateProjectileEntity(self, spawnerId: str, entityIdentifier: str, param: dict=None):
        """ 创建并发射投掷物(param参数参考网易文档) """
        if param is None:
            param = {}
        return _entityModule._serverShootProjectile(spawnerId, entityIdentifier, param)

class EngineTypeComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetEngineTypeStr(self):
        """ 获取实体类型名称(标识符) """
        return _entityModule._serverGetEntityTypeName(self.entityId)

class GameEngineComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def IsEntityAlive(self, entityId: str):
        """ 检查实体是否存活 """
        return _entityModule._serverCheckEntityAlive(entityId)

    def KillEntity(self, entityId: str):
        """ 杀死实体 """
        return _entityModule._serverKillEntity(entityId)

    def AddTimer(self, delay: float, func: 'function', *args, **kwargs) -> TimerTask:
        """ 添加定时器 """
        return ServerTimerManager.getInstance().addFuncTask(lambda: func(*args, **kwargs), int(round(delay * 20)))

    def AddRepeatedTimer(self, delay: float, func: 'function', *args, **kwargs) -> TimerTask:
        """ 添加重复定时器 """
        return ServerTimerManager.getInstance().addFuncTask(lambda: func(*args, **kwargs), int(round(delay * 20)), repeat=True)

    def CancelTimer(self, task: TimerTask):
        """ 取消定时器 """
        return ServerTimerManager.getInstance().removeTask(task)

class CommandComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def SetCommand(self, cmdStr: str, entityId: str="", showOutput: bool=False):
        """ 设置执行命令 """
        if cmdStr.startswith("/"):
            cmdStr = cmdStr[1:]
        return _entityModule._setCommand(cmdStr, entityId, showOutput)

class ActionComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetAttackTarget(self):
        """ 获取目标实体ID """
        return _entityModule._serverGetEntityTargetId(self.entityId)

class MsgComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def NotifyOneMessage(self, playerId: str, msg: str, color: str=""):
        """ 给指定玩家发送消息 """
        return _entityModule._serverSendMessage(playerId, color+msg)

class DimensionComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetEntityDimensionId(self):
        """ 获取实体所在维度ID, 异常返回-1, 原版维度返回0-2, 三方JE自定义维度返回其他映射负数值(仅运行时临时分配) """
        return _entityModule._serverGetEntityDmId(self.entityId)

class BlockStateComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

class BlockInfoComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def GetBlockNew(self, pos: tuple[int, int, int], dimensionId: int=0):
        """
        获取某一位置的方块信息
        :param pos: 方块位置坐标
        :param dimensionId: 维度ID
        :return: 方块信息字典, 例如 {"name": "minecraft:stone", "aux": 0}
        注意：若方块所在区域未加载将返回空气
        """
        return _worldModule._serverGetBlock(pos, dimensionId)

    def SetBlockNew(self,
            pos: tuple[int, int, int],
            blockDict: dict,
            oldBlockHandling: int=0,
            dimensionId: int=0,
            isLegacy: bool=False,   # 在JE废弃该参数
            updateNeighbors: bool=True
        ):
        """
        设置某一位置方块
        :param pos: 方块位置坐标
        :param blockDict: 方块数据字典, 例如 {"name": "minecraft:stone"}}
        :param oldBlockHandling: 旧方块处理方式, 0-替换, 1-破坏, 2-保留
        :param dimensionId: 维度ID
        :param isLegacy: 该参数在JE中不存在
        :param updateNeighbors: 是否更新邻近方块
        """
        return _worldModule._serverSetBlock(pos, blockDict, oldBlockHandling, dimensionId, updateNeighbors)

class EngineCompFactory:
    # 实现网易组件工厂
    @lru_cache(80)
    def CreateItem(self, entityId: str):
        pass

    @lru_cache(80)
    def CreatePos(self, entityId: str):
        return EntityPosComp(entityId)
    
    @lru_cache(80)
    def CreateRot(self, entityId: str):
        return EntityRotComp(entityId)
    
    @lru_cache(80)
    def CreateProjectile(self, levelId: str):
        return ProjectileComp(levelId)
    
    @lru_cache(80)
    def CreateEngineType(self, entityId: str):
        return EngineTypeComp(entityId)

    @lru_cache(80)
    def CreateGame(self, levelId: str):
        return GameEngineComp(levelId)
    
    @lru_cache(80)
    def CreateCommand(self, levelId: str):
        return CommandComp(levelId)
    
    @lru_cache(80)
    def CreateAction(self, entityId: str):
        return ActionComp(entityId)

    @lru_cache(80)
    def CreateMsg(self, entityId: str):
        return MsgComp(entityId)
    
    @lru_cache(80)
    def CreateDimension(self, entityId: str):
        return DimensionComp(entityId)
    
    @lru_cache(80)
    def CreateBlockState(self, levelId: str):
        return BlockStateComp(levelId)

    @lru_cache(80)
    def CreateBlockInfo(self, levelId: str):
        return BlockInfoComp(levelId)