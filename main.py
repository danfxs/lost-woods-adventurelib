from adventurelib import *
import sys
sys.path.append('./character')
from MainCharacter import MainCharacter

name_character = input('Qual o nome do seu personagem? ')
character = MainCharacter(name_character)

@when("quem sou")
def quemSou():
    print(character)



start()
