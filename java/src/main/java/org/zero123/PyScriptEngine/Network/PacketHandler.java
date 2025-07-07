package org.zero123.PyScriptEngine.Network;

import com.google.gson.JsonObject;
import net.minecraft.network.ConnectionProtocol;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.registration.NetworkRegistry;
import org.jetbrains.annotations.NotNull;
import org.zero123.PyMcBridge.EventManager;

import java.util.List;
import java.util.Optional;

public class PacketHandler
{
    public static class PacketCodec implements StreamCodec<FriendlyByteBuf, Packet>
    {

        public static final PacketCodec INSTANCE = new PacketCodec();

        @Override
        public @NotNull Packet decode(@NotNull FriendlyByteBuf input)
        {
            return new Packet(input);  // 解码构造器
        }

        @Override
        public void encode(@NotNull FriendlyByteBuf output, @NotNull Packet packet)
        {
            packet.write(output);
        }
    }

    public static void init()
    {
        NetworkRegistry.register(
                Packet.TYPE,
                PacketCodec.INSTANCE,
                // 服务器收到客户端发包时处理
                (packet, context) -> {  // 服务器处理器
                    context.enqueueWork(() -> {
                        Player sender = context.player();
                        String msg = packet.message();
                        JsonObject jo = new JsonObject();
                        jo.addProperty("playerId", sender.getUUID().toString());
                        jo.addProperty("msg", msg);
                        EventManager.callServerJsonEvent(-1, jo.toString());
                    });
                },
                // 客户端收到服务器发包时处理
                (packet, context) ->
                {
                    context.enqueueWork(() -> {
                        final var msg = packet.message();
                        JsonObject jo = new JsonObject();
                        jo.addProperty("msg", msg);
                        EventManager.callClientJsonEvent(-1, jo.toString());
                    });
                },
                List.of(ConnectionProtocol.PLAY),   // 适用协议列表
                Optional.empty(),                   // 默认不指定流向
                "1",                                // 版本号（自定义）
                false                               // 非可选包
        );
    }
}
