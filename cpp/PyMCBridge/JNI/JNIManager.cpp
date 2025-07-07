#include "JNIManager.h"
#include <iostream>
#include <pybind11/embed.h>
#include <pybind11/stl.h>
#include <format>

namespace py = pybind11;

static JavaVM* jvm = nullptr;

extern "C"
{

    JNIEXPORT jint JNI_OnLoad(JavaVM* vm, void* reserved)
    {
        jvm = vm;
        return JNI_VERSION_1_6;
    }

    JNIEXPORT void JNI_OnUnload(JavaVM*, void*)
    {
        jvm = nullptr;
    }
}

class JVMFunction
{
private:
    JavaVM* jvm_;
    jclass cls_ = nullptr;         // 全局引用，防止被回收
    jmethodID methodId_ = nullptr;
    std::string classPath_;
    std::string methodName_;
    std::string methodSig_;
    // mutable std::mutex mutex_;

public:
    // 构造时查找并缓存jclass与methodId
    JVMFunction(JavaVM* jvm, const std::string& classPath, const std::string& methodName, const std::string& methodSig)
        : jvm_(jvm), classPath_(classPath), methodName_(methodName), methodSig_(methodSig)
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env)
        {
            throw std::runtime_error("JNI环境错误");
        }

        std::string fixedPath = classPath_;
        // std::replace(fixedPath.begin(), fixedPath.end(), '.', '/');

        jclass localCls = env->FindClass(fixedPath.c_str());
        if (!localCls)
        {
            throw std::runtime_error("找不到目标class: " + fixedPath);
        }

        // 创建全局引用防止被GC回收
        cls_ = (jclass)env->NewGlobalRef(localCls);
        env->DeleteLocalRef(localCls);

        if (!cls_)
        {
            return;
        }

        methodId_ = env->GetStaticMethodID(cls_, methodName_.c_str(), methodSig_.c_str());
        if (!methodId_)
        {
            env->DeleteGlobalRef(cls_);
            cls_ = nullptr;
            throw std::runtime_error("找不到目标函数: " + methodName_);
        }
    }

    ~JVMFunction()
    {
        if (cls_)
        {
            JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
            if (env && QPyMCBridge::JNI::getJVMLiveState())
            {
                env->DeleteGlobalRef(cls_);
            }
            cls_ = nullptr;
        }
    }

    // 禁止复制，允许移动
    JVMFunction(const JVMFunction&) = delete;
    JVMFunction& operator=(const JVMFunction&) = delete;

    JVMFunction(JVMFunction&& other) noexcept
        : jvm_(other.jvm_), cls_(other.cls_), methodId_(other.methodId_),
        classPath_(std::move(other.classPath_)), methodName_(std::move(other.methodName_)),
        methodSig_(std::move(other.methodSig_))
    {
        other.cls_ = nullptr;
        other.methodId_ = nullptr;
    }

    JVMFunction& operator=(JVMFunction&& other) noexcept
    {
        if (this != &other)
        {
            this->~JVMFunction();
            jvm_ = other.jvm_;
            cls_ = other.cls_;
            methodId_ = other.methodId_;
            classPath_ = std::move(other.classPath_);
            methodName_ = std::move(other.methodName_);
            methodSig_ = std::move(other.methodSig_);
            other.cls_ = nullptr;
            other.methodId_ = nullptr;
        }
        return *this;
    }

    // 判断是否有效
    bool valid() const
    {
        return cls_ != nullptr && methodId_ != nullptr;
    }

    // 有参Object返回类型调用
    jobject objectFuncCall(const std::vector<jvalue>& args) const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        jobject result = env->CallStaticObjectMethodA(cls_, methodId_, args.data());
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
        return result;
    }

    // 无参Object返回类型调用
    jobject objectFuncCall() const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        jobject result = env->CallStaticObjectMethod(cls_, methodId_);
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
        return result;
    }

    int callStaticIntMethod(const std::vector<jvalue>& args) const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        jint result = env->CallStaticIntMethodA(cls_, methodId_, args.data());
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
        return result;
    }

    // 无参版本
    int callStaticIntMethod() const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        jint result = env->CallStaticIntMethod(cls_, methodId_);
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
        return result;
    }

    void callStaticVoidMethod(const std::vector<jvalue>& args) const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        env->CallStaticVoidMethodA(cls_, methodId_, args.data());
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
    }

    // 无参版本
    void callStaticVoidMethod() const
    {
        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            throw std::runtime_error("无效的JVM对象");
        }

        env->CallStaticVoidMethod(cls_, methodId_);
        if (env->ExceptionCheck())
        {
            env->ExceptionDescribe();
            env->ExceptionClear();
            throw std::runtime_error("JVM函数调用异常");
        }
    }
};

enum CAST_TYPE
{
    VOID = 0,
    INT = 1,
    STRING = 2,
};

static std::string getJavaSignature(const std::vector<CAST_TYPE>& paramTypes, CAST_TYPE returnType)
{
    std::string sig = "(";

    for (CAST_TYPE type : paramTypes)
    {
        if (type == CAST_TYPE::VOID)
        {
            throw std::invalid_argument("VOID cannot be used as a parameter type");
        }

        switch (type)
        {
        case CAST_TYPE::INT:
            sig += "I";
            break;
        case CAST_TYPE::STRING:
            sig += "Ljava/lang/String;";
            break;
        default:
            throw std::invalid_argument("Unsupported CAST_TYPE in parameters");
        }
    }

    sig += ")";

    switch (returnType)
    {
    case CAST_TYPE::VOID:
        sig += "V";
        break;
    case CAST_TYPE::INT:
        sig += "I";
        break;
    case CAST_TYPE::STRING:
        sig += "Ljava/lang/String;";
        break;
    default:
        throw std::invalid_argument("Unsupported CAST_TYPE in return type");
    }

    return sig;
}

class PyCastJVMFunction : public JVMFunction
{
private:
    const std::vector<CAST_TYPE> argsType;
    CAST_TYPE retType;
public:
    PyCastJVMFunction(const std::string& clsPath,
        const std::string& funcName,
        const std::vector<CAST_TYPE>& argsType,
        CAST_TYPE retType = CAST_TYPE::VOID)
        : JVMFunction(jvm, clsPath, funcName, getJavaSignature(argsType, retType)),
        argsType(argsType), retType(retType) {}

    py::object _call(const py::args& args, const bool noGIL)
    {
        if (args.size() != argsType.size())
        {
            throw std::runtime_error("调用参数数量不一致");
        }

        JNIEnv* env = QPyMCBridge::JNI::getJNIEnv();
        if (!env || !valid())
        {
            std::cerr << env << "\n";
            throw std::runtime_error("无效的JVM指针");
        }

        // 转换参数
        std::vector<jvalue> jargs(args.size());
        std::vector<jstring> localStrRefs; // 用来存临时jstring，方便统一释放

        for (size_t i = 0; i < args.size(); i++)
        {
            switch (argsType[i])
            {
            case CAST_TYPE::INT:
                jargs[i].i = args[i].cast<int>();
                break;

            case CAST_TYPE::STRING:
            {
                std::string s = args[i].cast<std::string>();
                jstring jstr = env->NewStringUTF(s.c_str());
                if (!jstr)
                {
                    // 内存或JVM异常
                    throw std::runtime_error("Failed to create Java string");
                }
                jargs[i].l = jstr;
                localStrRefs.push_back(jstr);
                break;
            }

            default:
                throw std::runtime_error("不支持的参数类型");
            }
        }

        py::object retVal = py::none();
        std::optional<py::gil_scoped_release> gil;
        if (noGIL)
        {
            gil.emplace();
        }
        try
        {
            switch (retType)
            {
            case CAST_TYPE::VOID:
            {                
                if (jargs.size() == 0)
                {
                    callStaticVoidMethod();
                }
                else
                {
                    callStaticVoidMethod(jargs);
                }
				gil.reset();
                retVal = py::none();
                break;
            }

            case CAST_TYPE::INT:
            {
                int res = 0;
                if (jargs.size() == 0)
                {
                    res = callStaticIntMethod();
                }
                else
                {
                    res = callStaticIntMethod(jargs);
                }
                gil.reset();
                retVal = py::int_(res);
                break;
            }

            case CAST_TYPE::STRING:
            {
                jobject jres;
                if (jargs.size() == 0)
                {
                    jres = objectFuncCall();
                }
                else
                {
                    jres = objectFuncCall(jargs);
                }
                gil.reset();
                if (jres == nullptr)
                {
                    retVal = py::none();
                }
                else
                {
                    jstring jstr = static_cast<jstring>(jres);
                    const char* cstr = env->GetStringUTFChars(jstr, nullptr);
                    retVal = py::str(cstr);
                    env->ReleaseStringUTFChars(jstr, cstr);
                    env->DeleteLocalRef(jstr);
                }
                break;
            }

            default:
                throw std::runtime_error("不支持的返回类型");
            }

            if (env->ExceptionCheck())
            {
                env->ExceptionDescribe();
                env->ExceptionClear();
                throw std::runtime_error("JVM函数调用异常");
            }
        }
        catch (...)
        {
            // 释放所有临时字符串引用
            for (jstring s : localStrRefs)
            {
                env->DeleteLocalRef(s);
            }
            throw;
        }

        // 调用结束后释放所有临时字符串引用
        for (jstring s : localStrRefs)
        {
            env->DeleteLocalRef(s);
        }
        return retVal;
    }

    py::object call(const py::args& args)
    {
        return _call(args, false);
    }

    py::object noGILCall(const py::args& args)
    {
        return _call(args, true);
    }
};

namespace QPyMCBridge
{
    namespace JNI
    {
        // 获取当前线程的JNI环境
        JNIEnv* QPyMCBridge::JNI::getJNIEnv()
        {
            JNIEnv* env = nullptr;
            jint ret = jvm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6);
            if (ret == JNI_EDETACHED)
            {
                // 当前线程未附着JVM，尝试附着
                if (jvm->AttachCurrentThread(reinterpret_cast<void**>(&env), nullptr) != 0)
                {
                    throw std::runtime_error("无法附着当前线程到JVM");
                }
            }
            else if (ret != JNI_OK)
            {
                throw std::runtime_error("JNI环境获取异常");
            }
            return env;
        }

        static bool testJNILiveState(JavaVM* targetJvm, JNIEnv* env)
        {
            jint status = targetJvm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6);
            if (status == JNI_EDETACHED)
            {
                if (jvm->AttachCurrentThread(reinterpret_cast<void**>(&env), nullptr) != JNI_OK)
                {
                    return false;
                }
            }
            else if (status != JNI_OK)
            {
                return false;
            }
            return true;
        }

        // 获取JVM存活状态
        bool getJVMLiveState()
        {
            if (!jvm)
            {
                return false;
            }
            return testJNILiveState(jvm, getJNIEnv());
        }

        void _JNIModuleReg(pybind11::module_* m)
        {
            pybind11::module_ jniModule = m->def_submodule("JNI");

            py::enum_<CAST_TYPE>(jniModule, "CAST_TYPE")
                .value("VOID", CAST_TYPE::VOID)
                .value("INT", CAST_TYPE::INT)
                .value("STRING", CAST_TYPE::STRING)
                .export_values();

            py::class_<PyCastJVMFunction>(jniModule, "PyCastJVMFunction")
                .def(py::init<const std::string&, const std::string&, const std::vector<CAST_TYPE>&, CAST_TYPE>(),
                    py::arg("clsPath"),
                    py::arg("funcName"),
                    py::arg("argsType"),
                    py::arg("retType") = CAST_TYPE::VOID)
                .def("call", &PyCastJVMFunction::call)
                .def("noGILCall", &PyCastJVMFunction::noGILCall);
        }
    }
}