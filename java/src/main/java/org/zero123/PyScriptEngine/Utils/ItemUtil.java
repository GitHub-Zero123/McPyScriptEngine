package org.zero123.PyScriptEngine.Utils;

import com.google.gson.JsonObject;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.entity.Entity;

import javax.annotation.Nullable;
import java.util.Optional;

public class ItemUtil
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

    public static Optional<ItemStack> getEntityHandItem(Entity entity)
    {
        if(entity instanceof LivingEntity living)
        {
            return Optional.of(living.getMainHandItem());
        }
        return Optional.empty();
    }

    public static JsonObject itemStackToJo(@Nullable ItemStack itemStack)
    {
        if(itemStack.isEmpty())
        {
            return new JsonObject();
        }
        final var itemJo = new JsonObject();
        itemJo.addProperty("newItemName", getItemKeyName(itemStack.getItem()));
        itemJo.addProperty("newAuxValue", 0);
        return itemJo;
    }

    public static String getItemKeyName(Item item)
    {
        final var key = BuiltInRegistries.ITEM.getKey(item);
        return key.getNamespace() + ":" + key.getPath();
    }
}
