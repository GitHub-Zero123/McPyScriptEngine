package org.zero123.PyScriptEngine.ModSdk;

import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import org.zero123.PyScriptEngine.Utils.EntityUtil;
import org.zero123.PyScriptEngine.Utils.WorldUtil;

import java.util.ArrayList;

public class EntityModule
{
    public static class EntityRot
    {
        public float x;
        public float y;
        public EntityRot(float x, float y)
        {
            this.x = x;
            this.y = y;
        }
    }

    // 获取实体的rot旋转角
    public static EntityRot getEntityRot(Entity entity)
    {
        return new EntityRot(entity.getXRot(), entity.getYRot());
    }

    // 基于rot转换为向量
    public static Vec3 toDirectionVector(float yaw, float pitch)
    {
        double radYaw = Math.toRadians(yaw);
        double radPitch = Math.toRadians(pitch);
        double x = -Math.cos(radPitch) * Math.sin(radYaw);
        double y = -Math.sin(radPitch);
        double z = Math.cos(radPitch) * Math.cos(radYaw);
        return new Vec3(x, y, z);
    }

    public static Vec3 toDirectionVector(EntityRot rot)
    {
        return toDirectionVector(rot.x, rot.y);
    }

    // ====================== 绑定函数 ======================

    // 获取实体坐标
    public static String _serverGetEntityPos(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return "";
        }
        final var pos = entityOpt.get().position();
        Double[] posArray = new Double[] {
            pos.x, pos.y, pos.z
        };
        return Utils.arrayToString(posArray);
    }

    // 客户端获取实体坐标
    public static String _clientGetEntityPos(String entityId)
    {
        var entityOpt = EntityUtil.clientGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return "";
        }
        final var pos = entityOpt.get().position();
        Double[] posArray = new Double[] {
                pos.x, pos.y, pos.z
        };
        return Utils.arrayToString(posArray);
    }

    // 设置实体坐标
    public static void _serverSetEntityPos(String entityId, String posBytes)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            var posArray = Utils.parseDoubleArray(posBytes);
            final var entity = entityOpt.get();
            entity.teleportTo(posArray[0], posArray[1], posArray[2]);
            entity.setDeltaMovement(Vec3.ZERO);
/*            if (entity.get() instanceof ServerPlayer player)
            {
                // 玩家同步并刷新客户端
                player.teleportTo(posArray[0], posArray[1], posArray[2]);
            }*/
        }
    }

    // 获取实体旋转角
    public static String _serverGetEntityRot(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            final var entity = entityOpt.get();
            return Utils.arrayToString(new Float[] { entity.getXRot(), entity.getYRot() });
        }
        return "";
    }

    // 客户端获取实体旋转角
    public static String _clientGetEntityRot(String entityId)
    {
        var entityOpt = EntityUtil.clientGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            final var entity = entityOpt.get();
            return Utils.arrayToString(new Float[] { entity.getXRot(), entity.getYRot() });
        }
        return "";
    }

    // 获取实体的标识符
    public static String _serverGetEntityTypeName(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            return EntityType.getKey(entityOpt.get().getType()).toString();
        }
        return "";
    }

    // 客户端获取实体标识符
    public static String _clientGetEntityTypeName(String entityId)
    {
        var entityOpt = EntityUtil.clientGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            return EntityType.getKey(entityOpt.get().getType()).toString();
        }
        return "";
    }

    // 判断实体类型是不是玩家
    public static int _serverCheckIsPlayer(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            if(entityOpt.get() instanceof Player)
            {
                return 1;
            }
        }
        return 0;
    }

    // 客户端判断实体是不是玩家
    public static int _clientCheckIsPlayer(String entityId)
    {
        var entityOpt = EntityUtil.clientGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            if(entityOpt.get() instanceof Player)
            {
                return 1;
            }
        }
        return 0;
    }

    // 判断实体是否存在
    public static int _serverCheckEntityAlive(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        return entityOpt.isPresent() ? 1 : 0;
    }

    // 客户端判断实体是否存在
    public static int _clientCheckEntityAlive(String entityId)
    {
        var entityOpt = EntityUtil.clientGetEntityByUUID(entityId);
        return entityOpt.isPresent() ? 1 : 0;
    }

    // 【服务端】获取世界实体列表
    public static String _serverGetWorldEntityList()
    {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        ArrayList<String> entityIds = new ArrayList<>();
        if (server != null)
        {
            for (ServerLevel level : server.getAllLevels())
            {
                // 遍历当前维度所有实体
                for (Entity entity : level.getEntities().getAll())
                {
                    entityIds.add(entity.getUUID().toString());
                }
            }
        }
        return Utils.joinWithSpace(entityIds);
    }

    // 【客户端】获取加载中的所有实体列表
    public static String _clientGetWorldEntityList()
    {
        final var clientLevel = Minecraft.getInstance().level;
        ArrayList<String> entityIds = new ArrayList<>();
        if (clientLevel != null)
        {
            // 遍历当前维度所有实体
            for (Entity entity : clientLevel.entitiesForRendering())
            {
                entityIds.add(entity.getUUID().toString());
            }
        }
        return Utils.joinWithSpace(entityIds);
    }

    // 【客户端】获取本地玩家ID
    public static String _clientGetLocalPlayerId()
    {
        final var player = Minecraft.getInstance().player;
        if (player != null)
        {
            return player.getUUID().toString();
        }
        return "";
    }

    // 杀死特定实体
    public static int _serverKillEntity(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            final var entity = entityOpt.get();
            if (entity.level() instanceof ServerLevel serverLevel)
            {
                entity.kill(serverLevel);
                return 1;
            }
            return 0;
        }
        return 0;
    }

    // 销毁特定实体
    public static int _serverDestroyEntity(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isPresent())
        {
            final var entity = entityOpt.get();
            if (entity.level() instanceof ServerLevel && !(entity instanceof Player))
            {
                entity.discard();
                return 1;
            }
            return 0;
        }
        return 0;
    }

    // 获取所有玩家ID
    public static String _serverGetAllPlayerId()
    {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null)
        {
            return "";
        }

        StringBuilder sb = new StringBuilder();
        for (ServerPlayer player : server.getPlayerList().getPlayers())
        {
            sb.append(player.getUUID()).append(" ");
        }
        if (!sb.isEmpty())
        {
            sb.setLength(sb.length() - 1); // 去掉最后一个空格
        }
        return sb.toString();
    }

    // 获取指定实体的目标id 如果不存在返回空字符串
    public static String _serverGetEntityTargetId(String entityId)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return "";
        }
        final var entity = entityOpt.get();
        if (entity instanceof Mob mob)
        {
            LivingEntity target = mob.getTarget();
            if (target != null)
            {
                return target.getUUID().toString();
            }
        }
        return "";
    }

    /** 向指定玩家发送一条服务端消息（系统消息） **/
    public static void _serverSendMessage(String entityId, String message)
    {
        var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return;
        }
        if(entityOpt.get() instanceof ServerPlayer player)
        {
            player.sendSystemMessage(Component.literal(message));
        }
    }

    /** 向所有玩家发送消息 **/
    public static void _serverSendMessageAll(String message)
    {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null)
        {
            return;
        }
        Component text = Component.literal(message);
        for (ServerPlayer player : server.getPlayerList().getPlayers())
        {
            player.sendSystemMessage(text);
        }
    }

    /** 客户端玩家创建系统消息 **/
    public static void _clientSendMessage(String msg)
    {
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        if (player != null)
        {
            player.displayClientMessage(Component.literal(msg), false);
        }
    }

    // 服务端获取实体所在维度
    public static int _serverGetEntityDmId(String entityId)
    {
        return WorldUtil.serverGetEntityDimensionId(EntityUtil.serverGetEntityByUUID(entityId).orElse(null));
    }
}
