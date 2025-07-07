from .jni import findJavaCls, CAST_TYPE

_NET_MODULE = "org/zero123/PyScriptEngine/Network/NetworkManager"

def _serverSendMsgToClient(playerId: str, msg: str) -> None:
    """ 服务端向单个客户端发送消息 """
    return findJavaCls(_NET_MODULE, "_serverSendMsgToClient", [CAST_TYPE.STRING, CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        str(playerId), msg
    )

def _serverSendMsgToMutClients(playerList: list, msg: str) -> None:
    """ 服务端向多个客户端发送消息 """
    return findJavaCls(_NET_MODULE, "_serverSendMsgToMutClients", [CAST_TYPE.STRING, CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        " ".join(v for v in playerList if v), msg
    )

def _serverSendMsgToAllClients(msg: str) -> None:
    """ 服务端向所有客户端发送消息 """
    return findJavaCls(_NET_MODULE, "_serverSendMsgToAllClients", [CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        msg
    )

def _clientSendMsgToServer(msg: str) -> None:
    """ 客户端向服务端发送消息 """
    return findJavaCls(_NET_MODULE, "_clientSendMsgToServer", [CAST_TYPE.STRING], CAST_TYPE.VOID).call(
        msg
    )