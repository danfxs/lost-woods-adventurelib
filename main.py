from adventurelib import *
import adventurelib
import random
import copy
import time
from MainCharacter import MainCharacter
from Game import Game
from Help import Help
from Enemies import Enemy, Wolf, Goblin, Ogre
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
character = MainCharacter(name_character, lang)

game = Game()

current_room = Room("")
latest_room = Room("")
forest = Room(lang["forest_room"])
cavern = Room(lang["cavern_room"])
cavern_warehouse = Room(lang["cavern_warehouse_room"])
cavern_final = Room(lang["cavern_final_room"])

enemy = None
wolf = Wolf(4, 5, lang)
goblin = Goblin(6, 5, lang)
ogre = Ogre(8, 5, lang)

@when(lang["action_who_am_i"])
def who_am_i():
    print(character)

@when(lang["action_where_i_am"])
def where_i_am():
    global current_room
    print(current_room)

@when(lang["action_goto_direction"], context="forest")
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

@when(lang["action_battle_attack"], context="battle")
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

@when(lang["action_battle_defend"], context="battle")
def defend_battle():
    global character, enemy
    vl_defesa = character.defend_action()
    vl_ataque = enemy.attack_action()
    character.health_points = character.health_points - vl_ataque + min(vl_defesa, vl_ataque)

@when(lang["action_battle_escape"], context="battle")
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

@when(lang["action_cavern_left"], context="cavern.entrance")
def cavern_left():
    global character, latest_context, goblin, enemy, latest_room, cavern_warehouse
    say(lang["cavern_entrance_1"])
    say(lang["cavern_entrance_2"].format(character.name))
    say(lang["cavern_entrance_3"].format(character.name))
    latest_context = "cavern.warehouse"
    latest_room = cavern_warehouse
    enemy = copy.copy(goblin)
    set_context("battle")

@when(lang["action_cavern_left"], context="cavern.entrance")
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

@when(lang["action_cavern_search"], context="cavern.warehouse")
def search():
    global character, current_room, cavern_final
    recovered_hp = random.randint(1, 4) + random.randint(1, 4)
    character.health_points += recovered_hp
    say(lang["cavern_warehouse_1"])
    say(lang["cavern_warehouse_2"].format(character.name, recovered_hp))
    say(lang["cavern_warehouse_3"].format(character.name))
    set_context("cavern.final")
    current_room = cavern_final
    show_where_character()

@when(lang["action_cavern_continue"], context="cavern.warehouse")
def continue_cavern():
    global character, current_room, cavern_final
    say(lang["cavern_warehouse_4"].format(character.name))
    current_room = cavern_final
    set_context("cavern.final")
    show_where_character()

def show_where_character():
    global character, current_room
    say(lang["show_where_character"].format(character.name, current_room))

@when("ANYTHING", context="cavern.final")
def cavern_final_action(anything):
    global character, game, enemy, ogre, latest_context, latest_room, cavern_final, current_room
    if (not game.checkIfFinalBossDefeated()):
        say(lang["cavern_final"].format(character.name))
        game.enterBattleFinalBoss()
        enemy = copy.copy(ogre)
        set_context("battle")
        latest_context = "cavern.decision"
        latest_room = cavern_final
        current_room = cavern_final
    else:
        show_final_decision()

def show_final_decision():
    global character
    say(lang["final_decision_1"].format(character.name))
    time.sleep(2)
    say(lang["final_decision_2"].format(character.name))

@when(lang["action_enter_portal"], context="cavern.decision")
def enter_portal():
    global character
    say(lang["enter_portal_1"].format(character.name))
    time.sleep(3)
    say(lang["enter_portal_2"])
    time.sleep(3)
    say(lang["enter_portal_3"])
    time.sleep(3)
    say(lang["enter_portal_4"].format(character.name))
    time.sleep(4)
    say(lang["enter_portal_5"].format(character.name))
    time.sleep(3)
    say(lang["enter_portal_6"].format(character.name))
    exit_action()

@when(lang["action_break_portal"], context="caverna.decisao")
def quebrar_portal():
    global character
    say(lang["break_portal_1"].format(character.weapon, character.name))
    time.sleep(2)
    say(lang["break_portal_2"])
    time.sleep(2)
    say(lang["break_portal_3"].format(character.name))
    time.sleep(2)
    say(lang["break_portal_4"])
    time.sleep(2)
    say(lang["break_portal_5"].format(character.name))
    exit_action()


print(lang["begin_game"])

set_context("forest")
latest_context = get_context()
current_room = forest

help = Help(lang)

@when(lang["action_help"])
def help_action():
    help.help(get_context)

@when(lang["action_exit"])
def exit_action():
    quit()

def no_command_matches(command):
    say(random.choice([
        lang["cant_understand_1"],
        lang["cant_understand_2"],
        lang["cant_understand_3"]
    ]))
    help.help(get_context())

def prompt():
    if (get_context() == "battle"):
        global character
        return '{hp}HP > '.format(hp = character.health_points)
    else:
        return '> '

adventurelib.no_command_matches = no_command_matches
adventurelib.prompt = prompt

start(help=False)
