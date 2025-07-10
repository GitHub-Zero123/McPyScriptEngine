from ..api.entityModule import (
    _serverSetEntityPos,
    _serverGetEntityPos,
    _serverGetEntityRot,
    _serverShootProjectile,
    _serverGetEntityTypeName,
    _serverCheckEntityAlive,
    _serverKillEntity,
    _serverGetEntityTargetId,
    _serverSendMessage,
    _setCommand,
)
from ..common.timer import ServerTimerManager, TimerTask
from functools import lru_cache
lambda: "By Zero123"

class EntityPosComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def SetPos(self, value: tuple):
        """ 设置实体位置 """
        return _serverSetEntityPos(self.entityId, value)

    def GetPos(self):
        """ 获取实体位置 """
        return _serverGetEntityPos(self.entityId)

class EntityRotComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetRot(self):
        """ 获取实体旋转欧拉角 """
        return _serverGetEntityRot(self.entityId)

class ProjectileComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def CreateProjectileEntity(self, spawnerId: str, entityIdentifier: str, param: dict=None):
        """ 创建并发射投掷物(param参数参考网易文档) """
        if param is None:
            param = {}
        return _serverShootProjectile(spawnerId, entityIdentifier, param)

class EngineTypeComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetEngineTypeStr(self):
        """ 获取实体类型名称(标识符) """
        return _serverGetEntityTypeName(self.entityId)

class GameEngineComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def IsEntityAlive(self, entityId: str):
        """ 检查实体是否存活 """
        return _serverCheckEntityAlive(entityId)

    def KillEntity(self, entityId: str):
        """ 杀死实体 """
        return _serverKillEntity(entityId)

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
        return _setCommand(cmdStr, entityId, showOutput)

class ActionComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetAttackTarget(self):
        """ 获取目标实体ID """
        return _serverGetEntityTargetId(self.entityId)

class MsgComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def NotifyOneMessage(self, playerId: str, msg: str, color: str=""):
        """ 给指定玩家发送消息 """
        return _serverSendMessage(playerId, color+msg)

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