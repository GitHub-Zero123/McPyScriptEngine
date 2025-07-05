#include "EnvEncode.h"
#include <iostream>
#include <vector>

#ifdef _WIN32
#include <Windows.h>
void Encoding::initEnvcode()
{
    std::locale::global(std::locale(".UTF-8"));
    // 设置控制台输出代码页
    SetConsoleOutputCP(CP_UTF8);
    // 设置控制台输入代码页
    SetConsoleCP(CP_UTF8);
}

// 辅助函数：将本地编码转换为宽字符
std::wstring Encoding::convertToWide(const char* input)
{
    // 计算需要多少字符来容纳转换后的宽字符字符串
    int len = MultiByteToWideChar(CP_ACP, 0, input, -1, nullptr, 0);
    if (len <= 0)
    {
        return L"";
    }
    // 分配足够的空间来保存转换后的宽字符字符串
    std::wstring wideString(len - 1, 0);
    MultiByteToWideChar(CP_ACP, 0, input, -1, &wideString[0], len);
    return wideString;
}

// 辅助函数：将宽字符转换为UTF-8
std::string Encoding::convertToUTF8(const std::wstring& wideString)
{
    // 计算需要多少字符来容纳转换后的宽字符字符串
    int len = WideCharToMultiByte(CP_UTF8, 0, wideString.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (len <= 0)
    {
        return "";
    }
    // 分配足够的空间来保存转换后的字符串
    std::string utf8String(len - 1, 0);
    WideCharToMultiByte(CP_UTF8, 0, wideString.c_str(), -1, &utf8String[0], len, nullptr, nullptr);
    return utf8String;
}

// 获取完整的U8 Args
std::vector<std::string> Encoding::getUTF8Vector(int argc, const char** argv)
{
    std::vector<std::string> vc{};
    for (int i = 0; i < argc; i++)
    {
        vc.push_back(getUTF8Args(argv[i]));
    }
    return vc;
}

// 获取并转换为UTF8的Args参数字符串
std::string Encoding::getUTF8Args(const char* argStr)
{
    // 将本地编码转换为宽字符（UTF-16）
    std::wstring wideArg = convertToWide(argStr);
    if (wideArg.empty())
    {
        return "";  // 如果转换失败，返回空字符串
    }
    // 将宽字符（UTF-16）转换为UTF-8
    return convertToUTF8(wideArg);
}

#else
void Encoding::initEnvcode()
{
    std::locale::global(std::locale(".UTF-8"));
}
#endif