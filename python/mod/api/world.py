from .jni import findJavaCls, CAST_TYPE, numberTupleJoin
from json import dumps, loads
lambda: "By Zero123"

_WORLD_MODULE = "org/zero123/PyScriptEngine/ModSdk/World"

def _serverSetBlock(pos: tuple[int, int, int], blockJo: dict, oldHandling: bool = 0, dimensionId: int = 0, updateNeighbors: bool=True) -> bool:
    """ 服务端设置方块
    :param pos: 方块位置
    :param blockJo: 方块数据 {"name": "minecraft:stone"} (AUX在此废弃，不会被解析)
    :param oldHandling: 旧方块处理策略: 0(默认).直接替换 1.破坏并替换 2.保留
    :param dimensionId: 维度ID
    :param updateNeighbors: 是否更新邻居方块(默认更新)
    """
    return bool(findJavaCls(_WORLD_MODULE, "_serverSetBlock", [CAST_TYPE.STRING, CAST_TYPE.STRING, CAST_TYPE.INT, CAST_TYPE.INT, CAST_TYPE.INT], CAST_TYPE.INT).call(
        numberTupleJoin(int(v) for v in pos), dumps(blockJo) if blockJo else "", int(oldHandling), int(dimensionId), int(updateNeighbors)
    ))

def _serverGetBlock(pos: tuple[int, int, int], dimensionId: int = 0) -> dict:
    """ 服务端获取方块数据
    :param pos: 方块位置
    :param dimensionId: 维度ID
    :return: 方块数据字典 {"name": "minecraft:stone", "aux": 0}
    """
    return loads(findJavaCls(_WORLD_MODULE, "_serverGetBlock", [CAST_TYPE.STRING, CAST_TYPE.INT], CAST_TYPE.STRING).call(
        numberTupleJoin(int(v) for v in pos), int(dimensionId)
    ))