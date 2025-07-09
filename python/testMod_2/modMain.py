from mod.qumod3.api import EventBus
from mod.qumod3.event.world import OnScriptTickServer, OnScriptTickClient
from mod.qumod3.event.item import ServerItemTryUseEvent
from mod.qumod3.event.entity import AddEntityServerEvent
from mod.qumod3.entity import ServerEntity, ClientEntity
import mod.server.extraServerApi as serverApi

@EventBus
def onItemTryUseServer(event: ServerItemTryUseEvent):
    itemName = event.getItemName()
    if itemName == "minecraft:diamond_sword":
        player = event.getEntity()
        for entity in ServerEntity.getWorldEntities():
            if entity == player:
                continue
            entity.setCommand("/summon lightning_bolt")
            entity.kill()
        player.sendMessage("All entities have been killed except you!")
    elif itemName == "minecraft:diamond":
        player = event.getEntity()
        x, y, z = player.position.getPos()
        # 混合使用modsdk兼容层API
        serverApi.GetEngineCompFactory().CreateProjectile(serverApi.GetLevelId()).CreateProjectileEntity(
            player.entityId,
            "minecraft:creeper",
            {
                "position": (x, y+1.5, z),
                "direction": player.rotation.getRotDir(),
                "isDamageOwner": False,
                "power": 2.0,
            }
        )
        player.sendMessage("Creeper projectile created!")

@EventBus
def onAddEntityServer(event: AddEntityServerEvent):
    if event.getEngineTypeStr() != "minecraft:player":
        return
    # 仅针对玩家发送消息
    player = event.getEntity()
    player.sendMessage("§e[提示] testMod_2 已完成加载！")
    player.sendMessage("§b1.§f 右键使用 §c钻石剑 §f→ §6秒杀全部生物")
    player.sendMessage("§b2.§f 右键使用 §a钻石 §f→ §d发射一只苦力怕")
    player.sendMessage("§b3.§f §e哈斯克僵尸 §f现在会远程扔出存活一定时间的§e僵尸")

@EventBus
def onScriptTickServer(event: OnScriptTickServer):
    pass

@EventBus
def onScriptTickClient(event: OnScriptTickClient):
    pass
