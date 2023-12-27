from adventurelib import *
import random

class MainCharacter(Item):
    
    def __init__(self, name, lang):
        self.name = name
        self.inventory = Bag()
        self.attack = 4
        self.defense = 1
        self.dexterity = 5
        self.atk_focus = 0
        self.health_points = 50
        self.lang = lang
        self.weapon = Item(self.lang["character_initial_weapon"])
        self.weapon_atk = 4        
    
    def attack_action(self) -> int:
        attack = self.attack + random.randint(1, self.weapon_atk) + self.atk_focus
        self.atk_focus = 0
        print(self.lang["character_action_attack"].format(self.name, self.weapon, attack))
        return attack
    
    def defend_action(self) -> int:
        self.atk_focus += random.randint(1, 5)
        defend_value = self.defense + random.randint(1, 3)
        print(self.lang["character_defend_attack"].format(self.name, defend_value, self.atk_focus))
        return defend_value
    
    def getItem(self, Item) -> None:
        self.inventory.add(Item)

    def equip(self, item, weapon_atk) -> None:
        weapon = self.inventory.find(item)
        if weapon:
            self.weapon = weapon
            self.weapon_atk = weapon_atk
