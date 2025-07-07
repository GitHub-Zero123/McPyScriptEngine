package org.zero123.PyScriptEngine.ModSdk;

import net.minecraft.commands.CommandSource;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import net.minecraft.server.level.ServerPlayer;
import java.util.Objects;

public class Command
{
    // 执行命令
    public static int _setCommand(String cmd, String entityId, int showOutput)
    {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null)
        {
            return 0;
        }
        // 全局执行
        if(entityId.isEmpty())
        {
            CommandSourceStack source = server.createCommandSourceStack().withPermission(4);
            if(showOutput == 0)
            {
                // 禁用控制台提示
                source = source.withSuppressedOutput();
            }
            server.getCommands().performPrefixedCommand(source, cmd);
            return 1;
        }
        // 实体执行(不一定是玩家)
        final var entityOpt = EntityManager.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return 0;
        }

        Entity entity = entityOpt.get();
        CommandSourceStack source;

        if (entity instanceof ServerPlayer player)
        {
            // 玩家：使用自身的 source stack（带权限、位置、反馈）
            source = player.createCommandSourceStack();
        }
        else
        {
            // 非玩家实体：构造虚拟命令源
            source = new CommandSourceStack(
                    CommandSource.NULL,
                    entity.position(),
                    entity.getRotationVector(),
                    (ServerLevel) entity.level(),
                    4, // 权限等级
                    entity.getName().getString(),  // 名字
                    Objects.requireNonNull(entity.getDisplayName()),
                    server,
                    entity
            );
        }

        if (showOutput == 0)
        {
            source = source.withSuppressedOutput();
        }

        server.getCommands().performPrefixedCommand(source, cmd);
        return 1;
    }
}
