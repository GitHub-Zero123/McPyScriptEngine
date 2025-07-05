# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
ServerSystemCls = serverApi.GetServerSystemCls()

levelId = serverApi.GetLevelId()

class TestSystem(ServerSystemCls):
    def __init__(self, namespace: str, systemName: str):
        super().__init__(namespace, systemName)
        self._tickValue = 0
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "OnScriptTickServer", None, self.onServerTick)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerItemTryUseEvent", None, self.ServerItemTryUseEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "AddEntityServerEvent", None, self.AddEntityServerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "EntityRemoveEvent", None, self.EntityRemoveEvent)
        print("TestSystem 服务端实例化")

    def AddEntityServerEvent(self, args: dict) -> None:
        pass

    def EntityRemoveEvent(self, args: dict) -> None:
        pass

    def ServerItemTryUseEvent(self, args: dict) -> None:
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

        for entityId in serverApi.GetEngineActor():
            comp = serverApi.GetEngineCompFactory().CreatePos(entityId)
            nowPos = comp.GetPos()
            comp.SetPos((nowPos[0], nowPos[1] + 5, nowPos[2]))
        
        # from time import time
        # state = False
        # IsEntityAlive = serverApi.GetEngineCompFactory().CreateGameComp(levelId).IsEntityAlive
        # s = time()
        # for _ in range(1000000):
        #     state = IsEntityAlive(playerId)
        # print(f"IsEntityAlive: {state}, 耗时: {time() - s:.3f}秒")
