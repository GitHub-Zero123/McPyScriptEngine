package org.zero123;

import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.fml.loading.FMLPaths;
import org.zero123.PyMcBridge.Native;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;

public class PyInitConfig
{
    // 调试环境路径
    static final String[] _debugEnvPaths = {
        "D:/Zero123/Minecraft/MODSDK_ENV"
    };
    // 调试目标modName
    static final String[] _debugTargetMods = {
        "testMod_0", "gameLog"
    };
    // 是否使用调试信息
    static boolean debugMode = true;
    // 是否加载pyMods目录
    static boolean loadModsDir = true;

    static
    {
        if (getProduction())
        {
            // 正式环境处理
            debugMode = false;
            loadModsDir = true;
        }
    }

    public static boolean getProduction()
    {
        return FMLEnvironment.production;
    }

    // 返回需要添加到PythonVM的环境路径
    public static String[] initEnvPaths()
    {
        ArrayList<String> envPaths = new ArrayList<>();
        // 内置标准库扩展(仅正式环境)
        if(getProduction())
        {
            // production标准库环境
            envPaths.add(initStdModule().toString().replace("\\", "/"));
        }
        // mod加载环境配置
        if(loadModsDir)
        {
            envPaths.add(getPyModsPath().toString().replace("\\", "/"));
        }
        if(debugMode)
        {
            Collections.addAll(envPaths, _debugEnvPaths);
        }
        return envPaths.toArray(new String[0]);
    }

    // 获取需要加载的Mod列表(import {name}.modMain)
    public static String[] initTargetMods()
    {
        ArrayList<String> modLists = new ArrayList<>();
        if(loadModsDir)
        {
            findModFoldersWithMainScript(modLists);
        }
        if(debugMode)
        {
            Collections.addAll(modLists, _debugTargetMods);
        }
        return modLists.toArray(new String[0]);
    }

    // 基于入口脚本搜索PythonMods
    public static void findModFoldersWithMainScript(ArrayList<String> ref)
    {
        Path modsDir = getPyModsPath();
        if (!Files.exists(modsDir) || !Files.isDirectory(modsDir))
        {
            // 无效的路径
            return;
        }
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(modsDir))
        {
            for (Path subDir : stream)
            {
                if (Files.isDirectory(subDir))
                {
                    Path mainScript = subDir.resolve("modMain.py");
                    if (Files.exists(mainScript) && Files.isRegularFile(mainScript))
                    {
                        ref.add(subDir.getFileName().toString());
                    }
                }
            }
        } catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    public static Path getPyModsPath()
    {
        return FMLPaths.GAMEDIR.get().resolve("pyMods");
    }

    // 初始化标准库模块
    public static Path initStdModule()
    {
        try {
            final var path = FMLPaths.GAMEDIR.get().resolve("python/MC_LIBS");
            Native.extractZipFromJar("/python/MC_STD.zip", path);
            return path;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
