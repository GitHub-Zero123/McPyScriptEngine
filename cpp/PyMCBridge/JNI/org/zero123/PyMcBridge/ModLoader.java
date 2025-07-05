package org.zero123.PyMcBridge;
import java.util.concurrent.CountDownLatch;
// By Zero123

public class ModLoader
{
    /*
     * 关于 PythonVM 生命周期:
     * - 当任意线程加载时，自动创建 PythonVM 实例。
     * - 当所有线程均卸载时，自动销毁 PythonVM 实例。
     *
     * 关于线程安全:
     * - 几乎所有方法都不是线程安全的, 请在对应的线程下调用
     * - VM相关接口为全局配置, 只需要在vm创建前调用一次即可(同样不是线程安全的需要自行加锁)
     */

    // 加载服务端线程(需在对应的线程下调用)
    public static native void loadServerThread();

    // 加载客户端线程(需在对应的线程下调用)
    public static native void loadClientThread();

    // 卸载服务端线程(需在对应的线程下调用)
    public static native void destroyServerThread();

    // 卸载客户端线程(需在对应的线程下调用)
    public static native void destroyClientThread();

    // 获取Py服务端线程存活状态
    public static native int getPyServerLiveState();

    // 获取Py客户端线程存活状态
    public static native int getPyClientLiveState();

    // 刷新PyVM标准输出流(需在VM创建完毕之后调用)
    public static native void flushPyStdout();

    // 动态执行Python代码(需在VM创建完毕之后调用)
    public static native void execPyCode(String code);
    
    // -------------- VM配置相关接口(需在VM创建之前调用) --------------

    // 添加环境变量路径 可随时调用 即便没有创建VM
    public static native void addEnvPath(String path);

    // 设置目标MOD列表(在启动后会自动加载)
    public static native void setTargetMods(String[] mods);

    // 设置Py输出流强制使用UTF8编码
    public static native void setPyForceUseUTF8(int state);

    // 设置PythonHome路径(需在创建VM前调用)以便加载解释器(pythonXX.dll)
    public static native void setPythonHome(String path);

    // 设置Py输出流按行刷新
    public static native void setPyLineFlushMode(boolean state);

    static {
        System.loadLibrary("PyMCBridge");
    }

    // -------------- Java封装实现 --------------

    private static final CountDownLatch vmInitLatch = new CountDownLatch(1);
    private static volatile boolean initialized = false;

    /**
     * 执行一次初始化配置，且保证其他线程阻塞等待直到初始化完成。
     */
    public static void initializeVMConfigOnce(Runnable configHandler) {
        // 快速判断是否已经初始化过
        if (initialized) {
            // 已经初始化，直接返回
            return;
        }

        synchronized (ModLoader.class) {
            if (!initialized) {
                try {
                    configHandler.run();
                    initialized = true;
                } finally {
                    vmInitLatch.countDown();  // 释放等待线程
                }
            }
        }

        // 如果当前线程不是执行初始化的线程，则等待初始化完成
        if (!initialized) {
            try {
                vmInitLatch.await();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("初始化等待被中断", e);
            }
        }
    }
}