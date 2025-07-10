from collections import OrderedDict # 避免版本歧义
from ..utils import TRY_EXEC_FUNC
lambda: "By Zero123"

class TimerTask:
    __slots__ = ("bindFunc", "delayTick", "repeat", "remainingTicks",)
    def __init__(self,
            bindFunc=lambda: None,
            delayTick: int = 0,
            repeat: bool = False
        ):
        self.bindFunc = bindFunc            # 绑定的函数
        self.delayTick = delayTick          # 延迟的Tick数
        self.repeat = repeat
        self.remainingTicks = delayTick     # 剩余的Tick数

class TimerManager:
    def __init__(self):
        self._tasks = OrderedDict()  # type: OrderedDict[TimerTask, None]
        self._callFuncs = []         # type: list[TimerTask]
        self._clearTasks = []        # type: list[TimerTask]

    def update(self):
        if not self._tasks:
            return
        callFuncs = self._callFuncs
        clearTasks = self._clearTasks
        for task in self._tasks:
            task.remainingTicks -= 1
            if task.remainingTicks <= 0:
                # 如果任务的延迟时间到达
                callFuncs.append(task)
                if task.repeat:
                    # 如果是重复任务，重置剩余Tick
                    task.remainingTicks = task.delayTick
                    continue
                clearTasks.append(task)
        for clObj in clearTasks:
            self._tasks.pop(clObj)
        for callObj in callFuncs:
            TRY_EXEC_FUNC(callObj.bindFunc)
        callFuncs.clear()
        clearTasks.clear()

    def addTask(self, task: TimerTask):
        self._tasks[task] = None

    def addFuncTask(self, func: 'function', delayTick: int = 0, repeat: bool = False) -> TimerTask:
        task = TimerTask(func, delayTick, repeat)
        self.addTask(task)
        return task

    def removeTask(self, task: TimerTask):
        if task in self._tasks:
            del self._tasks[task]
            return True
        return False