
def getThreadTypeId() -> int:
    """ 获取当前线程ID """
    ...

def isServerThread() -> bool:
    """ 判断当前线程是否为服务器线程 """
    ...

def isClientThread() -> bool:
    """ 判断当前线程是否为客户端线程 """
    ...

def checkJVMIsAlive() -> bool:
    """ 检查JVM是否存活 """
    ...

# 注: 所有的注册Handler将在游戏对应的线程环境关闭时自动清理
def regServerLoaderHandler(func: 'function') -> None:
    """ 注册服务器加载器处理函数"""
    ...

def regClientLoaderHandler(func: 'function') -> None:
    """ 注册客户端加载器处理函数 """
    ...

def regServerDestroyHandler(func: 'function') -> None:
    """ 注册服务器销毁处理函数 """
    ...

def regClientDestroyHandler(func: 'function') -> None:
    """ 注册客户端销毁处理函数 """
    ...

def regPyVMDestroyHandler(func: 'function') -> None:
    """ 注册PyVM销毁处理函数 """
    ...