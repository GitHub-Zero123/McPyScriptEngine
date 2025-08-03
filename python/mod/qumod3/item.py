
class Item:
    def __init__(self, itemName=""):
        self.itemName = itemName
        self.aux = 0

    def empty(self) -> bool:
        """
        检查物品是否为空
        :return: 如果物品为空则返回True，否则返回False
        """
        return not self.itemName
    
    def __str__(self):
        return f"Item(name={self.itemName}, pyObjectId={id(self)})"

    def __eq__(self, value):
        if isinstance(value, Item):
            return self.itemName == value.itemName and self.aux == value.aux
        elif isinstance(value, str):
            return self.itemName == value
        return False