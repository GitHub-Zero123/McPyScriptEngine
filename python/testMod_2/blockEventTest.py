from mod.qumod3.event.block import ServerPlayerTryDestroyBlockEvent
from mod.qumod3.api import SubscribeEvent
import mod.server.extraServerApi as serverApi

@SubscribeEvent
def onServerPlayerTryDestroyBlock(event: ServerPlayerTryDestroyBlockEvent):
    if event.getBlockName() == "minecraft:diamond_block":
        player = event.getEntity()
        player.sendMessage("You cannot destroy diamond blocks!")
        player.setCommand("/summon lightning_bolt {} {} {}".format(*event.getPos()))
        event.setCanceled()
        serverApi.GetEngineCompFactory().CreateBlockState(None).SetBlockNew(
            event.getPos(), {"name": "minecraft:iron_block"}, 0, event.getDimensionId()
        )
        # x, y, z = event.getPos()
        # print(serverApi.GetEngineCompFactory().CreateBlockInfo(None).GetBlockNew(
        #     (x, y+1, z), event.getDimensionId()
        # ))