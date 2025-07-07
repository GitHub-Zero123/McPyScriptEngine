package org.zero123.PyScriptEngine.ModSdk;

import com.google.gson.JsonObject;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;

public class ItemManager
{
    public static JsonObject itemToJson(Item itemObj)
    {
        var jo = new JsonObject();
        ResourceLocation itemId = BuiltInRegistries.ITEM.getKey(itemObj);
        jo.addProperty("newItemName", itemId.toString());
        // AUX扁平化一律视为0
        jo.addProperty("newAuxValue", 0);
        return jo;
    }
}
