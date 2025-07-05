from .jni import findJavaCls, CAST_TYPE

_CMD_MODULE = "org/zero123/ModSdk/Command"

def _setCommand(cmdStr: str, entityId: str="", showOutput: bool=False) -> bool:
    """ 设置执行命令 """
    return bool(findJavaCls(_CMD_MODULE, "_setCommand", [CAST_TYPE.STRING, CAST_TYPE.STRING, CAST_TYPE.INT], CAST_TYPE.INT).call(
        cmdStr, entityId, int(showOutput)
    ))
