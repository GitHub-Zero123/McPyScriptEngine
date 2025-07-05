from .jni import findJavaCls, CAST_TYPE, floatSplit, numberTupleJoin
from json import dumps
lambda: "By Zero123"

_ENTITY_MODULE = "org/zero123/ModSdk/EntityModule"
_PROJECTILE_MODULE = "org/zero123/ModSdk/ProjectileModule"

def _serverGetEntityPos(entityId: str):
    """ 获取实体位置 """
    return floatSplit(findJavaCls(_ENTITY_MODULE, "_serverGetEntityPos", [CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        entityId
    ))

def _serverSetEntityPos(entityId: str, pos: tuple):
    """ 设置实体位置 """
    return findJavaCls(_ENTITY_MODULE, "_serverSetEntityPos", [CAST_TYPE.STRING, CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        entityId, numberTupleJoin((pos[0], pos[1], pos[2]))
    )

def _serverGetEntityRot(entityId: str):
    """ 获取实体旋转欧拉角 """
    return floatSplit(findJavaCls(_ENTITY_MODULE, "_serverGetEntityRot", [CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        entityId
    ))

def _serverShootProjectile(entityId: str, entityIdentifier: str, dataMap: dict) -> str:
    """ 创建并发射投掷物 """
    return findJavaCls(_PROJECTILE_MODULE, "_serverShootProjectile", [CAST_TYPE.STRING, CAST_TYPE.STRING, CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        entityId, entityIdentifier, dumps(dataMap)
    )

def _serverGetEntityTypeName(entityId: str) -> str:
    """ 获取实体类型名称(标识符) """
    return findJavaCls(_ENTITY_MODULE, "_serverGetEntityTypeName", [CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        entityId
    )

def _serverCheckIsPlayer(entityId: str) -> bool:
    """ 检查实体是否为玩家 """
    return bool(findJavaCls(_ENTITY_MODULE, "_serverCheckIsPlayer", [CAST_TYPE.STRING], CAST_TYPE.INT).call(
        entityId
    ))

def _serverCheckEntityAlive(entityId: str) -> bool:
    """ 检查实体是否存活 """
    return bool(findJavaCls(_ENTITY_MODULE, "_serverCheckEntityAlive", [CAST_TYPE.STRING], CAST_TYPE.INT).call(
        entityId
    ))

def _serverGetWorldEntityList() -> list:
    """ 获取世界实体id列表 """
    data = str(findJavaCls(_ENTITY_MODULE, "_serverGetWorldEntityList", [], CAST_TYPE.STRING).call())
    if not data:
        return []
    return list(data.split(" "))

def _serverKillEntity(entityId: str) -> bool:
    """ 杀死实体 """
    return bool(findJavaCls(_ENTITY_MODULE, "_serverKillEntity", [CAST_TYPE.STRING], CAST_TYPE.INT).call(
        entityId
    ))

def _serverDestroyEntity(entityId: str) -> bool:
    """ 销毁实体 """
    return bool(findJavaCls(_ENTITY_MODULE, "_serverDestroyEntity", [CAST_TYPE.STRING], CAST_TYPE.INT).call(
        entityId
    ))

def _serverGetAllPlayerId() -> list:
    """ 获取所有玩家ID """
    data = str(findJavaCls(_ENTITY_MODULE, "_serverGetAllPlayerId", [], CAST_TYPE.STRING).call())
    if not data:
        return []
    return list(data.split(" "))

def _serverGetEntityTargetId(entityId: str) -> str:
    """ 获取实体目标ID """
    return findJavaCls(_ENTITY_MODULE, "_serverGetEntityTargetId", [CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        entityId
    )

def _serverSendMessage(playerId: str, message: str):
    """ 向指定玩家发送消息 """
    return findJavaCls(_ENTITY_MODULE, "_serverSendMessage", [CAST_TYPE.STRING, CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        playerId, message
    )

def _serverSendMessageAll(message: str):
    """ 向所有玩家发送消息 """
    return findJavaCls(_ENTITY_MODULE, "_serverSendMessageAll", [CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        message
    )