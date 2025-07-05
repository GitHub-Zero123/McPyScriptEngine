# -*- coding: utf-8 -*-
from .QuModLibs.Server import *
from .QuModLibs.Modules.EntityComps.Server import QBaseEntityComp

# 有限存活时间组件
class TestLiveTimeComp(QBaseEntityComp):
    """ 测试实体有限存活时间组件 """
    def __init__(self):
        super().__init__()
        self._liveTick = 60

    def update(self):
        super().update()
        self._liveTick -= 1
        if self._liveTick <= 0:
            comp = serverApi.GetEngineCompFactory().CreateGame(levelId)
            comp.KillEntity(self.entityId)
            return

@QBaseEntityComp.regEntity("minecraft:husk")    # 为特定实体注册组件
class TestFireComp(QBaseEntityComp):
    """ 测试远程攻击组件 """
    def __init__(self):
        super().__init__()
        self._tickValue = 0
        self.targetEntity = "minecraft:zombie"
    
    def update(self):
        super().update()
        self._tickValue += 1
        targetId = serverApi.GetEngineCompFactory().CreateAction(self.entityId).GetAttackTarget()
        if not targetId:
            return
        myPos = serverApi.GetEngineCompFactory().CreatePos(self.entityId).GetPos()
        targetPos = serverApi.GetEngineCompFactory().CreatePos(targetId).GetPos()
        if not myPos or not targetPos:
            return
        x1, y1, z1 = myPos
        x2, y2, z2 = targetPos
        distance = ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) ** 0.5
        if distance < 3:
            return
        if self._tickValue % 10 != 0:
            return
        comp = serverApi.GetEngineCompFactory().CreateRot(self.entityId)
        rot = comp.GetRot()
        dirRot = serverApi.GetDirFromRot((rot[0]+5, rot[1]))
        entityId = serverApi.GetEngineCompFactory().CreateProjectile(levelId).CreateProjectileEntity(
            self.entityId,
            self.targetEntity,
            {
                "position": (x1, y1+1.0, z1),
                "direction": dirRot,
                "isDamageOwner": False,
                "power": distance * 0.18,
            }
        )
        if entityId:
            TestLiveTimeComp().bind(entityId)  # 绑定有限存活时间组件

class InitMsgComp(QBaseEntityComp):
    """ 初始化消息组件 """
    def __init__(self):
        super().__init__()
        self.addTimer(QBaseEntityComp.Timer(self.initMsg, time=0.2))
    
    def initMsg(self):
        msgComp = serverApi.GetEngineCompFactory().CreateMsg(self.entityId)
        msgComp.NotifyOneMessage(self.entityId, "§e[提示] testMod_0 已完成加载！")
        msgComp.NotifyOneMessage(self.entityId, "§b1.§f 右键使用 §c钻石剑 §f→ §6秒杀全部生物")
        msgComp.NotifyOneMessage(self.entityId, "§b2.§f 右键使用 §a钻石 §f→ §d发射一只苦力怕")
        msgComp.NotifyOneMessage(self.entityId, "§b3.§f §e哈斯克僵尸 §f现在会远程扔出存活一定时间的§7僵尸")
        self.unbind()  # 初始化消息发送后解绑组件

@Listen("AddEntityServerEvent")
def AddEntityServerEvent(args: dict) -> None:
    if args["engineTypeStr"] == "minecraft:player":
        # 玩家加入了游戏
        entityId = args["id"]
        InitMsgComp().bind(entityId)  # 绑定初始化消息组件

@QBaseEntityComp.regEntity("minecraft:wither")  # 为特定实体注册组件
class TntFireComp(TestFireComp):
    """ 测试TNT远程攻击组件 """
    def __init__(self):
        super().__init__()
        self.targetEntity = "minecraft:tnt"

@Listen("ServerItemTryUseEvent")
def ServerItemTryUseEvent(args: dict) -> None:
    playerId = args["playerId"]
    itemDict = args["itemDict"]
    newItemName = itemDict["newItemName"]

    if newItemName == "minecraft:diamond":
        comp = serverApi.GetEngineCompFactory().CreateRot(playerId)
        rot = comp.GetRot()
        dirRot = serverApi.GetDirFromRot(rot)
        x, y, z = serverApi.GetEngineCompFactory().CreatePos(playerId).GetPos()
        y += 1.5
        serverApi.GetEngineCompFactory().CreateProjectile(levelId).CreateProjectileEntity(
            playerId,
            "minecraft:creeper",
            {
                "position": (x, y, z),
                "direction": dirRot,
                "isDamageOwner": False,
                "power": 2.0,
            }
        )
        return
    elif newItemName == "minecraft:diamond_sword":
        cmdComp = serverApi.GetEngineCompFactory().CreateCommand(levelId)
        gameComp = serverApi.GetEngineCompFactory().CreateGame(levelId)
        for entityId in serverApi.GetEngineActor():
            if entityId == playerId:
                continue
            pos = serverApi.GetEngineCompFactory().CreatePos(entityId).GetPos()
            if not pos:
                continue
            x, y, z = pos
            gameComp.KillEntity(entityId)
            cmdComp.SetCommand(f"/summon lightning_bolt {x} {y} {z}", playerId) 
        return

    # for entityId in serverApi.GetEngineActor():
    #     comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
    #     nowPos = comp.GetPos()
    #     comp.SetPos((nowPos[0], nowPos[1] + 5, nowPos[2]))