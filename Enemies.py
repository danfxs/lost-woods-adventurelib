from abc import ABC, abstractmethod
import random

class Enemy(ABC):
    def __init__(self, attack, health_points):
        self._attack = attack
        self._health_points = health_points

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

    def didItDie(self) -> bool:
        return self.health_points <= 0


class Wolf(Enemy):    
    def get_name(self):
        return "o lobo"

    def attack_action(self):
        atk = random.randint(1, self.attack)
        print(f"O lobo ataca com suas garras afiadas. (-{atk}HP)")
        return atk

class Goblin(Enemy):
    def get_name(self):
        return "o goblin"

    def attack_action(self):
        atk = random.randint(1, self.attack)
        print(f"O goblin agita sua arma rude! (-{atk}HP)")
        return atk
