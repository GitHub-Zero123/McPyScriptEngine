package org.zero123.PyScriptEngine.Network;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.protocol.common.ClientboundCustomPayloadPacket;
import net.minecraft.network.protocol.common.ServerboundCustomPayloadPacket;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import org.jetbrains.annotations.NotNull;
import org.zero123.PyScriptEngine.PyScriptEngine;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.zip.DeflaterOutputStream;
import java.util.zip.InflaterInputStream;

public record Packet(String message) implements CustomPacketPayload
{
    // 网络包类型
    public static final Type<Packet> TYPE = new Type<>(
            ResourceLocation.fromNamespaceAndPath(PyScriptEngine.MODID, "net_pack")
    );

    // 从网络缓冲区反序列化构造
    public Packet(FriendlyByteBuf buf)
    {
        this(readCompressedString(buf));
    }

    // 序列化数据写入缓冲区
    public void write(FriendlyByteBuf buf)
    {
        writeCompressedString(buf, message);
    }

    @Override
    public @NotNull Type<? extends CustomPacketPayload> type()
    {
        return TYPE;
    }

    @Override
    public @NotNull ServerboundCustomPayloadPacket toVanillaServerbound()
    {
        // 直接用 this 构造，框架会调用 write() 自动序列化
        return new ServerboundCustomPayloadPacket(this);
    }

    @Override
    public @NotNull ClientboundCustomPayloadPacket toVanillaClientbound()
    {
        return new ClientboundCustomPayloadPacket(this);
    }

    // 🔧 压缩并写入
    private static void writeCompressedString(FriendlyByteBuf buf, String str)
    {
        try
        {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            try (DeflaterOutputStream dos = new DeflaterOutputStream(baos))
            {
                dos.write(str.getBytes(StandardCharsets.UTF_8));
            }
            byte[] compressed = baos.toByteArray();
            buf.writeVarInt(compressed.length);
            buf.writeByteArray(compressed);
        } catch (Exception e)
        {
            throw new RuntimeException("Failed to compress string", e);
        }
    }

    // 🔧 解压读取
    private static String readCompressedString(FriendlyByteBuf buf)
    {
        try
        {
            int length = buf.readVarInt();
            byte[] compressed = buf.readByteArray(length);
            ByteArrayInputStream bais = new ByteArrayInputStream(compressed);
            try (InflaterInputStream iis = new InflaterInputStream(bais))
            {
                return new String(iis.readAllBytes(), StandardCharsets.UTF_8);
            }
        } catch (Exception e)
        {
            throw new RuntimeException("Failed to decompress string", e);
        }
    }
}
