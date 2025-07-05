package org.zero123.PyMcBridge;

import net.neoforged.fml.loading.FMLPaths;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class Native
{
    private static boolean loaded = false;

    // 线程安全的加载native扩展
    public static synchronized void loadLibrary()
    {
//        System.load("D:/Zero123/Java/PyScriptEngine/libs/PyMCBridge.dll");
//        System.loadLibrary("PyMCBridge");
        if(loaded) { return; }
        loaded = true;
        final var targetPath = initPythonEnvironment();
        // 解压dll文件
        try (InputStream in = Native.class.getResourceAsStream("/natives/PyMCBridge.dll"))
        {
            if (in == null)
            {
                throw new IOException("DLL not found in JAR");
            }
            Path modNativePath = FMLPaths.MODSDIR.get()
                    .resolve("PyScriptEngine")
                    .resolve("PyMCBridge.dll");
            Files.createDirectories(modNativePath.getParent());
//            if (!Files.exists(modNativePath))
//            {
//                Files.copy(in, modNativePath, StandardCopyOption.REPLACE_EXISTING);
//            }
            Files.copy(in, modNativePath, StandardCopyOption.REPLACE_EXISTING);
            System.load(modNativePath.toAbsolutePath().toString());
        } catch (IOException e)
        {
            throw new RuntimeException("Failed to load native library", e);
        }
        ModLoader.setPythonHome(targetPath.toString());
    }

    public static Path initPythonEnvironment()
    {
        try
        {
            final var targetPath = _initPythonEnvironment("/python/Python312.zip", "Python312");
            System.load(targetPath.resolve("python312.dll").toString());
            // ModLoader.setPythonHome(targetPath.toString());
            return targetPath;
        } catch (IOException e)
        {
            throw new RuntimeException(e);
        }
    }

    public static Path _initPythonEnvironment(String zipPack, String version) throws IOException
    {
        Path pVMPath = FMLPaths.MODSDIR.get().resolve("PyScriptEngine/python").resolve(version);
        if (!Files.exists(pVMPath.resolve("python3.dll")))
        {
            extractZipFromJar(zipPack, pVMPath);
        }
        return pVMPath;
    }

    /**
     * 从 JAR 内提取 zip 并解压到指定目录
     * @param jarInternalPath JAR 内部路径（如 "/natives/Python312.zip"）
     * @param extractTo       解压到的目标路径（如 mods/PyScriptEngine/python312）
     * @throws IOException 若资源不存在或解压失败
     */
    public static void extractZipFromJar(String jarInternalPath, Path extractTo) throws IOException
    {
        // 创建目标目录
        Files.createDirectories(extractTo);

        // 从 jar 中读取资源
        try (InputStream zipStream = Native.class.getResourceAsStream(jarInternalPath))
        {
            if (zipStream == null)
            {
                throw new FileNotFoundException("未找到资源：" + jarInternalPath);
            }
            unzip(zipStream, extractTo);
        }
    }

    /**
     * 解压 zip 流到目标路径
     */
    public static void unzip(InputStream zipInputStream, Path targetDir) throws IOException
    {
        try (ZipInputStream zis = new ZipInputStream(zipInputStream))
        {
            ZipEntry entry;
            while ((entry = zis.getNextEntry()) != null)
            {
                Path filePath = targetDir.resolve(entry.getName());
                if (entry.isDirectory()) {
                    Files.createDirectories(filePath);
                } else {
                    Files.createDirectories(filePath.getParent());
                    try (OutputStream out = Files.newOutputStream(filePath))
                    {
                        byte[] buffer = new byte[4096];
                        int len;
                        while ((len = zis.read(buffer)) > 0)
                        {
                            out.write(buffer, 0, len);
                        }
                    }
                }
                zis.closeEntry();
            }
        }
    }
}
