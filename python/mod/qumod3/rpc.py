from .entity import Entity, ServerEntity
from ..server.system.serverSystem import ServerSystemManager
from ..client.system.clientSystem import ClientSystemManager
import PyMCBridge.ModLoader as _ModLoader # type: ignore

class RpcBridge:
    _SERVER_THREAD_EMS = "This method can only be called from the server thread."
    def __init__(self, namespace: str):
        # 需要通过命名空间来化分数据包处理
        self.namespace = namespace

    def serverRpc(self, func):
        """
        绑定服务端RPC函数
        """
        self.registerServerRPC(func.__name__, func)
        self.registerServerRPC(func.__qualname__, func)
        return func

    def clientRpc(self, func):
        """
        绑定客户端RPC函数
        """
        self.registerClientRPC(func.__name__, func)
        self.registerClientRPC(func.__qualname__, func)
        return func

    def registerServerRPC(self, bindName: str, func: 'function'):
        """
        注册服务端RPC函数
        """
        return RPCManager.getInstance().registerServerRPC(self.namespace, bindName, func)

    def registerClientRPC(self, bindName: str, func: 'function'):
        """
        注册客户端RPC函数
        """
        return RPCManager.getInstance().registerClientRPC(self.namespace, bindName, func)

    def callServer(self, bind, *args, **kwargs):
        """
        客户端调用服务端RPC函数
        """
        if not _ModLoader.isClientThread():
            raise RuntimeError("This method can only be called from the client thread.")
        if callable(bind):
            bind = bind.__qualname__
        return RPCManager.getInstance().callServerRpc(self.namespace, bind, *args, **kwargs)

    def callClient(self, player, bind, *args, **kwargs):
        """
        服务端调用客户端RPC函数
        """
        if not _ModLoader.isServerThread():
            raise RuntimeError(RpcBridge._SERVER_THREAD_EMS)
        playerId = player.entityId if isinstance(player, Entity) else player
        if callable(bind):
            bind = bind.__qualname__
        return RPCManager.getInstance().callClientRpc(playerId, self.namespace, bind, *args, **kwargs)

    def callMutClient(self, playerIds: list[str | Entity], bind, *args, **kwargs):
        """
        服务端调用多个客户端RPC函数
        """
        if not _ModLoader.isServerThread():
            raise RuntimeError(RpcBridge._SERVER_THREAD_EMS)
        playerIds = [player.entityId if isinstance(player, Entity) else player for player in playerIds]
        if callable(bind):
            bind = bind.__qualname__
        return RPCManager.getInstance().callMutClientRpc(playerIds, self.namespace, bind, *args, **kwargs)

    def callAllClient(self, bind, *args, **kwargs):
        """
        服务端调用所有客户端RPC函数
        """
        if not _ModLoader.isServerThread():
            raise RuntimeError(RpcBridge._SERVER_THREAD_EMS)
        if callable(bind):
            bind = bind.__qualname__
        return RPCManager.getInstance().callAllClientRpc(self.namespace, bind, *args, **kwargs)
    
    @staticmethod
    def getCurrentRpcSenderId() -> str:
        """ 服务端获取当前发包者玩家ID """
        return RPCManager.getInstance()._tempServerPlayerId

    @staticmethod
    def getCurrentRpcSenderEntity() -> ServerEntity | None:
        """ 服务端获取当前发包者玩家实体 """
        if not _ModLoader.isServerThread():
            raise RuntimeError("This method can only be called from the server thread.")
        playerId = RPCManager.getInstance()._tempServerPlayerId
        if playerId:
            return ServerEntity(playerId)
        return None

class RPCManager:
    _INSTANCE = None
    _EVENT_NAME = "RPCEvent"

    @staticmethod
    def getInstance():
        if RPCManager._INSTANCE is None:
            RPCManager._INSTANCE = RPCManager()
        return RPCManager._INSTANCE

    def __init__(self):
        self.serverRpcBind: dict[str, dict] = {}
        self.clientRpcBind: dict[str, dict] = {}
        self._tempServerPlayerId = ""
        self._initServerNetwork()
        self._initClientNetwork()

    def _initServerNetwork(self):
        """
        初始化服务端网络
        """
        def networkPacketReceived(args: dict):
            self._tempServerPlayerId = args.get("__id__", "")
            namespace = args.get("n", "")
            bindName = args.get("b", "")
            argsList = args.get("a", [])
            kwargsDict = args.get("k", {})
            rpcFunc = self.getServerRpc(namespace, bindName)
            if rpcFunc:
                rpcFunc(*argsList, **kwargsDict)
            else:
                raise RuntimeError(f"RPC function not found: {namespace}::{bindName}")
        ServerSystemManager.getInstance().listenForEvent(RPCManager._EVENT_NAME, networkPacketReceived)

    def _initClientNetwork(self):
        """
        初始化客户端网络
        """
        def networkPacketReceived(args: dict):
            namespace = args.get("n", "")
            bindName = args.get("b", "")
            argsList = args.get("a", [])
            kwargsDict = args.get("k", {})
            rpcFunc = self.getClientRpc(namespace, bindName)
            if rpcFunc:
                rpcFunc(*argsList, **kwargsDict)
            else:
                raise RuntimeError(f"RPC function not found: {namespace}::{bindName}")
        ClientSystemManager.getInstance().listenForEvent(RPCManager._EVENT_NAME, networkPacketReceived)

    def registerServerRPC(self, namespace: str, bindName: str, func: 'function'):
        """
        注册服务端RPC函数
        """
        if namespace not in self.serverRpcBind:
            self.serverRpcBind[namespace] = {}
        self.serverRpcBind[namespace][bindName] = func
    
    def registerClientRPC(self, namespace: str, bindName: str, func: 'function'):
        """
        注册客户端RPC函数
        """
        if namespace not in self.clientRpcBind:
            self.clientRpcBind[namespace] = {}
        self.clientRpcBind[namespace][bindName] = func
    
    def getServerRpc(self, namespace: str, bindName: str):
        """
        获取服务端RPC函数
        """
        return self.serverRpcBind.get(namespace, {}).get(bindName)

    def getClientRpc(self, namespace: str, bindName: str):
        """
        获取客户端RPC函数
        """
        return self.clientRpcBind.get(namespace, {}).get(bindName)
    
    @staticmethod
    def packArgs(namespace: str, bindName: str, *args, **kwargs):
        return {
            "n": namespace,
            "b": bindName,
            "a": list(args),
            "k": dict(kwargs)
        }
    
    def callServerRpc(self, namespace: str, bindName: str, *args, **kwargs):
        """
        调用服务端RPC函数
        """
        ClientSystemManager.getInstance().sendToServer(RPCManager._EVENT_NAME, RPCManager.packArgs(namespace, bindName, *args, **kwargs))

    def callClientRpc(self, playerId: str, namespace: str, bindName: str, *args, **kwargs):
        """
        调用客户端RPC函数
        """
        ServerSystemManager.getInstance().sendEventToClient(playerId, RPCManager._EVENT_NAME, RPCManager.packArgs(namespace, bindName, *args, **kwargs))

    def callMutClientRpc(self, playerIds: list[str], namespace: str, bindName: str, *args, **kwargs):
        """
        调用多个客户端RPC函数
        """
        ServerSystemManager.getInstance().sendEventToMultiClients(playerIds, RPCManager._EVENT_NAME, RPCManager.packArgs(namespace, bindName, *args, **kwargs))
    
    def callAllClientRpc(self, namespace: str, bindName: str, *args, **kwargs):
        """
        调用所有客户端RPC函数
        """
        ServerSystemManager.getInstance().sendEventToAllClient(RPCManager._EVENT_NAME, RPCManager.packArgs(namespace, bindName, *args, **kwargs))