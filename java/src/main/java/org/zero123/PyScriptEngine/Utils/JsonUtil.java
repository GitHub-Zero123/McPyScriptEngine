package org.zero123.PyScriptEngine.Utils;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class JsonUtil
{
    public static int getIntOrDefault(JsonObject obj, String key, int defaultValue)
    {
        if (obj == null || !obj.has(key))
        {
            return defaultValue;
        }
        JsonElement elem = obj.get(key);
        try {
            if (elem.isJsonPrimitive())
            {
                return elem.getAsInt();
            }
        } catch (Exception ignored) {}
        return defaultValue;
    }

    public static float getFloatOrDefault(JsonObject obj, String key, float defaultValue)
    {
        if (obj == null || !obj.has(key))
        {
            return defaultValue;
        }
        JsonElement elem = obj.get(key);
        try {
            if (elem.isJsonPrimitive()) {
                return elem.getAsFloat();
            }
        } catch (Exception ignored) {
        }
        return defaultValue;
    }
}
