from adventurelib import *
import adventurelib
import random
import copy
import time
from MainCharacter import MainCharacter
from Game import Game
from Help import Help
from Enemies import Enemy, Wolf, Goblin, Ogro
from languages.lang_eng import lang_eng
from languages.lang_ptbr import lang_ptbr

lang = None
lang_opt = 0
while lang_opt not in [1, 2]:
    try:
        lang_opt = int(input('[1] English\n[2] Português (Brasil)\n > '))
        if lang_opt not in [1, 2]:
            print("Invalid option. Choose 1 or 2.\nOpção inválida. Escolha 1 ou 2.")
    except ValueError:
        print("Invalid option. Choose 1 or 2.\nOpção inválida. Escolha 1 ou 2.")

if lang_opt == 1:    
    lang = lang_eng
else:    
    lang = lang_ptbr

name_character = input(lang["character_name"])
character = MainCharacter(name_character)

game = Game()

current_room = Room("")
latest_room = Room("")
forest = Room(lang["forest_room"])
cavern = Room(lang["cavern_room"])
cavern_warehouse = Room(lang["cavern_warehouse_room"])
cavern_final = Room(lang["cavern_final_room"])

enemy = None
wolf = Wolf(4, 5)
goblin = Goblin(6, 5)
ogro = Ogro(8, 5)

@when("quem sou")
@when("who am i")
def quem_sou():
    print(character)

@when("onde estou")
@when("where i am")
def onde_estou():
    global current_room
    print(current_room)

@when("ir para DIRECTION", context="forest")
@when("go to DIRECTION", context="forest")
def goToDirection(direction):
    global game, character, current_room, latest_room, cavern, forest, latest_context, enemy, wolf
    if (get_context() == 'forest'):
        game.lowerCountForest()
        if (game.checkForestSafe()):
            set_context('cavern.entrance')
            current_room = cavern
            say(lang["arrive_cavern_1"].format(character.name, current_room))
            say(lang["arrive_cavern_2"].format(character.name))
            say(lang["arrive_cavern_3"])
            say(lang["arrive_cavern_4"])
        else:
            if random.randint(1, 10) > game.chance_find_battle:
                say(lang["forest_going_circle"])
                game.chance_find_battle += 1
            else:
                game.chance_find_battle = game.standard_prob
                say(lang["find_forest_battle"])
                enemy = copy.copy(wolf)
                set_context('battle')
                latest_room = forest

def check_win():
    global character
    time.sleep(2)
    if (get_context() == "cavern.warehouse"):
        say(lang["get_weapon_crude_sword"].format(character.name))
        crude_sword_description = lang["crude_sword_description"]
        crude_sword = Item(crude_sword_description)
        character.getItem(crude_sword)
        character.equip(crude_sword_description, 8)
        time.sleep(2)
    elif (get_context() == "cavern.decision"):
        say(lang["after_beat_ogre_1"].format(character.name))
        time.sleep(2)
        say(lang["after_beat_ogre_2"].format(character.name))

@when("atacar", context="battle")
@when("attack", context="battle")
def attack_battle():
    global character, enemy, current_room, forest, cavern, latest_room, latest_context
    vl_attack = character.attack_action()
    enemy.health_points -= vl_attack
    if (enemy.didItDie()):
        set_context(latest_context)
        current_room = latest_room
        say(lang["finish_battle"].format(enemy.get_name(), character.name, current_room))
        check_win()
    else:
        vl_attack = enemy.attack_action()
        character.health_points -= vl_attack

@when("defender", context="battle")
@when("defend", context="battle")
def defend_battle():
    global character, enemy
    vl_defesa = character.defend_action()
    vl_ataque = enemy.attack_action()
    character.health_points = character.health_points - vl_ataque + min(vl_defesa, vl_ataque)

@when("fugir", context="battle")
@when("escape", context="battle")
def escape_battle():
    global character, enemy, latest_context, current_room, latest_room
    if enemy.canRun():
        prob = character.health_points + character.destreza
        say(lang["escape_action"].format(character.name, prob))
        if (random.randint(1, 100) < prob):
            say(lang["escape_success"].format(character.name))
            set_context(latest_context)
            current_room = latest_room
        else:
            say(lang["escape_fail"].format(character.name))
            character.health_points = character.health_points - enemy.attack_action()
    else:
        say(lang["escape_impossible"].format(character.name))

@when("esquerda", context="cavern.entrance")
@when("left", context="cavern.entrance")
def cavern_left():
    global character, latest_context, goblin, enemy, latest_room, cavern_warehouse
    say(lang["cavern_entrance_1"])
    say(lang["cavern_entrance_2"].format(character.name))
    say(lang["cavern_entrance_3"].format(character.name))
    latest_context = "cavern.warehouse"
    latest_room = cavern_warehouse
    enemy = copy.copy(goblin)
    set_context("battle")

@when("direita", context="cavern.entrance")
@when("right", context="cavern.entrance")
def cavern_right():
    global character, current_room, cavern_final
    say(lang["cavern_right"].format(character.name))
    prob = character.health_points + character.destreza
    if random.randint(1, 100) < prob:
        say(lang["cavern_trap_success_1"].format(character.name))
        say(lang["cavern_trap_success_2"].format(character.name))
    else:
        dmg = random.randint(1, 6) + random.randint(1, 6)
        character.health_points -= dmg
        say(lang["cavern_trap_fail_1"].format(character.name))
        say(lang["cavern_trap_fail_2"].format(character.name, dmg))
    set_context("cavern.final")
    current_room = cavern_final

@when("procurar", context="cavern.warehouse")
@when("seach", context="cavern.warehouse")
def search():
    global character, current_room, cavern_final
    recovered_hp = random.randint(1, 4) + random.randint(1, 4)
    character.health_points += recovered_hp
    say(f"Diversas caixas estão espalhadas e abrindo, uma a uma, foi possível encontrar um vidro com um líquido vermelho")
    say(f"{character.name} bebe todo o líquido vermelho recuperando {recovered_hp}HP")
    say(f"Como não há mais nada de útil nas caixas, {character.name} segue adiante")
    set_context("caverna.final")
    current_room = caverna_final
    exibir_personagem_esta()

@when("continuar", context="caverna.deposito")
def continuar():
    global character, current_room, caverna_final
    say(f"Com bastante moral, {character.name} segue adiante no caminho")
    current_room = caverna_final
    set_context("caverna.final")
    exibir_personagem_esta()

def exibir_personagem_esta():
    global character, current_room
    say(f"{character.name} está {current_room}")

@when("QUALQUERCOISA", context="caverna.final")
def caverna_final_action(qualquercoisa):
    global character, game, enemy, ogro, latest_context, latest_room, caverna_final, current_room
    if (not game.checkIfFinalBossDefeated()):
        say(f"Através do portal, trepidações no chão são sentidas pelos pés de {character.name}, até seus olhos perceberem um ogro gigante vindo em sua direção")
        game.enterBattleFinalBoss()
        enemy = copy.copy(ogro)
        set_context("batalha")
        latest_context = "caverna.decisao"
        latest_room = caverna_final
        current_room = caverna_final
    else:
        exibir_final()

def exibir_final():
    global character
    say(f"Após derrotar o ogro, {character.name} anda até a outra extremidade da sala analisando os pilares")
    time.sleep(2)
    say(f"Após investigar o portal e o brilho vermelho, {character.name} se pergunta se deveria [entrar no portal] ou [quebrar o portal].")

@when("entrar no portal", context="caverna.decisao")
def entrar_portal():
    global character
    say(f"{character.name} enche os pulmões de ar como se aquela ação aumentasse sua coragem e coloca o seu braço através do portal")
    time.sleep(3)
    say(f"Ficando com mais ânimo, resolve andar através do portal")
    time.sleep(3)
    say(f"Tudo fica claro, impossível de distinguir quaisquer coisas que estariam ao seu redor")
    time.sleep(3)
    say(f"Ao tempo que sua visão fica melhor, {character.name} percebe que está sentado na frente de uma máquina eletrônica escrevendo ações e esperando resultados")
    time.sleep(4)
    say(f"{character.name} se sentindo a tranquilidade do local, sua memória volta e se lembra que está em casa")
    time.sleep(3)
    say(f"Com um sorriso de ponta a ponta, {character.name} segue em direção ao seu quarto para encontrar sua cama e dormir para recuperar as forças para uma próxima aventura")
    sair()

@when("quebrar portal", context="caverna.decisao")
def quebrar_portal():
    global character
    say(f"Com {character.weapon}, {character.name} começa a danificar o portal")
    time.sleep(2)
    say(f"O brilho do portal diminui lentamente até escurecer totalmente")
    time.sleep(2)
    say(f"{character.name} vê o formato do portal desmoronando aos seus pés")
    time.sleep(2)
    say(f"Um rugido estremece a escuridão quando a destruição do portal se completa")
    time.sleep(2)
    say(f"{character.name} dá meia volta em direção da entrada da caverna, respira fundo e espera sobreviver nesse novo lugar desconhecido")
    sair()


print(lang["begin_game"])

set_context("floresta")
latest_context = get_context()
current_room = floresta

help = Help()

@when("ajuda")
def ajuda():
    help.help(get_context)

@when("sair")
def sair():
    quit()

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
