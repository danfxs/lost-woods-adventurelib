from adventurelib import *
import adventurelib
from MainCharacter import MainCharacter
from Game import Game
from Help import Help
from Enemies import Enemy, Wolf, Goblin
import random
import copy

name_character = input('Qual o nome do seu personagem? ')
character = MainCharacter(name_character)

game = Game()

current_room = Room("")
latest_room = Room("")
floresta = Room("clareira no meio da floresta")
caverna = Room("entrada de uma caverna")
floresta_batalha = Room("O vento sopra através das arvores levando o rosnado raivoso do lobo a sua frente")

enemy = None
wolf = Wolf(6, 15)
goblin = Goblin(10, 25)

@when("quem sou")
def quem_sou():
    print(character)

@when("onde estou")
def onde_estou():
    global current_room
    print(current_room)

@when("ir para DIRECAO", context="floresta")
def irParaDirecao(direcao):
    global game, character, current_room, latest_room, caverna, floresta, floresta_batalha, latest_context, enemy, wolf
    if (get_context() == 'floresta'):
        game.lowerCountForest()
        if (game.checkForestSafe()):
            set_context('caverna')
            current_room = caverna
            say(f"{character.name} chegou na {current_room}")
        else:
            if random.randint(1, 10) > game.chance_find_battle:
                say('Após andar por alguns minutos, você encontra uma clareira muito parecida da qual você estava')
                game.chance_find_battle += 1
            else:
                game.chance_find_battle = game.standard_prob
                say('Você encontra um lobo raivoso, você deve derrotar o lobo antes de prosseguir')
                enemy = copy.copy(wolf)
                set_context('batalha')
                latest_room = floresta
                current_room = floresta_batalha

@when("atacar", context="batalha")
def atacar_batalha():
    global character, enemy, current_room, floresta, caverna, latest_room, latest_context
    vlr_ataque = character.attack_action()
    enemy.health_points -= vlr_ataque
    if (enemy.didItDie()):
        set_context(latest_context)
        current_room = latest_room
        say(f"Você derrotou {enemy.get_name()}. {character.name} voltou para {current_room}")
    else:
        vlr_ataque = enemy.attack_action()
        character.health_points -= vlr_ataque

@when("defender", context="batalha")
def defender_batalha():
    global character, enemy
    vlr_defesa = character.defend_action()
    vlr_ataque = enemy.attack_action()
    character.health_points = character.health_points - vlr_ataque + min(vlr_defesa, vlr_ataque)

print("""
Você acorda confuso no meio de uma clareira em uma floresta. 
Você tem a sua armadura de couro em seu corpo e uma espada danificada na sua mão. 
No fundo das grandes árvores no horizonte, é possível perceber alguns olhos aparecendo e desaparecendo. 
Sons de folhas sendo remexidas no chão são emitidas por todos os lados. 
Você precisa encontrar um caminho para fora da floresta e achar um local seguro.
Você pode ir para o norte, sul, leste ou oeste para procurar um local seguro. (ir para [escolha uma direcao como norte/sul/leste/oeste])
""")

set_context("floresta")
latest_context = get_context()
current_room = floresta

help = Help()

def no_command_matches(command):
    say(random.choice([
        'Não entendi.',
        'Você poderia repetir?',
        'Tente novamente, não compreendi o que você quis dizer'
    ]))
    help.help(get_context())

def prompt():
    if (get_context() == "batalha"):
        global character
        return '{hp}HP > '.format(hp = character.health_points)
    else:
        return '> '

adventurelib.no_command_matches = no_command_matches
adventurelib.prompt = prompt

start(help=False)
