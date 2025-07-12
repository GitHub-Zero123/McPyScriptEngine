package org.zero123.PyScriptEngine.Events;

import com.google.gson.JsonObject;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.level.BlockEvent;
import org.zero123.PyMcBridge.EventManager;
import org.zero123.PyScriptEngine.Utils.BlockUtil;
import org.zero123.PyScriptEngine.Utils.WorldUtil;

public class Block
{
    // 玩家破坏方块事件
    @SubscribeEvent
    public void onBreakEvent(BlockEvent.BreakEvent event)
    {
        final var args = new JsonObject();
        args.addProperty("playerId", event.getPlayer().getUUID().toString());
        args.addProperty("fullName", BlockUtil.getBlockFullName(event.getState()));
        final var blockPos = event.getPos();
        args.addProperty("x", blockPos.getX());
        args.addProperty("y", blockPos.getY());
        args.addProperty("z", blockPos.getZ());
        if (event.getLevel() instanceof Level level)
        {
            args.addProperty("dimensionId", WorldUtil.getDimensionId(level));
        } else
        {
            args.addProperty("dimensionId", -1);
        }
        args.addProperty("cancel", false);
        final var ret = EventManager.Server.callEvent(110, args, new String[]{"cancel"});
        if(ret.has("cancel") && ret.get("cancel").getAsBoolean())
        {
            event.setCanceled(true);
        }
    }
}
