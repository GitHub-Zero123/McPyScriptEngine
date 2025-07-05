
# 注: 所有的监听将在游戏对应的线程环境关闭时自动清理
def listenForServerEvent(eventId: int, func: function) -> bool:
    """ 注册服务器事件监听器 """
    pass

# def unListenForServerEvent(eventId: int, func: function) -> bool:
#     """ 注销服务器事件监听器 """
#     pass

# def unListenForAllServerEvent(eventId: int) -> bool:
#     """ 注销所有服务器事件监听器 """
#     pass

def listenForClientEvent(eventId: int, func: function) -> bool:
    """ 注册客户端事件监听器 """
    pass

# def unListenForClientEvent(eventId: int, func: function) -> bool:
#     """ 注销客户端事件监听器 """
#     pass

# def unListenForAllClientEvent(eventId: int) -> bool:
#     """ 注销所有客户端事件监听器 """
#     pass