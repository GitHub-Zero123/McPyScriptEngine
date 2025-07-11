from mod.qumod3.event.entity import DamageEvent, ActuallyHurtServerEvent, ActorHurtServerEvent
from mod.qumod3.api import SubscribeEvent

@SubscribeEvent
def onDamageEvent(event: DamageEvent):
    if event.getDamage() < 5:
        event.setCanceled()

@SubscribeEvent
def onActuallyHurtServer(event: ActuallyHurtServerEvent):
    # print(f"受伤2: {event.args}")
    pass

@SubscribeEvent
def onActorHurtServer(event: ActorHurtServerEvent):
    # print(f"受伤3: {event.args}")
    pass
