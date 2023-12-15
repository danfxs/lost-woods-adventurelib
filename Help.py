from adventurelib import *

class Help:
    def __init__(self) -> None:
        pass

    def help(self, context) -> None:
        match context:
            case "floresta":
                say("Na floresta, você pode utilizar os comandos:")
                say("ir para DIRECAO -> DIRECAO pode ser norte/sul/leste/oeste")
            case "batalha":
                say("atacar   - ataca o inimigo")
                say("defender - se defende contra o ataque inimigo acumulando forca para o próximo ataque")
                say("fugir    - tenta fugir do inimigo")
            case "caverna.entrada":
                say("esquerda - escolha a passagem da esquerda")
                say("direita - escolha a passagem da direita")
            case "caverna.deposito":
                say("continuar - segue adiante para a próxima parte da caverna")
                say("procurar - procura nas caixas por mantimentos")
            case "caverna.final":
                say("")
        say("ajuda - mostra as opções do seu local atual")
        say("sair - sair do jogo")
