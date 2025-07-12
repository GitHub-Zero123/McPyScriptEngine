package org.zero123.PyScriptEngine.Utils;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.server.ServerLifecycleHooks;

import java.util.HashMap;
import java.util.Optional;

public class WorldUtil
{
    public static final HashMap<String, Integer> DIMENSION_ID_MAP = new HashMap<>();
    public static final HashMap<Integer, ResourceKey<Level>> DIMENSION_ID_MAP_R = new HashMap<>();
    public static final HashMap<Integer, String> DIMENSION_NAMED_MAP = new HashMap<>();

    // 根据维度获取ID
    public static int getDimensionId(Level level)
    {
/*        var dim = level.dimension();
        if (dim.equals(Level.OVERWORLD)) return 0;
        if (dim.equals(Level.NETHER)) return 1;
        if (dim.equals(Level.END)) return 2;
        return System.identityHashCode(dim); */
        final var dmName = getDimensionKey(level);
        final var idValue = DIMENSION_ID_MAP.get(dmName);
        if(idValue == null)
        {
            return -1;
        }
        return idValue;
    }

    public static String getDimensionKey(Level level)
    {
        return level.dimension().location().toString();
    }

    // 基于ID搜索维度返回对应的level对象
    public static Optional<ServerLevel> findServerLevelById(int id)
    {
        final var dimName = DIMENSION_NAMED_MAP.get(id);
        if (dimName == null)
        {
            return Optional.empty();
        }
        ResourceLocation resLoc = ResourceLocation.tryParse(dimName);
        if (resLoc == null)
        {
            return Optional.empty();
        }
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        ResourceKey<Level> key = ResourceKey.create(Registries.DIMENSION, resLoc);
        if(server == null)
        {
            return Optional.empty();
        }
        // 尝试搜索目标level(可能未加载)
        final var level = server.getLevel(key);
        if (level != null)
        {
            return Optional.of(level);
        }
        return Optional.empty();
    }

    // 服务端初始化扫描维度信息 处理自定义维度映射
    public static void _serverInit(ServerStartedEvent event)
    {
        // 生成维度映射表(intId)
        DIMENSION_ID_MAP.clear();
        DIMENSION_ID_MAP_R.clear();
        DIMENSION_NAMED_MAP.clear();
        MinecraftServer server = event.getServer();

        int index = -10;
        for (ResourceKey<Level> levelKey : server.levelKeys())
        {
            String name = levelKey.location().toString(); // e.g. "minecraft:the_nether"
            DIMENSION_ID_MAP.put(name, index);
            DIMENSION_ID_MAP_R.put(index, levelKey);
            DIMENSION_NAMED_MAP.put(index, name);
            index--;
        }

        // 额外覆盖主世界、地狱、末地的ID为0, 1, 2
        String overworld = "minecraft:overworld";
        String nether = "minecraft:the_nether";
        String end = "minecraft:the_end";

        if (DIMENSION_ID_MAP.containsKey(overworld))
        {
            int oldId = DIMENSION_ID_MAP.get(overworld);
            ResourceKey<Level> oldKey = DIMENSION_ID_MAP_R.get(oldId);
            DIMENSION_ID_MAP.put(overworld, 0);
            DIMENSION_ID_MAP_R.put(0, oldKey);
            DIMENSION_NAMED_MAP.put(0, overworld);

            // 清理旧映射
            DIMENSION_ID_MAP_R.remove(oldId);
            DIMENSION_NAMED_MAP.remove(oldId);
        }

        if (DIMENSION_ID_MAP.containsKey(nether))
        {
            int oldId = DIMENSION_ID_MAP.get(nether);
            ResourceKey<Level> oldKey = DIMENSION_ID_MAP_R.get(oldId);
            DIMENSION_ID_MAP.put(nether, 1);
            DIMENSION_ID_MAP_R.put(1, oldKey);
            DIMENSION_NAMED_MAP.put(1, nether);

            DIMENSION_ID_MAP_R.remove(oldId);
            DIMENSION_NAMED_MAP.remove(oldId);
        }

        if (DIMENSION_ID_MAP.containsKey(end))
        {
            int oldId = DIMENSION_ID_MAP.get(end);
            ResourceKey<Level> oldKey = DIMENSION_ID_MAP_R.get(oldId);
            DIMENSION_ID_MAP.put(end, 2);
            DIMENSION_ID_MAP_R.put(2, oldKey);
            DIMENSION_NAMED_MAP.put(2, end);

            DIMENSION_ID_MAP_R.remove(oldId);
            DIMENSION_NAMED_MAP.remove(oldId);
        }
    }
}
