package org.zero123.PyScriptEngine.ModSdk;

import org.zero123.PyScriptEngine.Utils.EntityUtil;

public class ItemModule
{
    // 服务端获取实体手中物品信息
    public static String _serverGetEntityHandItemInfo(String entityId)
    {
        final var entityOpt = EntityUtil.serverGetEntityByUUID(entityId);
        if(entityOpt.isEmpty())
        {
            return "";
        }
        final var entity = entityOpt.get();
        final var itemStackOpt = ItemUtil.getEntityHandItem(entity);
        if(itemStackOpt.isEmpty())
        {
            return "";
        }
        final var itemStack = itemStackOpt.get();
        return ItemUtil.itemStackToJo(itemStack).toString();
    }
}
