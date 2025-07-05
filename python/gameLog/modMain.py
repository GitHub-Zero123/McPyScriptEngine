import sys
import PyMCBridge.ModLoader as ModLoader # type: ignore
import mod.api.entityModule as entityModule # type: ignore

_baseStdOutWrite = sys.stdout.write

# 重写 sys.stdout.write 方法 实现游戏内日志显示
def _gameStdOutWrite(text: object):
    if text != "\n":
        msg = "[Python] "+str(text)
        if ModLoader.isServerThread():
            entityModule._serverSendMessageAll(msg)
        elif ModLoader.isClientThread():
            entityModule._clientSendMessage(msg)
    return _baseStdOutWrite(text)

sys.stdout.write = _gameStdOutWrite

_baseStdErrWrite = sys.stderr.write

# 重写 sys.stderr.write 方法 实现游戏内错误日志显示
def _gameStdErrWrite(text: object):
    if text != "\n":
        msg = "§c[Python][Error] "+str(text)
        if ModLoader.isServerThread():
            entityModule._serverSendMessageAll(msg)
        elif ModLoader.isClientThread():
            entityModule._clientSendMessage(msg)
    return _baseStdErrWrite(text)

sys.stderr.write = _gameStdErrWrite