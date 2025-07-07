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
        if (!event.getLevel().isClientSide())
        {
            // 服务端用户尝试使用物品
            var data = new JsonObject();
            data.addProperty("playerId", event.getEntity().getUUID().toString());
            data.add("itemDict", ItemManager.itemToJson(item));
            data.addProperty("cancel", false); // 暂不支持cancel
            EventManager.callServerJsonEvent(2, data.toString());
        }
    }
}
