from mod.qumod3.event.block import ServerPlayerTryDestroyBlockEvent
from mod.qumod3.api import SubscribeEvent

@SubscribeEvent
def onServerPlayerTryDestroyBlock(event: ServerPlayerTryDestroyBlockEvent):
    if event.getBlockName() == "minecraft:diamond_block":
        player = event.getEntity()
        player.sendMessage("You cannot destroy diamond blocks!")
        player.setCommand("/summon lightning_bolt")
        event.setCanceled()