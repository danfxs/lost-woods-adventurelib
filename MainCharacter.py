from adventurelib import *
import random

class MainCharacter(Item):
    
    def __init__(self, name):
        self.name = name
        self.inventory = Bag()
        self.attack = 4
        self.defense = 1
        self.destreza = 5
        self.atq_acumulado = 0
        self.health_points = 50
        self.weapon = Item("suas mãos")
    
    def attack_action(self) -> int:
        ataque = self.attack + random.randint(1, 4) + self.atq_acumulado
        self.atq_acumulado = 0
        print(f"{self.name} atacou o inimigo usando {self.weapon}. (-{ataque}HP)")
        return ataque
    
    def defend_action(self) -> int:
        self.atq_acumulado += random.randint(1, 5)
        defend_value = self.defense + random.randint(1, 3)
        print(f"{self.name} se defende de {defend_value} e se concentra ({self.atq_acumulado}) para o próximo ataque")
        return defend_value
    
    def getItem(self, Item) -> None:
        self.inventory.add(Item)
