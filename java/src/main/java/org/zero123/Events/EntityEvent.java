package org.zero123.Events;

import com.google.gson.JsonObject;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.item.ItemEntity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.EntityLeaveLevelEvent;
import org.zero123.PyMcBridge.EventManager;
import org.zero123.ModSdk.WorldManager;

public class EntityEvent
{
    // 实体构造事件
    @SubscribeEvent
    public void onEntityJoinLevel(EntityJoinLevelEvent event)
    {
        if (!event.getLevel().isClientSide())
        {
            // 服务端事件
            final var entity = event.getEntity();
            JsonObject args = new JsonObject();
            // 基础参数处理
            args.addProperty("id", entity.getUUID().toString());
            args.addProperty("dimensionId", WorldManager.getDimensionId(entity.level()));
            args.addProperty("engineTypeStr", EntityType.getKey(entity.getType()).toString());
            // 位置信息处理
            final var pos = entity.position();
            args.addProperty("x", pos.x);
            args.addProperty("y", pos.y);
            args.addProperty("z", pos.z);
            args.addProperty("isBaby", false);
            // 宝宝实体处理
            if (entity instanceof AgeableMob ageable)
            {
                if (ageable.isBaby())
                {
                    args.addProperty("isBaby", true);
                }
            }
            // 物品实体（ItemEntity）
            if (entity instanceof ItemEntity)
            {
                args.addProperty("itemName", "minecraft:item");
//                args.addProperty("itemName", BuiltInRegistries.ITEM.getKey(itemEntity.getItem().getItem()).toString());
                args.addProperty("auxValue", 0);
            }
            EventManager.callServerJsonEvent(3, args.toString());
        }
    }

    // 实体卸载/移除事件
    @SubscribeEvent
    public void onEntityLeaveLevel(EntityLeaveLevelEvent event)
    {
        if (!event.getLevel().isClientSide())
        {
            // 服务端事件
            final var entity = event.getEntity();
            JsonObject args = new JsonObject();
            args.addProperty("id", entity.getUUID().toString());
            EventManager.callServerJsonEvent(4, args.toString());
        }
    }
}
