package org.zero123.PyMcBridge;
// By Zero123

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class EventManager
{
    /*
        事件管理器提供了native事件广播接口
     */
    public static native void callServerEvent(int eventId);
    public static native void callClientEvent(int eventId);
    public static native void callServerJsonEvent(int eventId, String json);
    public static native void callClientJsonEvent(int eventId, String json);
    public static native String callServerEventCap(int eventId, String json, String[] captureKeys);
    public static native String callClientEventCap(int eventId, String json, String[] captureKeys);

    public static class Client
    {
        // 无参事件广播
        public static void callEvent(int eventId)
        {
            EventManager.callClientEvent(eventId);
        }

        // 有参事件广播
        public static void callEvent(int eventId, JsonObject json)
        {
            EventManager.callClientJsonEvent(eventId, json.toString());
        }

        // 有参且捕获变化的事件广播
        public static JsonObject callEvent(int eventId, JsonObject json, String[] captureKeys)
        {
            final var retJson = EventManager.callClientEventCap(eventId, json.toString(), captureKeys);
            if(retJson.isEmpty() || retJson.equals("{}"))
            {
                return new JsonObject();
            }
            return JsonParser.parseString(retJson).getAsJsonObject();
        }
    }

    public static class Server
    {
        // 无参事件广播
        public static void callEvent(int eventId)
        {
            EventManager.callServerEvent(eventId);
        }

        // 有参事件广播
        public static void callEvent(int eventId, JsonObject json)
        {
            EventManager.callServerJsonEvent(eventId, json.toString());
        }

        // 有参且捕获变化的事件广播
        public static JsonObject callEvent(int eventId, JsonObject json, String[] captureKeys)
        {
            final var retJson = EventManager.callServerEventCap(eventId, json.toString(), captureKeys);
            if(retJson.isEmpty() || retJson.equals("{}"))
            {
                return new JsonObject();
            }
            return JsonParser.parseString(retJson).getAsJsonObject();
        }
    }

    static {
        Native.loadLibrary();
//        System.loadLibrary("PyMCBridge");
//        System.load("D:/Zero123/Java/PyScriptEngine/libs/PyMCBridge.dll");
    }
}
