package org.zero123.PyScriptEngine.Utils;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;

import javax.annotation.Nullable;
import java.util.Optional;

public class BlockUtil
{
    public static String getBlockFullName(BlockState blockState)
    {
        final var key = blockState.getBlockHolder().getKey();
        if(key != null)
        {
            return key.location().toString();
        }
        return "";
    }

    // json解析方块状态
    public static BlockState jsonToBlockState(@Nullable JsonObject jo)
    {
        if (jo == null || !jo.has("name"))
        {
            return Blocks.AIR.defaultBlockState();
        }

        String name = jo.get("name").getAsString();
        try {
            ResourceLocation id = ResourceLocation.tryParse(name);
            if (id != null)
            {
                Optional<Holder.Reference<Block>> optionalHolder = BuiltInRegistries.BLOCK.get(id);
                if (optionalHolder.isPresent())
                {
                    Block block = optionalHolder.get().value();
                    return block.defaultBlockState();
                }
            }
        } catch (Exception ignored) {}
        return Blocks.AIR.defaultBlockState();
    }

    // 解析方块状态
    public static BlockState jsonToBlockState(String joStr)
    {
        if(!joStr.isEmpty())
        {
            try {
                final var json = JsonParser.parseString(joStr);
                if (json != null && json.isJsonObject()) {
                    return jsonToBlockState(json.getAsJsonObject());
                }
            } catch (JsonSyntaxException | IllegalStateException ignored) {
            }
        }
        return Blocks.AIR.defaultBlockState();
    }

    // 方块状态转换为json
    public static JsonObject blockStateToJson(@Nullable BlockState state)
    {
        JsonObject jo = new JsonObject();
        // 获取方块注册名并写入 name 字段
        if(state != null)
        {
            ResourceLocation blockId = BuiltInRegistries.BLOCK.getKey(state.getBlock());
            jo.addProperty("name", blockId.toString());
        }
        else
        {
            jo.addProperty("name", "minecraft:air");
        }
        jo.addProperty("aux", 0);
        return jo;
    }
}
