# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
ClientSystemCls = clientApi.GetClientSystemCls()

class TestSystem(ClientSystemCls):
    def __init__(self, namespace: str, systemName: str):
        super().__init__(namespace, systemName)
        self._tickValue = 0
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "OnScriptTickClient", None, self.onClientTick)
        print("TestSystem 客户端实例化")
    
    def onClientTick(self):
        pass