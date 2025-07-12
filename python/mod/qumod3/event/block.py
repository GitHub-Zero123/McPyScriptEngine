from .entity import BaseServerEntityEvent
from .base import SERVER_EVENT
from ..entity import ServerEntity

class ServerPlayerTryDestroyBlockEvent(BaseServerEntityEvent):
    """
    玩家尝试破坏方块事件
    """
    _NATIVE_ID = SERVER_EVENT.PLAYER_BLOCK_BREAK

    def __init__(self, args: dict):
        super().__init__(args.get("playerId", ""))
        self.args = args

    def getPlayer(self) -> ServerEntity:
        """
        获取尝试破坏方块的玩家实体
        :return: 玩家实体对象
        """
        return self.getEntity()
    
    def getPos(self) -> tuple[int, int, int]:
        """
        获取尝试破坏方块的坐标
        :return: (x, y, z)
        """
        args = self.args
        return (args["x"], args["y"], args["z"])

    def setCanceled(self, cancel: bool = True):
        """
        设置事件为取消状态，阻止方块被破坏
        """
        self.args["cancel"] = cancel
    
    def getBlockName(self) -> str:
        """
        获取方块的完整名称
        """
        return self.args.get("fullName", "")
    
    def getDimensionId(self) -> int:
        """
        获取事件发生的维度ID
        :return: 维度ID
        """
        return self.args.get("dimensionId", 0)