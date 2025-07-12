package org.zero123.PyScriptEngine.Utils;

import net.minecraft.world.level.Level;

public class WorldUtil
{
    public static int getDimensionId(Level level)
    {
        var dim = level.dimension();
        if (dim.equals(Level.OVERWORLD)) return 0;
        if (dim.equals(Level.NETHER)) return 1;
        if (dim.equals(Level.END)) return 2;
        return System.identityHashCode(dim); // 自定义维度使用哈希码描述
    }

    public static String getDimensionKey(Level level)
    {
        return level.dimension().location().toString();
    }
}
