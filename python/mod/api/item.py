from .jni import findJavaCls, CAST_TYPE
from json import loads
lambda: "By Zero123"

_ITEM_MODULE = "org/zero123/PyScriptEngine/ModSdk/ItemModule"

def _serverGetEntityHandItemInfo(entityId: str) -> dict | None:
    """ 获取实体手持物品信息, 如果失败/不存在返回None """
    info = findJavaCls(_ITEM_MODULE, "_serverGetEntityHandItemInfo", [CAST_TYPE.STRING], CAST_TYPE.STRING).call(
        str(entityId)
    )
    if not info:
        return None
    return loads(info)