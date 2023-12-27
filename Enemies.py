from abc import ABC, abstractmethod
from math import ceil
import random

class Enemy(ABC):
    def __init__(self, attack, health_points, lang):
        self._attack = attack
        self._health_points = health_points
        self.lang = lang

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        if isinstance(value, (int, float)):
            self._attack = value
        else:
            raise ValueError("Attack must be a numeric value")

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        if isinstance(value, int):
            self._health_points = value
        else:
            raise ValueError("Health points must be an integer")
        
    @abstractmethod
    def attack_action(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def canRun(self):
        pass

    def didItDie(self) -> bool:
        return self.health_points <= 0


class Wolf(Enemy):    
    def get_name(self):
        return self.lang["wolf_description"]
    
    def canRun(self):
        return True

    def attack_action(self):
        atk = random.randint(1, self.attack)
        print(self.lang["work_attack"].format(atk))
        return atk

class Goblin(Enemy):
    def get_name(self):
        return self.lang["goblin_description"]
    
    def canRun(self):
        return True

    def attack_action(self):
        atk = random.randint(1, self.attack)
        print(self.lang["goblin_attack"].format(atk))
        return atk

class Ogre(Enemy):
    def get_name(self):
        return self.lang["ogre_description"]
    
    def canRun(self):
        return False
    
    def attack_action(self):
        atk = random.randint(1, self.attack) + ceil(random.randint(1, self.attack)/2)
        print(self.lang["ogre_attack"].format(atk))
        return atk