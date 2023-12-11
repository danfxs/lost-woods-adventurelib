from adventurelib import *
import random

class MainCharacter(Item):
    def __init__(self, name):
        self.name = name
        self.inventory = Bag()
        self.attack = 10
        self.defense = 10
    def attack(self):
        return self.attack + random.randint(1, 6)
    def defense(self):
        return self.defense + random.randint(1, 4)
    def getItem(self, Item):
        self.inventory.add(Item)
