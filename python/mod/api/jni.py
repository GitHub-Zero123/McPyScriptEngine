import functools
from PyMCBridge.JNI import PyCastJVMFunction, CAST_TYPE # type: ignore
import PyMCBridge.ModLoader as _ModLoader # type: ignore
lambda: "By Zero123"
# 由于JNI自身的性能问题, 完全在CPP上实现获得的提升微忽慎微, 且不利于维护, 因此直接绑定给Python动态调用与缓存

_JAVA_CLS_CACHE = {}    # type: dict[object, PyCastJVMFunction]

def findJavaCls(clsPath: str, methodName: str, argsType: list[CAST_TYPE], returnType: CAST_TYPE=CAST_TYPE.VOID) -> PyCastJVMFunction:
    """ 查找或创建一个Java类的函数绑定(若路径无效可能导致进程崩溃) """
    args = (clsPath, methodName)
    if args in _JAVA_CLS_CACHE:
        return _JAVA_CLS_CACHE[args]
    bindFunc = PyCastJVMFunction(clsPath, methodName, argsType, returnType)
    _JAVA_CLS_CACHE[args] = bindFunc
    return bindFunc

def floatSplit(data: str):
    if not data:
        return None
    return tuple(float(v) for v in data.split(" "))

def numberTupleJoin(data: tuple) -> str:
    return " ".join(str(v) for v in data)

def ClientOnly(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _ModLoader.isClientThread():
            raise RuntimeError(f"函数 {func.__name__} 只能在客户端调用！")
        return func(*args, **kwargs)
    return wrapper

def ServerOnly(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _ModLoader.isServerThread():
            raise RuntimeError(f"函数 {func.__name__} 只能在服务端调用！")
        return func(*args, **kwargs)
    return wrapper