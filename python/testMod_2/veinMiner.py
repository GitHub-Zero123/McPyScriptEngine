from mod.qumod3.api import SubscribeEvent
from mod.qumod3.event.block import ServerPlayerTryDestroyBlockEvent
from mod.qumod3.block import BlockState, PlaceOptions
from collections import deque

class Static:
    veinMiningPlayers = set()

@SubscribeEvent
def onServerPlayerTryDestroyBlock(event: ServerPlayerTryDestroyBlockEvent):
    player = event.getPlayer()
    if player in Static.veinMiningPlayers:
        # 避免循环调用
        return
    item = player.getMainHandItem()
    if not "pickaxe" in item.itemName:
        return
    dmId = event.getDimensionId()
    maxItCount = 500
    # 搞子类物品 触发连锁挖掘
    startPos = event.getPos()
    originBlockState = event.getBlockState()

    visited = set()
    queue = deque()
    targetPos = set()

    # 六个方向的偏移量
    directions = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]

    visited.add(startPos)
    queue.append(startPos)
    targetPos.add(startPos)

    while queue and len(targetPos) < maxItCount:
        current = queue.popleft()
        for dx, dy, dz in directions:
            neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)
            if neighbor in visited:
                continue
            visited.add(neighbor)
            neighborState = BlockState.getBlockState(neighbor, dmId)
            if neighborState == originBlockState:
                targetPos.add(neighbor)
                queue.append(neighbor)
    targetPos.discard(startPos)
    Static.veinMiningPlayers.add(player)
    for pos in targetPos:
        # 模拟玩家破坏方块(消耗武器耐久)
        player.action.destroyBlock(pos)
    Static.veinMiningPlayers.discard(player)

    # airBlock = BlockState.createAirBlock()
    # placeOpt = PlaceOptions(1, False)
    # for pos in targetPos:
    #     airBlock.placeServer(pos, dmId, placeOpt)