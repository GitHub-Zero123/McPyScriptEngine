package org.zero123.PyScriptEngine.ModSdk;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.server.ServerLifecycleHooks;

import java.lang.reflect.Constructor;
import java.util.HashMap;
import java.util.Optional;
import java.util.UUID;

public class EntityManager
{
    public static HashMap<UUID, Entity> _serverTempEntity = new HashMap<>();

    public static void addServerTempEntity(UUID uuid, Entity entity)
    {
        _serverTempEntity.put(uuid, entity);
    }

    public static void removeServerTempEntity(UUID uuid)
    {
        _serverTempEntity.remove(uuid);
    }

    // 服务端根据实体uuid搜索实体
    public static Optional<Entity> serverGetEntityByUUID(UUID uuid)
    {
        // 先检查临时表
        Entity tempEntity = _serverTempEntity.get(uuid);
        if (tempEntity != null && tempEntity.isAlive())
        {
            // 存在Temp实体直接返回
            return Optional.of(tempEntity);
        }
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();

        if (server != null)
        {
            for (ServerLevel level : server.getAllLevels())
            {
                var entity = level.getEntity(uuid);
                if(entity != null)
                {
                    return Optional.of(entity);
                }
            }
        }
        return Optional.empty();
    }

    // 服务端根据字符串uuid搜索实体
    public static Optional<Entity> serverGetEntityByUUID(String uuid)
    {
        try
        {
            return serverGetEntityByUUID(UUID.fromString(uuid));
        } catch (IllegalArgumentException e)
        {
            return Optional.empty();
        }
    }

    /**
     * 根据资源标识符获取实体类
     * @param resourceId 资源ID，格式 "namespace:id"
     * @return 实体类 Class，找不到返回null
     */
    public static Class<? extends Entity> getEntityClassByResource(String resourceId)
    {
        // 通过注册表查找EntityType
        EntityType<?> entityType = EntityType.byString(resourceId).orElse(null);
        if (entityType == null)
        {
            return null;
        }
        return entityType.getBaseClass();
    }

    public static Entity createEntityByClass(Class<? extends Entity> entityCls, EntityType<?> entityType, Level world)
    {
        try
        {
            // 查找构造函数：(EntityType<?>, Level)
            Constructor<? extends Entity> ctor = entityCls.getConstructor(EntityType.class, Level.class);
            // 反射创建实体对象
            return ctor.newInstance(entityType, world);
        } catch (Exception e)
        {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * 动态创建实体实例（需要世界和位置）
     */
    public static Entity createEntityByResource(Level world, String resourceId, Vec3 pos, Vec3 direction, float velocity)
    {
        EntityType<?> entityType = EntityType.byString(resourceId).orElse(null);
        if (entityType == null)
        {
            return null;
        }
        // 通过EntityType创建实体
        Entity entity = entityType.create(world, EntitySpawnReason.TRIGGERED);
        if (entity != null)
        {
            entity.setPos(pos);
            // 如果是抛射物，则设置发射方向
            if (entity instanceof Projectile projectile)
            {
                projectile.shoot(direction.x, direction.y, direction.z, velocity, 0.0f); // inaccuracy=0.0f 表示直线发射
            }
            else
            {
                // 如果不是Projectile，可以考虑直接设置运动向量
                entity.setDeltaMovement(direction.normalize().scale(velocity));
            }
        }
        return entity;
    }
}
