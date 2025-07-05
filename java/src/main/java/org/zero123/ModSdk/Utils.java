package org.zero123.ModSdk;

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
}
