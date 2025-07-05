package org.zero123;

public class PyInitConfig
{
    // 返回需要添加到PythonVM的环境路径(以便import搜索)
    public static String[] getEnvPaths()
    {
        // 在此添加环境目录
        return new String[] {
            "D:/Zero123/Minecraft/MODSDK_ENV"
        };
    }

    // 获取需要加载的Mod列表(本质上是 import {name}.modMain)
    public static String[] getTargetMods()
    {
        // 在此添加需要加载的Mod包
        return new String[] {
            "testMod_0"
        };
    }
}
