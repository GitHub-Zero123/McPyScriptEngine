package org.zero123.PyScriptEngine.Events;

import com.google.gson.JsonObject;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import org.zero123.PyMcBridge.EventManager;
import org.zero123.PyScriptEngine.ModSdk.ItemManager;

public class ItemEvent
{
    @SubscribeEvent
    public void onRightClickItem(PlayerInteractEvent.RightClickItem event)
    {
        var item = event.getItemStack().getItem();
        var data = new JsonObject();
        data.addProperty("playerId", event.getEntity().getUUID().toString());
        data.add("itemDict", ItemManager.itemToJson(item));
        data.addProperty("cancel", false);
        JsonObject retJson;
        if (event.getLevel().isClientSide())
        {
            // 客户端触发
            retJson = EventManager.Client.callEvent(2, data, new String[]{"cancel"});
        } else {
            // 服务端触发
            retJson = EventManager.Server.callEvent(2, data, new String[]{"cancel"});
        }
        final var cancel = retJson.get("cancel");
        if (cancel != null && cancel.isJsonPrimitive() && cancel.getAsJsonPrimitive().isBoolean())
        {
            if(cancel.getAsBoolean())
            {
                event.setCanceled(true);
            }
        }
    }
}
