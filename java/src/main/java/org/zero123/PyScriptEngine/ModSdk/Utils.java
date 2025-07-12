package org.zero123.PyScriptEngine.ModSdk;

import java.util.ArrayList;

public class Utils
{
    public static <T> String arrayToString(T[] obs)
    {
        if (obs == null || obs.length == 0)
        {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        for (Object obj : obs)
        {
            if (!sb.isEmpty())
            {
                sb.append(" ");
            }
            sb.append(obj);
        }
        return sb.toString();
    }

    public static int[] parseIntArray(String input)
    {
        if (input == null || input.isBlank()) {
            return new int[0];
        }

        String[] parts = input.trim().split("\\s+"); // 按空格分隔
        int[] result = new int[parts.length];
        for (int i = 0; i < parts.length; i++)
        {
            result[i] = Integer.parseInt(parts[i]);
        }
        return result;
    }

    public static double[] parseDoubleArray(String input)
    {
        if (input == null || input.isBlank()) {
            return new double[0];
        }

        String[] parts = input.trim().split("\\s+"); // 按空格分隔
        double[] result = new double[parts.length];
        for (int i = 0; i < parts.length; i++)
        {
            result[i] = Double.parseDouble(parts[i]);
        }
        return result;
    }

    // 拼接字符串列表
    public static String joinWithSpace(ArrayList<String> list)
    {
        if (list == null || list.isEmpty())
        {
            return "";
        }
        StringBuilder builder = new StringBuilder();
        for (String s : list)
        {
            builder.append(s).append(' ');
        }
        builder.setLength(builder.length() - 1); // 移除最后一个空格
        return builder.toString();
    }
}
