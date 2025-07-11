package org.zero123.PyMcBridge;
// By Zero123

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

    static {
        System.loadLibrary("PyMCBridge");
    }
}
