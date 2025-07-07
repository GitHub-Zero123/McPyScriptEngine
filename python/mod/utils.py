import pickle
lambda: "通用工具模块 By Zero123"

class Version:
    def __init__(self, version: str):
        self.parts = [int(p) for p in version.strip().split('.')]

    def newerThan(self, other: 'Version'):
        maxLen = max(len(self.parts), len(other.parts))
        selfParts = self.parts + [0] * (maxLen - len(self.parts))
        otherParts = other.parts + [0] * (maxLen - len(other.parts))

        for i in range(maxLen):
            a = selfParts[i]
            b = otherParts[i]
            if a > b:
                return True
            elif a < b:
                return False
        return False  # 完全相等

def TRY_EXEC_FUNC(func: 'function'):
    try:
        return func()
    except Exception:
        import traceback
        traceback.print_exc()
    return None

def importModule(modulePath: str) -> object:
    import importlib
    return importlib.import_module(modulePath)

def importChild(childPath: str) -> object:
    moduleName, className = childPath.rsplit('.', 1)
    module = importModule(moduleName)
    return getattr(module, className)

# def entityRotToDir(rot: tuple=(0, 0)) -> tuple:
#     import math
#     pitchDeg, yawDeg = rot
#     pitch = math.radians(pitchDeg)
#     yaw = math.radians(yawDeg)

#     x = -math.sin(yaw) * math.cos(pitch)
#     y = -math.sin(pitch)
#     z = math.cos(yaw) * math.cos(pitch)

#     return (x, y, z)

def entityRotToDir(rot: tuple=(0, 0)) -> tuple:
    from PyMCBridge.Math import _entityRotToDir # type: ignore
    return _entityRotToDir(rot[0], rot[1])

def serializeToPacket(data: dict) -> str:
    """ 将数据字典序列化为字符串格式的网络包 """
    return pickle.dumps(data, protocol=0).decode("utf-8")

def decodeFromPacket(packet: str) -> dict:
    """ 将字符串格式的网络包解码为数据字典 """
    try:
        return pickle.loads(packet.encode("utf-8"))
    except Exception:
        import traceback
        traceback.print_exc()
        return {}

def decodeJsonPacket(packet: dict) -> dict:
    """ 尝试解码JSON网络包 """
    if not "msg" in packet:
        raise RuntimeError("Invalid packet format: 'msg' key not found")
    packet["msg"] = decodeFromPacket(packet["msg"])  # 解码msg字段
    return packet

def packSystemPacket(event: tuple, sendData: dict, typeId: object=0) -> str:
    # 注: 内置的数据包typeId默认为0 若需自定义数据包处理handler, 请区分typeId(允许使用非int值)
    """
    打包系统事件数据包
    :param event: 系统事件名称
    :param sendData: 数据参数
    :return: 打包后的字段
    """
    return serializeToPacket({"event": event, "data": sendData, "typeId": typeId})