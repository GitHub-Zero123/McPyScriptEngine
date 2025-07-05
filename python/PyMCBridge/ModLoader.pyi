
def getThreadTypeId() -> int:
    """ 获取当前线程ID """
    pass

def isServerThread() -> bool:
    """ 判断当前线程是否为服务器线程 """
    pass

def isClientThread() -> bool:
    """ 判断当前线程是否为客户端线程 """
    pass

def checkJVMIsAlive() -> bool:
    """ 检查JVM是否存活 """
    pass

# 注: 所有的注册Handler将在游戏对应的线程环境关闭时自动清理
def regServerLoaderHandler(func: function) -> bool:
    """ 注册服务器加载器处理函数"""
    pass

def regClientLoaderHandler(func: function) -> bool:
    """ 注册客户端加载器处理函数 """
    pass

def regServerDestroyHandler(func: function) -> bool:
    """ 注册服务器销毁处理函数 """
    pass

def regClientDestroyHandler(func: function) -> bool:
    """ 注册客户端销毁处理函数 """
    pass