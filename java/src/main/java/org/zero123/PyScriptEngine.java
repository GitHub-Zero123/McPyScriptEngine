package org.zero123;

import com.mojang.logging.LogUtils;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import org.slf4j.Logger;
import org.zero123.Events.EntityEvent;
import org.zero123.Events.ItemEvent;
import org.zero123.PyMcBridge.EventManager;
import org.zero123.PyMcBridge.ModLoader;
import org.zero123.PyMcBridge.Native;

@Mod(PyScriptEngine.MODID)
public class PyScriptEngine
{
    public static final String MODID = "py_script_engine";
    private static final Logger LOGGER = LogUtils.getLogger();
    private boolean serverInit = false;
    public static boolean clientInit = false;

    public PyScriptEngine(IEventBus modEventBus, ModContainer modContainer)
    {
        modEventBus.addListener(this::commonSetup);
        NeoForge.EVENT_BUS.register(this);
        NeoForge.EVENT_BUS.register(new ItemEvent());
        NeoForge.EVENT_BUS.register(new EntityEvent());
    }

    // 公用初始化方法，会在游戏加载时被调用
    private void commonSetup(final FMLCommonSetupEvent event)
    {
        // 配置PyVM
        ModLoader.initializeVMConfigOnce(() -> {
            Native.initPythonEnvironment();
            ModLoader.setPyForceUseUTF8(1);
            ModLoader.setPyLineFlushMode(true);
            for (String path : PyInitConfig.getEnvPaths())
            {
                ModLoader.addEnvPath(path);
            }
            ModLoader.setTargetMods(PyInitConfig.getTargetMods());
        });
    }

    // 服务端启动事件
    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event)
    {
        LOGGER.info("[ENGINE] 服务端初始化");
        if(!serverInit)
        {
            serverInit = true;
            ModLoader.loadServerThread();
        }
    }

    @SubscribeEvent
    public void onServerTick(ServerTickEvent.Post event)
    {
        // 广播tick事件 id:1
        if (serverInit)
        {
            EventManager.callServerEvent(1);
        }
    }

    @SubscribeEvent
    public void onClientTick(ClientTickEvent.Post event)
    {
        // 客户端Tick
        if (clientInit)
        {
            EventManager.callClientEvent(1);
        }
    }

    @SubscribeEvent
    public void onServerStopping(ServerStoppingEvent event)
    {
        if(serverInit)
        {
            serverInit = false;
            ModLoader.destroyServerThread();
            LOGGER.info("[ENGINE] 服务端销毁");
        }
    }

    @SubscribeEvent
    public void onClientJoin(ClientPlayerNetworkEvent.LoggingIn event)
    {
        if(!clientInit)
        {
            LOGGER.info("[ENGINE] 客户端初始化");
            clientInit = true;
            ModLoader.loadClientThread();
        }
    }

    @SubscribeEvent
    public void onClientLeave(ClientPlayerNetworkEvent.LoggingOut event)
    {
        if(clientInit)
        {
            clientInit = false;
            ModLoader.destroyClientThread();
            LOGGER.info("[ENGINE] 客户端销毁");
        }
    }
}
