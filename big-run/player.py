from items import SquareContent

class Player(object):
    def __init__(self, id, name, lives):
        self.name = name
        self.id = id 
        self.lives = lives
        self.inventory = {}
        self.position = 0

        self.inventory_to_live_formula = {SquareContent.WATER: 1, SquareContent.FOOD: 1}

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)

    def StatusReport(self):
        return '{} is in position {} and has {} lives.'.format(self.name,
                                                               self.position,
                                                               self.lives)
    def IsAlive(self):
        return self.lives > 0

    def AddInventory(self, content, n = 1):
        # Take one SquareContent and put in the inventory
        if content not in self.inventory:
            self.inventory[content] = 0
        self.inventory[content] += n

        while self._inventoryCanConvertOneLive():
            self._convertOneLive()

    def _inventoryCanConvertOneLive(self):
        for ingredient, count in self.inventory_to_live_formula.items():
            if ingredient not in self.inventory:
                return False
            if self.inventory[ingredient] < count:
                return False

        return True

    def _convertOneLive(self):
        for ingredient, count in self.inventory_to_live_formula.items():
            self.inventory[ingredient] -= count

        self.lives += 1

    def LostLife(self, n = 1):
        self.lives -= n

    def TakeEffect(self, content):
        if content == SquareContent.NOTHING:
            return
        elif content == SquareContent.X:
            self.LostLife()
        elif content == SquareContent.WATER or content == SquareContent.FOOD:
            self.AddInventory(content)

    def Dump(self):
        return 'ID: {}; Name: {};\n.........Position: {}; Lives: {}; Inventory: {}'.format(
                self.id, self.name, self.position, self.lives, self.inventory)
