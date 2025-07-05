import enum

class CAST_TYPE(enum):
    VOID = 0
    INT = 1
    STRING = 2

class PyCastJVMFunction:
    def __init__(self, clsPath: str, methodName: str, argsType: list[CAST_TYPE], returnType: CAST_TYPE=CAST_TYPE.VOID):
        pass

    def call(self, *args) -> object | None:
        """
            调用JVM函数并自动转换为Python类型
        """
        pass