#pragma once
#include <iostream>
#include <vector>

namespace Encoding
{
	// 初始化环境编码到统一的UTF8
	void initEnvcode();
    // 辅助函数：将本地编码转换为宽字符
    std::wstring convertToWide(const char*);
    // 辅助函数：将宽字符转换为UTF-8
    std::string convertToUTF8(const std::wstring&);
    // 获取并转换为UTF8的Args参数字符串
    std::string getUTF8Args(const char*);
    // 获取完整的U8参数列表
    std::vector<std::string> getUTF8Vector(int, const char**);
}
