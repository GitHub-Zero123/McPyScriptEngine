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
        data.addProperty("cancel", false); // 暂不支持cancel
        if (event.getLevel().isClientSide())
        {
            // 客户端触发
            EventManager.callClientJsonEvent(2, data.toString());
        } else {
            // 服务端触发
            EventManager.callServerJsonEvent(2, data.toString());
        }
    }
}
