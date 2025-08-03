from ..api import world as _worldModule
import PyMCBridge.ModLoader as _ModLoader # type: ignore
lambda: "By Zero123"

class PlaceOptions:
    def __init__(self, oldHandlingMode: int = 0, updateNeighbors: bool = True):
        """
        方块放置配置参数
        :param oldHandlingMode: 旧方块处理模式(0.替换, 1.破坏, 2.保留)
        :param updateNeighbors: 是否更新邻近方块
        """
        self.oldHandlingMode = oldHandlingMode
        self.updateNeighbors = updateNeighbors

class BlockState:
    """ 方块状态 """
    def __init__(self, blockName: str):
        self.blockName = blockName

    def placeServer(self, pos: tuple[int, int, int], dimensionId: int, options: PlaceOptions = PlaceOptions()) -> bool:
        """
        放置方块在指定位置(仅服务端)
        :param pos: 方块位置
        :param dimensionId: 维度ID
        """
        if not _ModLoader.isServerThread():
            raise RuntimeError("This method can only be called on the server thread.")
        return _worldModule._serverSetBlock(pos, {"name": self.blockName}, options.oldHandlingMode, dimensionId, options.updateNeighbors)

    def isVoid(self):
        return self.blockName == "minecraft:air" or not self.blockName

    def isAir(self):
        return self.isVoid()
    
    @staticmethod
    def createAirBlock():
        return BlockState("minecraft:air")

    @staticmethod
    def getBlockState(pos: tuple[int, int, int], dimensionId: int=0) -> 'BlockState':
        """
        获取指定位置的方块状态(若在客户端获取则dimension始终为当前维度)
        :param pos: 方块位置
        :param dimensionId: 维度ID
        :return: 方块状态对象
        """
        if _ModLoader.isServerThread():
            return BlockState(_worldModule._serverGetBlock(pos, dimensionId).get("name", ""))
        else:
            return BlockState(_worldModule._clientGetBlock(pos).get("name", ""))
    
    def __eq__(self, value):
        if isinstance(value, BlockState):
            return self.blockName == value.blockName
        elif isinstance(value, str):
            return self.blockName == value
        return False