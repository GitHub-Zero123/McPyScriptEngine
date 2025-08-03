from mod.qumod3.api import SubscribeEvent
from mod.qumod3.event.block import ServerPlayerTryDestroyBlockEvent
from mod.qumod3.block import BlockState, PlaceOptions
from collections import deque

@SubscribeEvent
def onServerPlayerTryDestroyBlock(event: ServerPlayerTryDestroyBlockEvent):
    player = event.getPlayer()
    item = player.getMainHandItem()
    if not "pickaxe" in item.itemName:
        return
    dmId = event.getDimensionId()
    maxItCount = 1000
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

    airBlock = BlockState.createAirBlock()
    placeOpt = PlaceOptions(1, False)
    for pos in targetPos:
        airBlock.placeServer(pos, dmId, placeOpt)
