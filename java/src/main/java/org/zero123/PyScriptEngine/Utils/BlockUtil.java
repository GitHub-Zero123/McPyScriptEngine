package org.zero123.PyScriptEngine.Utils;
import net.minecraft.world.level.block.state.BlockState;

public class BlockUtil {
    public static String getBlockFullName(BlockState blockState)
    {
        final var key = blockState.getBlockHolder().getKey();
        if(key != null)
        {
            return key.location().toString();
        }
        return "";
    }
}
