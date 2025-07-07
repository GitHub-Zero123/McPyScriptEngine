package org.zero123.PyScriptEngine.Network;

import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientPacketListener;
import net.minecraft.network.protocol.common.ServerboundCustomPayloadPacket;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import org.zero123.PyScriptEngine.ModSdk.EntityManager;

public class NetworkManager
{
    // 服务端发包给指定客户端
    public static void _serverSendMsgToClient(String playerId, String msg)
    {
        final var entityOpt = EntityManager.serverGetEntityByUUID(playerId);
        if(entityOpt.isEmpty())
        {
            return;
        }
        final var entity = entityOpt.get();
        if(entity instanceof ServerPlayer player)
        {
            Packet packet = new Packet(msg);
            player.connection.send(packet.toVanillaClientbound());
        }
    }

    // 服务端发包给指定一批玩家客户端
    public static void _serverSendMsgToMutClients(String playerIds, String msg)
    {
        if(playerIds.isEmpty())
        {
            return;
        }
        Packet packet = new Packet(msg);
        var clientPacket = packet.toVanillaClientbound();
        for(var playerId : playerIds.trim().split("\\s+"))
        {
            final var entityOpt = EntityManager.serverGetEntityByUUID(playerId);
            if(entityOpt.isEmpty())
            {
                continue;
            }
            final var entity = entityOpt.get();
            if(entity instanceof ServerPlayer player)
            {
                player.connection.send(clientPacket);
            }
        }
    }

    // 服务端发包给全体客户端
    public static void _serverSendMsgToAllClients(String msg)
    {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null)
        {
            return;
        }
        Packet packet = new Packet(msg);
        var clientPacket = packet.toVanillaClientbound();
        for (ServerPlayer player : server.getPlayerList().getPlayers())
        {
            player.connection.send(clientPacket);
        }
    }

    // 客户端发包给服务端
    public static void _clientSendMsgToServer(String msg)
    {
        Packet packet = new Packet(msg);
        ServerboundCustomPayloadPacket vanillaPacket = packet.toVanillaServerbound();
        Minecraft mc = Minecraft.getInstance();
        ClientPacketListener connection = mc.getConnection();
        if (connection != null)
        {
            connection.send(vanillaPacket);
        }
    }
}
