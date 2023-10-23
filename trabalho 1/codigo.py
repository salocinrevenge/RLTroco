import numpy as np
from itertools import product
import random
import numpy.random as npr

class Jogador():
    def __init__(self, x, y, labirinto, politica):
        self.x = x
        self.y = y
        self.labirinto = labirinto if labirinto else Labirinto(self)
        self.politica = politica
        self.pontos = 0
        self.acoes = list('UDLR')
        self.gamma = 0.9
        self.recompensas = {'.':-1, '$':100}
        self.probabilidades = [] # para cada estado par-acao, a probablidade de cair no estado s'
        
    def converterDirecao(self, direcao):
        match direcao:
            case "U":
                return (0, -1)
            case "D":
                return (0, 1)
            case "L":
                return (-1, 0)
            case "R":
                return (1, 0)

    def mover(self, direcao):
        direcao = self.converterDirecao(direcao)
        self.labirinto.mover(self, (self.x + direcao[0], self.y + direcao[1]))
        pos = self.labirinto.verChao(self.x, self.y)
        self.pontos += self.recompensas[pos]

    def decidir(self):
        movimento = random.choices(list("UDLR"), weights=self.politica[self.x, self.y, :])
        self.mover(movimento[0])


class Labirinto():
    def __init__(self, jogador = None, fator_estocastico=0):
        self.tabuleiroOriginal = np.asarray(list("##########"+
                                    "#$.......#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "##########")).reshape((10,10))
        self.tabuleiro = self.tabuleiroOriginal.copy()
        self.player = Jogador(self) if not jogador else jogador
        self.tabuleiro[self.player.x, self.player.y] = '@'
        self.fator_estocastico = fator_estocastico

    def ver(self, x, y):
        return self.tabuleiro[y, x]
    
    def verChao(self, x, y):
        return self.tabuleiroOriginal[y, x]

    def render(self):
        print(self.tabuleiro.transpose())

    def mover(self, jogador, pos):
        if self.ver(*pos) != '#':
            self.tabuleiro[jogador.x, jogador.y] = self.verChao(jogador.x, jogador.y)
            jogador.x, jogador.y = pos
            self.tabuleiro[pos] = "@"


class monteCarlo():
    def __init__(self,tabuleiro) -> None:
        self.contruirPoliticaInicial(tabuleiro)
        self.testarPolitica()

    def contruirPoliticaInicial(self,tabuleiro):
        self.politicaAtual = np.full((tabuleiro.shape[0], tabuleiro.shape[1], 4),dtype=float, fill_value=0.25)
        self.mostrarPolitica(self.politicaAtual)
    
    def mostrarPolitica(self,politica):
        for i in range(len(politica)):
            for j in range(len(politica[i])):
                for k, acao in enumerate("UDLR"):
                    print(acao if politica[i][j][k] else "", end="")
                print(" ", end="")
            print()

    def testarPolitica(self):
        print("Testando politica 0")
        numeroTestes = 10000
        pontuacaoAtual = 0
        for i in range(numeroTestes):
            casosTestes = 0
            pontuacao = 0
            for pos in product(range(1,9), range(1,9)):
                #print("Testando posicao inicial ",pos)
                pontuacao += self.testarPosicao(pos)
                casosTestes += 1
            pontuacaoAtual += pontuacao/casosTestes
        print("O valor dessa politica eh: ", pontuacaoAtual/numeroTestes)

    def testarPosicao(self, pos):
        self.player = Jogador(*pos,None,self.politicaAtual)
        contador = 0
        while self.player.labirinto.ver(*pos) != '$' and contador < 100:
            self.player.decidir()
            # self.player.labirinto.render()
            contador += 1
        return self.player.pontos





# def converter(direcao):
#     # converte de wasd para UDLR
#     match direcao:
#         case "w":
#             return "U"
#         case "a":
#             return "L"
#         case "s":
#             return "D"
#         case "d":
#             return "R"
#         case _:
#             return direcao
        

# jogador = Jogador(8,8,None,None)
# lab = jogador.labirinto
# while True:
#     lab.render()
#     direcao = input("Digite a direcao: ")
#     direcao = converter(direcao)
#     lab.player.mover(direcao)

mapa = np.asarray(list("##########"+
                                    "#$.......#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "##########")).reshape((10,10))
monteCarlo(mapa)