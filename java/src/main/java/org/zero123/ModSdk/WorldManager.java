package org.zero123.ModSdk;

import net.minecraft.world.level.Level;

public class WorldManager
{
    public static int getDimensionId(Level level)
    {
        var dim = level.dimension();
        if (dim.equals(Level.OVERWORLD)) return 0;
        if (dim.equals(Level.NETHER)) return 1;
        if (dim.equals(Level.END)) return 2;
        return -1; // 未知维度
    }
}
