from adventurelib import *
import adventurelib
from MainCharacter import MainCharacter
from Game import Game
from Help import Help
from Enemies import Enemy, Wolf, Goblin, Ogro
import random
import copy
import time

name_character = input('Qual o nome do seu personagem? ')
character = MainCharacter(name_character)

game = Game()

current_room = Room("")
latest_room = Room("")
floresta = Room("uma clareira no meio da floresta")
caverna = Room("uma entrada de uma caverna")
caverna_deposito = Room("uma parte da caverna que contem diversas caixas, algumas mesas e cadeiras")
caverna_final = Room("uma grande sala com dois pilares simétricos até a parte superior da caverna. Também é possível enxergar um portal na outra extremidade da sala emitindo um brilho vermelho no seu interior")
floresta_batalha = Room("O vento sopra através das arvores levando o rosnado raivoso do lobo a sua frente")

enemy = None
wolf = Wolf(4, 5)
goblin = Goblin(6, 5)
ogro = Ogro(8, 5)

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
            set_context('caverna.entrada')
            current_room = caverna
            say(f"{character.name} chegou na {current_room}")
            say(f"Forçando a vista na escuridão da caverna, {character.name} consegue ver uma passagem para esquerda e para direita")
            say("Enquanto que na esquerda é possível ver mais luzes ao fundo de um caminho tortuoso, pela direita parece ser um caminho mais reto com poucas tochas caídas no chão ao longo do caminho")
            say("Escolher se quer ir para a [esquerda] ou [direita]")
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

def check_win():
    global character
    time.sleep(2)
    if (get_context() == "caverna.deposito"):
        say(f"{character.name} pega a espada do goblin com muita apreciação")
        crude_sword_description = "uma espada rústica"
        crude_sword = Item(crude_sword_description)
        character.getItem(crude_sword)
        character.equip(crude_sword_description, 8)
        time.sleep(2)
    elif (get_context() == "caverna.decisao"):
        say(f"Após derrotar o ogro, {character.name} anda até a outra extremidade da sala analisando os pilares")
        time.sleep(2)
        say(f"Após investigar o portal e o brilho vermelho, {character.name} se pergunta se deveria [entrar no portal] ou [quebrar o portal].")

@when("atacar", context="batalha")
def atacar_batalha():
    global character, enemy, current_room, floresta, caverna, latest_room, latest_context
    vlr_ataque = character.attack_action()
    enemy.health_points -= vlr_ataque
    if (enemy.didItDie()):
        set_context(latest_context)
        current_room = latest_room
        say(f"Você derrotou {enemy.get_name()}. {character.name} voltou para {current_room}")
        check_win()
    else:
        vlr_ataque = enemy.attack_action()
        character.health_points -= vlr_ataque

@when("defender", context="batalha")
def defender_batalha():
    global character, enemy
    vlr_defesa = character.defend_action()
    vlr_ataque = enemy.attack_action()
    character.health_points = character.health_points - vlr_ataque + min(vlr_defesa, vlr_ataque)

@when("fugir", context="batalha")
def fugir_batalha():
    global character, enemy, latest_context, current_room, latest_room
    if enemy.canRun():
        prob = character.health_points + character.destreza
        say(f"{character.name} tem {prob}% de chance de fugir")
        if (random.randint(1, 100) < prob):
            say(f"{character.name} conseguiu escapar")
            set_context(latest_context)
            current_room = latest_room
        else:
            say(f"{character.name} não conseguiu fugir")
            character.health_points = character.health_points - enemy.attack_action()
    else:
        say(f"{character.name} percebe é que impossível fugir desse inimigo")

@when("esquerda", context="caverna.entrada")
def caverna_esquerda():
    global character, latest_context, goblin, enemy, latest_room, caverna_deposito
    say("Ao andar com cuidado no piso de pedra da caverna, é possível perceber uma criatura verde sentada em uma cadeira comendo algumas carnes")
    say(f"A criatura se vira para pegar mais comidas em uma das caixas e vê {character.name} tentando permanecer nas sombras")
    say(f"A criatura pega sua espada e corre com hostilidade em direção a {character.name}")
    latest_context = "caverna.deposito"
    latest_room = caverna_deposito
    enemy = copy.copy(goblin)
    set_context("batalha")

@when("direita", context="caverna.entrada")
def caverna_direta():
    global character, current_room, caverna_final
    say(f"Percebendo as tochas solitárias, {character.name} anda devagar olhando para todas as direções")
    prob = character.health_points + character.destreza
    if random.randint(1, 100) < prob:
        say(f"Antes de pudesse dar um passo, {character.name} percebe uma linha estentida entre as paredes como armadilha")
        say(f"{character.name} pula com cuidado, seguindo seu caminho")
    else:
        dmg = random.randint(1, 6) + random.randint(1, 6)
        character.health_points -= dmg
        say(f"Mesmo tentando perceber tudo ao seu redor, uma linha entre as paredes da caverna aparece na frente de uma das pernas de {character.name}")
        say(f"Dardos saem de pequenos buracos acertando {character.name} e causando -{dmg}HP")
    set_context("caverna.final")
    current_room = caverna_final

@when("procurar", context="caverna.deposito")
def procurar():
    global character, current_room, caverna_final
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
