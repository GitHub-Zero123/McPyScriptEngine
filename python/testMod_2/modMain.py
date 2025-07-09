from mod.qumod3.api import EventBus
from mod.qumod3.event.world import OnScriptTickServer, OnScriptTickClient
from mod.qumod3.event.entity import ServerItemTryUseEvent

@EventBus
def onItemTryUseServer(event: ServerItemTryUseEvent):
    print(f"Server item try use event: {event.playerId} used item {event.itemDict}")
    if event.getItemName() == "minecraft:diamond_sword":
        event.getEntity().kill()

@EventBus
def onScriptTickServer(event: OnScriptTickServer):
    pass

@EventBus
def onScriptTickClient(event: OnScriptTickClient):
    pass