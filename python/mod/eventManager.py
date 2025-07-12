lambda: "通用事件管理器"

class EventHandler:
    def __init__(self, handler: 'function', priority=0):
        self.handler = handler
        self._priority = priority

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

    def __lt__(self, other: 'EventHandler'):
        return self._priority > other._priority

    def __eq__(self, other: 'EventHandler'):
        return self.handler == other.handler and self._priority == other._priority

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.handler, self._priority))
    
    def __repr__(self):
        return "<handler: {} priority: {} id: {}>".format(self.handler.__name__, self._priority, id(self))

class EventGroup:
    """ 事件组 包含多个事件处理器 """
    def __init__(self):
        self.handlers = []   # type: list[EventHandler]
        self._handlerSets = set()  # type: set[EventHandler]
        self.needOrder = False

    def hasHandler(self, handler: EventHandler):
        return handler in self._handlerSets

    def add(self, handler: EventHandler):
        if handler in self._handlerSets:
            return False
        if handler._priority == 0:
            self.handlers.append(handler)
        else:
            self.needOrder = True
        self._handlerSets.add(handler)
        return True

    def remove(self, handler: EventHandler):
        if handler in self._handlerSets:
            self._handlerSets.remove(handler)
            self.needOrder = True
            return True
        return False

    def update(self):
        if self.needOrder:
            self.needOrder = False
            self.handlers = sorted(self._handlerSets)

    def call(self, *args):
        self.update()
        for handler in self.handlers[::]:
            try:
                handler(*args)
            except Exception:
                import traceback
                traceback.print_exc()

    def walk(self):
        self.update()
        for handler in self.handlers:
            yield handler

class EventManager:
    """ 事件管理器 """
    def __init__(self):
        self.eventMaps = {}  # type: dict[object, EventGroup]

    def clearMap(self):
        self.eventMaps.clear()

    def regEventHandler(self, event, handler: EventHandler):
        if not event in self.eventMaps:
            self.eventMaps[event] = EventGroup()
        if self.eventMaps[event].add(handler):
            return True
        return False

    def unRegEventHandler(self, event, handler: EventHandler):
        if event in self.eventMaps:
            if self.eventMaps[event].remove(handler):
                return True
        return False

    def callEvent(self, event, *args):
        if event in self.eventMaps:
            self.eventMaps[event].call(*args)

    def regEventFuncHandler(self, event, func, priority=0):
        return self.regEventHandler(event, EventHandler(func, priority))

    def unRegEventFuncHandler(self, event, func, priority=0):
        return self.unRegEventHandler(event, EventHandler(func, priority))

class SERVER_EVENT:
    MOD_LOAD_FINISH = -2
    NETWORK_PACKET_RECEIVED = -1
    UNKNOWN = -100
    SERVER_TICK_PRE = 0
    SERVER_TICK_POST = 1    # Tick事件
    RIGHT_CLICK_ITEM = 2    # 物品尝试使用
    ENTITY_JOIN_LEVEL = 3   # 实体加入世界
    ENTITY_LEAVE_LEVEL = 4  # 实体离开世界
    # 服务端生物受伤事件
    LIVING_INCOMING_DAMAGE = 100     # 生物受到伤害前(未计算护甲值)
    LIVING_DAMAGE_PRE = 101          # 生物受到伤害前(已计算护甲值)
    LIVING_DAMAGE_POST = 102         # 生物受到伤害后(已计算护甲值)
    PLAYER_BLOCK_BREAK = 110         # 玩家尝试破坏方块

class CLIENT_EVENT:
    MOD_LOAD_FINISH = -2
    NETWORK_PACKET_RECEIVED = -1
    UNKNOWN = -100
    CLIENT_TICK_PRE = 0
    CLIENT_TICK_POST = 1    # Tick事件
    RIGHT_CLICK_ITEM = 2    # 物品尝试使用
    ENTITY_JOIN_LEVEL = 3   # 实体加入世界
    ENTITY_LEAVE_LEVEL = 4  # 实体离开世界

_MC_EVENT_MAPPING_TABLE = {
    # MOD加载完成事件
    "LoadServerAddonScriptsAfter": SERVER_EVENT.MOD_LOAD_FINISH,
    "LoadClientAddonScriptsAfter": CLIENT_EVENT.MOD_LOAD_FINISH,
    # 网络包接收事件
    "ServerboundPacketReceivedEvent": SERVER_EVENT.NETWORK_PACKET_RECEIVED,
    "ClientboundPacketReceivedEvent": CLIENT_EVENT.NETWORK_PACKET_RECEIVED,
    # 游戏Tick事件(20tick/s)
    "OnScriptTickServer": SERVER_EVENT.SERVER_TICK_POST,
    "OnScriptTickClient": CLIENT_EVENT.CLIENT_TICK_POST,
    # 物品尝试使用事件
    "ServerItemTryUseEvent": SERVER_EVENT.RIGHT_CLICK_ITEM,
    "ClientItemTryUseEvent": CLIENT_EVENT.RIGHT_CLICK_ITEM,
    # 实体构造/析构事件(新增/删除): 与BE不同, JE的实体与区块一并加载或卸载
    "AddEntityServerEvent": SERVER_EVENT.ENTITY_JOIN_LEVEL,
    "AddEntityClientEvent": CLIENT_EVENT.ENTITY_JOIN_LEVEL,
    "EntityRemoveEvent": SERVER_EVENT.ENTITY_LEAVE_LEVEL,
    "RemoveEntityClientEvent": CLIENT_EVENT.ENTITY_LEAVE_LEVEL,
    # 生物受伤事件
    "DamageEvent": SERVER_EVENT.LIVING_INCOMING_DAMAGE,
    "ActuallyHurtServerEvent": SERVER_EVENT.LIVING_DAMAGE_PRE,
    "ActorHurtServerEvent": SERVER_EVENT.LIVING_DAMAGE_POST,
    # 玩家尝试破坏方块事件
    "ServerPlayerTryDestroyBlockEvent": SERVER_EVENT.PLAYER_BLOCK_BREAK,
}

class EngineEventManager(EventManager):
    """ 引擎事件管理器 """
    def __init__(self):
        super().__init__()
        self._nativeEventInitSet = set()

    def regEventHandler(self, event, handler: EventHandler):
        return super().regEventHandler(self.formatEvent(event), handler)

    def unRegEventHandler(self, event, handler: EventHandler):
        return super().unRegEventHandler(self.formatEvent(event), handler)

    # def callEvent(self, event, *args):
    #     return super().callEvent(self.formatEvent(event), *args)

    def nativeEventUpdate(self, eventId=0):
        if eventId in self._nativeEventInitSet:
            return
        self._nativeEventInitSet.add(eventId)
        self._initNativeEventListener(eventId)
    
    def nativeListen(self, eventId: int, func: 'function', priority: int = 0):
        """ 注册原生事件监听器 """
        self.nativeEventUpdate(eventId)
        return self.regEventFuncHandler(eventId, func, priority)

    def _initNativeEventListener(self, eventId=-1):
        """ 初始化原生事件监听器 """
        pass

    def formatEvent(self, event):
        if not isinstance(event, tuple):
            return event
        if len(event) >= 3 and event[0] == "Minecraft" and event[1] == "Engine":
            eventName = event[2]
            if eventName in _MC_EVENT_MAPPING_TABLE:
                # 如果是Minecraft引擎事件，转换为对应的枚举值
                eventId = _MC_EVENT_MAPPING_TABLE[eventName]
                self.nativeEventUpdate(eventId)
                return eventId
            return event
        return event