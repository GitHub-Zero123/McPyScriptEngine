#pragma once
#include <iostream>
#include <jni.h>
#include <vector>

namespace QPyMCBridge
{
	namespace JNI
	{
        // 将 jstring 转换为 std::string（UTF-8）
        inline std::string jStringToStdString(JNIEnv* env, jstring jstr)
        {
            if (jstr == nullptr)
            {
                return "";
            }
            const char* utfChars = env->GetStringUTFChars(jstr, nullptr);
            if (utfChars == nullptr)
            {
                // JVM 内存不足或异常，返回空字符串
                return "";
            }
            std::string str(utfChars);
            env->ReleaseStringUTFChars(jstr, utfChars);
            return str;
        }

        // jobjectArray (Java String[]) 转 std::vector<std::string>
        inline std::vector<std::string> convertJStringArray(JNIEnv* env, jobjectArray jStrArray)
        {
            std::vector<std::string> result;
            if (!jStrArray)
            {
                return result;
            }

            jsize len = env->GetArrayLength(jStrArray);
            result.reserve(len);

            env->PushLocalFrame(16); // 提前分配局部引用空间（16个）

            for (jsize i = 0; i < len; ++i)
            {
                jstring jstr = static_cast<jstring>(env->GetObjectArrayElement(jStrArray, i));
                if (jstr)
                {
                    result.push_back(jStringToStdString(env, jstr));
                    env->DeleteLocalRef(jstr);
                }
            }

            env->PopLocalFrame(nullptr); // 清理所有局部引用
            return result;
        }
	}
}