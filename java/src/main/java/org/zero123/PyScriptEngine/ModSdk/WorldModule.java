package org.zero123.PyScriptEngine.ModSdk;

import net.minecraft.client.Minecraft;
import net.minecraft.core.BlockPos;
import org.zero123.PyScriptEngine.Utils.BlockUtil;
import org.zero123.PyScriptEngine.Utils.WorldUtil;

public class WorldModule
{
    // 服务端设置方块
    public static int _serverSetBlock(String pos, String blockJo, int oldHandling, int dimensionId, int updateNeighbors)
    {
        var posArray = Utils.parseIntArray(pos);
        final var levelOpt = WorldUtil.findServerLevelById(dimensionId);
        if(levelOpt.isEmpty())
        {
            return 0;
        }
        final var level = levelOpt.get();   // Level对象
        final var blockState = BlockUtil.jsonToBlockState(blockJo);
        final var blockPos = new BlockPos(posArray[0], posArray[1], posArray[2]);
        switch (oldHandling)
        {
            case 2:
                if (!level.getBlockState(blockPos).isAir())
                {
                    return 0; // 保留旧方块
                }
                break;
            case 1:
                if (!level.getBlockState(blockPos).isAir())
                {
                    // 破坏方块并掉落物品
                    level.destroyBlock(blockPos, true);
                }
                break;
            case 0:
            default:
                // 直接替换不作判定
                break;
        }
        int flags = 2 + (updateNeighbors != 0 ? 1 : 0);
        boolean setState = level.setBlock(blockPos, blockState, flags);
        return (setState ? 1 : 0);
    }

    // 服务端获取方块信息
    public static String _serverGetBlock(String pos, int dimensionId)
    {
        var posArray = Utils.parseIntArray(pos);
        final var levelOpt = WorldUtil.findServerLevelById(dimensionId);
        if(levelOpt.isEmpty())
        {
            return "{\"name\":\"minecraft:air\", \"aux\": 0}";
        }
        final var level = levelOpt.get();   // Level对象
        final var blockPos = new BlockPos(posArray[0], posArray[1], posArray[2]);
        final var current = level.getBlockState(blockPos);  // 获取已有方块对象
        return BlockUtil.blockStateToJson(current).toString();
    }

    // 客户端获取方块信息
    public static String _clientGetBlock(String pos)
    {
        var posArray = Utils.parseIntArray(pos);
        var level = Minecraft.getInstance().level; // 当前客户端世界

        if (level == null)
        {
            return "{\"name\":\"minecraft:air\", \"aux\": 0}";
        }

        var blockPos = new BlockPos(posArray[0], posArray[1], posArray[2]);
        var current = level.getBlockState(blockPos);
        return BlockUtil.blockStateToJson(current).toString();
    }
}
