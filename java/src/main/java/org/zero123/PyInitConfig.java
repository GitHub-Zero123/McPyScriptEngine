package org.zero123;

import net.neoforged.fml.loading.FMLPaths;

import java.io.IOException;
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
    static final boolean debugMode = true;
    // 是否加载pyMods目录
    static final boolean loadModsDir = true;

    // 返回需要添加到PythonVM的环境路径
    public static String[] getEnvPaths()
    {
        ArrayList<String> envPaths = new ArrayList<>();
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
    public static String[] getTargetMods()
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
}
