from adventurelib import *

class Help:
    def __init__(self) -> None:
        pass

    def help(self, context) -> None:
        match context:
            case "floresta":
                say("Na floresta, você pode utilizar os comandos:")
                say("ir para DIRECAO")
                say("Onde DIRECAO pode ser norte/sul/leste/oeste")
            case "batalha":
                say("atacar - ataca o inimigo")
                say("defender - se defende contra o ataque inimigo acumulando forca para o próximo ataque")
                say("fugir - tenta fugir do inimigo")
        say("quit para sair do jogo")
