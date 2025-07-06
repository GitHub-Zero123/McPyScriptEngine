from ..common.timer import TimerManager, TimerTask
from functools import lru_cache

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