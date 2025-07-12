from mod.qumod3.event.block import ServerPlayerTryDestroyBlockEvent
# from mod.qumod3.event.item import ServerItemTryUseEvent
from mod.qumod3.api import SubscribeEvent
import mod.server.extraServerApi as serverApi

@SubscribeEvent
def onServerPlayerTryDestroyBlock(event: ServerPlayerTryDestroyBlockEvent):
    if event.getBlockName() == "minecraft:diamond_block":
        player = event.getEntity()
        player.sendMessage("You cannot destroy diamond blocks!")
        player.setCommand("/summon lightning_bolt {} {} {}".format(*event.getPos()))
        event.setCanceled()
        serverApi.GetEngineCompFactory().CreateBlockInfo(None).SetBlockNew(
            event.getPos(), {"name": "minecraft:iron_block"}, 0, event.getDimensionId()
        )
        # x, y, z = event.getPos()
        # print(serverApi.GetEngineCompFactory().CreateBlockInfo(None).GetBlockNew(
        #     (x, y+1, z), event.getDimensionId()
        # ))

# @SubscribeEvent
# def onItemTryUseServer(event: ServerItemTryUseEvent):
#     itemName = event.getItemName()
#     if itemName != "minecraft:iron_sword":
#         return
#     setBlockNew = serverApi.GetEngineCompFactory().CreateBlockInfo(None).SetBlockNew
#     player = event.getEntity()
#     x, y, z = player.position.getPos()
#     dmId = player.getDimensionId()
#     player.sendMessage("You used an iron sword!")
#     from time import time
#     s = time()
#     for dx in range(-50, 50):
#         for dy in range(-50, 50):
#             for dz in range(-50, 50):
#                 if dx == 0 and dy == 0 and dz == 0:
#                     continue
#                 setBlockNew((x + dx, y + dy, z + dz), {"name": "minecraft:glass"}, 0, dmId)
#     print("Time taken to set blocks:", time() - s)