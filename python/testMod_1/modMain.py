# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

@Mod.Binding("testMod1", "1.0.0")
class TestMod1(object):
    def __init__(self):
        print("MOD对象实例化")

    @Mod.InitServer()
    def initServer(self):
        from PyMCBridge.ModLoader import getThreadTypeId # type: ignore
        print("服务端初始化")
        print("线程ID: "+str(getThreadTypeId()))
        serverApi.RegisterSystem("TestMod1", "TestServerSystem", "testMod_1.Server.TestSystem")

    @Mod.InitClient()
    def initClient(self):
        from PyMCBridge.ModLoader import getThreadTypeId # type: ignore
        print("客户端初始化")
        print("线程ID: "+str(getThreadTypeId()))
        clientApi.RegisterSystem("TestMod1", "TestClientSystem", "testMod_1.Client.TestSystem")

    @Mod.DestroyServer()
    def serverDestroy(self):
        print("服务端销毁")

    @Mod.DestroyClient()
    def clientDestroy(self):
        print("客户端销毁")