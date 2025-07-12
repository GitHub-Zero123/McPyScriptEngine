package org.zero123.PyScriptEngine.Events;

import com.google.gson.JsonObject;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.item.ItemEntity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.EntityLeaveLevelEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import org.zero123.PyScriptEngine.ModSdk.EntityManager;
import org.zero123.PyMcBridge.EventManager;
import org.zero123.PyScriptEngine.ModSdk.WorldManager;
import org.zero123.PyScriptEngine.Utils.JsonUtil;

public class EntityEvent
{
    // 实体构造事件
    @SubscribeEvent
    public void onEntityJoinLevel(EntityJoinLevelEvent event)
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
        final var uuid = entity.getUUID();
        if (event.getLevel().isClientSide())
        {
            EntityManager.addClientTempEntity(uuid, entity);
            EventManager.callClientJsonEvent(3, args.toString());
            EntityManager.removeClientTempEntity(uuid);
        }
        else
        {
            EntityManager.addServerTempEntity(uuid, entity);
            EventManager.callServerJsonEvent(3, args.toString());
            EntityManager.removeServerTempEntity(uuid);
        }
    }

    // 实体卸载/移除事件
    @SubscribeEvent
    public void onEntityLeaveLevel(EntityLeaveLevelEvent event)
    {
        final var entity = event.getEntity();
        JsonObject args = new JsonObject();
        args.addProperty("id", entity.getUUID().toString());
        if (event.getLevel().isClientSide())
        {
            EventManager.callClientJsonEvent(4, args.toString());
        }
        else
        {
            EventManager.callServerJsonEvent(4, args.toString());
        }
    }

    // =============== 服务端受伤事件 ===============

    @SubscribeEvent // 对应 DamageEvent
    public void onLivingIncomingDamage(LivingIncomingDamageEvent event)
    {
        final var args = new JsonObject();
        final var source = event.getSource();
        // 计算伤害源的实体
        args.addProperty("srcId", EntityManager.getEntityStrId(source.getEntity()));
        // 计算间接实体(通常是投掷物)
        args.addProperty("projectileId", EntityManager.getEntityStrId(source.getDirectEntity()));
        // 受伤的实体
        args.addProperty("entityId", EntityManager.getEntityStrId(event.getEntity()));
        // damage值(允许修改)
        args.addProperty("damage", event.getContainer().getOriginalDamage());
        // knock(暂不支持修改击退 但若knock设为false且damage为0则视为取消本次伤害)
        args.addProperty("knock", true);
        // ignite(是否是燃烧伤害)
        args.addProperty("ignite", event.getEntity().isOnFire());
        final var retJo = EventManager.Server.callEvent(100, args, new String[]{"damage", "knock"});
        if(retJo.has("damage"))
        {
            // 事件内修改伤害值
            event.getContainer().setNewDamage(JsonUtil.getFloatOrDefault(retJo, "damage", 0.0f));
        }
        if(retJo.has("knock") && event.getContainer().getNewDamage() == 0.0f)
        {
            if(!retJo.get("knock").getAsBoolean())
            {
                event.setCanceled(true);
            }
        }
    }

    @SubscribeEvent // 对应 ActuallyHurtServerEvent
    public void onLivingDamageBefore(LivingDamageEvent.Pre event)
    {
        final var args = new JsonObject();
        final var source = event.getSource();
        // 计算伤害源的实体
        args.addProperty("srcId", EntityManager.getEntityStrId(source.getEntity()));
        // 计算间接实体(通常是投掷物)
        args.addProperty("projectileId", EntityManager.getEntityStrId(source.getDirectEntity()));
        // 受伤的实体
        args.addProperty("entityId", EntityManager.getEntityStrId(event.getEntity()));
        // damage值(允许修改)
        args.addProperty("damage", event.getNewDamage());
        // knock(暂不支持)
        // ...
        final var retJo = EventManager.Server.callEvent(101, args, new String[]{"damage"});
        if(retJo.has("damage"))
        {
            // 事件内修改伤害值
            event.setNewDamage(JsonUtil.getFloatOrDefault(retJo, "damage", 0.0f));
        }
    }

    @SubscribeEvent // 对应 ActorHurtServerEvent
    public void onLivingDamageAfter(LivingDamageEvent.Post event)
    {
        final var args = new JsonObject();
        // 受伤的实体
        args.addProperty("entityId", EntityManager.getEntityStrId(event.getEntity()));
        // damage伤害值(不允许修改)
        args.addProperty("damage", event.getNewDamage());
        EventManager.Server.callEvent(102, args);
    }
}
