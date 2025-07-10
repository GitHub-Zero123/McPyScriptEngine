from ..api.entityModule import (
    _clientCheckEntityAlive,
    _clientGetEntityPos,
    _clientGetEntityRot,
    _clientGetEntityTypeName,
)
from ..common.timer import TimerManager, TimerTask
from functools import lru_cache
lambda: "By Zero123"

class GameEngineComp:
    def __init__(self, levelId: str):
        self.levelId = levelId

    def AddTimer(self, delay: float, func: 'function', *args, **kwargs) -> TimerTask:
        """ 添加定时器 """
        return GameTimer.getInstance().addFuncTask(lambda: func(*args, **kwargs), int(round(delay * 20)))

    def AddRepeatedTimer(self, delay: float, func: 'function', *args, **kwargs) -> TimerTask:
        """ 添加重复定时器 """
        return GameTimer.getInstance().addFuncTask(lambda: func(*args, **kwargs), int(round(delay * 20)), repeat=True)

    def CancelTimer(self, task: TimerTask):
        """ 取消定时器 """
        return GameTimer.getInstance().removeTask(task)
    
    def HasEntity(self, entityId: str) -> bool:
        """ 检查实体是否存在 """
        return _clientCheckEntityAlive(entityId)

    def IsEntityAlive(self, entityId: str) -> bool:
        """ 检查实体是否存活 """
        return _clientCheckEntityAlive(entityId)

class EngineTypeComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetEngineTypeStr(self):
        """ 获取实体类型名称(标识符) """
        return _clientGetEntityTypeName(self.entityId)

class EntityPosComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetPos(self):
        """ 获取实体位置 """
        return _clientGetEntityPos(self.entityId)

class EntityRotComp:
    def __init__(self, entityId: str):
        self.entityId = entityId

    def GetRot(self):
        """ 获取实体旋转欧拉角 """
        return _clientGetEntityRot(self.entityId)

class GameTimer(TimerManager):
    _INSTANCE = None

    @staticmethod
    def getInstance():
        if GameTimer._INSTANCE is None:
            GameTimer._INSTANCE = GameTimer()
        return GameTimer._INSTANCE

    def __init__(self):
        super().__init__()
        from .system.clientSystem import ClientSystemManager
        ClientSystemManager.getInstance().listenForEvent(("Minecraft", "Engine", "OnScriptTickClient"), self.update)

class EngineCompFactory:
    def CreateItem(self, entityId: str):
        pass

    @lru_cache(80)
    def CreateGame(self, levelId: str):
        return GameEngineComp(levelId)

    @lru_cache(80)
    def CreatePos(self, entityId: str):
        return EntityPosComp(entityId)
    
    @lru_cache(80)
    def CreateRot(self, entityId: str):
        return EntityRotComp(entityId)
    
    @lru_cache(80)
    def CreateEngineType(self, entityId: str):
        return EngineTypeComp(entityId)