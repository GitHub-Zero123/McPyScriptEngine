from mod.qumod3.api import SubscribeEvent, ServerInit, ClientInit
from mod.qumod3.event.world import OnScriptTickServer, OnScriptTickClient
from mod.qumod3.event.item import ServerItemTryUseEvent, ClientItemTryUseEvent
from mod.qumod3.event.entity import AddEntityServerEvent
from mod.qumod3.entity import ServerEntity, ClientEntity
from mod.qumod3.rpc import RpcBridge
import mod.server.extraServerApi as serverApi

rpc = RpcBridge("testMod_2")    # 命名空间为 testMod_2

@rpc.clientRpc
def clientTestFunc(args={}):
    print("客户端接收到了服务端的RPC调用！{}".format(args))
    rpc.callServer(serverTestFunc)

@rpc.serverRpc
def serverTestFunc():    
    print("服务端接收到了客户端的RPC调用！{}".format(RpcBridge.getCurrentRpcSenderId()))

@SubscribeEvent
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
    elif itemName == "minecraft:diamond_axe":
        player = event.getEntity()
        rpc.callClient(player, clientTestFunc, {"message": "Hello from server!"})

    if "apple" in event.getItemName():
        print("【服务端】禁止使用苹果！")
        event.setCanceled()

@SubscribeEvent
def onItemTryUseClient(event: ClientItemTryUseEvent):
    if "apple" in event.getItemName():
        # 取消物品使用需要双端同时进行
        print("【客户端】禁止使用苹果！")
        event.setCanceled()

@SubscribeEvent
def onAddEntityServer(event: AddEntityServerEvent):
    if event.getEngineTypeStr() != "minecraft:player":
        return
    # 仅针对玩家发送消息
    player = event.getEntity()
    player.sendMessage("§e[提示] testMod_2 已完成加载！")
    player.sendMessage("§b1.§f 右键使用 §c钻石剑 §f→ §6秒杀全部生物")
    player.sendMessage("§b2.§f 右键使用 §a钻石 §f→ §d发射一只苦力怕")
    player.sendMessage("§b3.§f 右键使用 §c钻石斧 §f→ §aRPC调用客户端函数")
    player.sendMessage("§b4.§f 右键使用 §a苹果 §f→ §c禁止使用苹果")

@SubscribeEvent
def onScriptTickServer(event: OnScriptTickServer):
    pass

@SubscribeEvent
def onScriptTickClient(event: OnScriptTickClient):
    pass

@ServerInit
def serverInit():
    pass

@ClientInit
def clientInit():
    pass