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

    static {
        Native.loadLibrary();
//        System.loadLibrary("PyMCBridge");
//        System.load("D:/Zero123/Java/PyScriptEngine/libs/PyMCBridge.dll");
    }
}
