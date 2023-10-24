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
                                    "#.$......#"+
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
        self.atualizarPolitica(100)

    def contruirPoliticaInicial(self,tabuleiro):
        self.politicaAtual = np.full((tabuleiro.shape[0], tabuleiro.shape[1], 4),dtype=float, fill_value=0.25)
    
    def mostrarPolitica(self,politica, probabilidade=True):
        if probabilidade:
            for i in range(len(politica)):
                for j in range(len(politica[i])):
                    for k, acao in enumerate("UDLR"):
                        print(f"{acao}({politica[i][j][k]})" if politica[i][j][k] else "", end="")
                    print(" ", end="")
                print()
        else:
            for i in range(len(politica)):
                for j in range(len(politica[i])):
                    possibilidades = []
                    for k, acao in enumerate("UDLR"):
                        possibilidades.append((acao,politica[i][j][k]))
                    possibilidades.sort(key=lambda x: x[1], reverse=True)
                    print(possibilidades[0][0], end=" ")
                print()

    def atualizarPolitica(self, numeroMelhorias):
        for i in range(numeroMelhorias):
            print("Melhoria ", i, " :")
            self.mostrarPolitica(self.politicaAtual,False)
            for pos in product(range(1,9), range(1,9)):
                self.testarPosicao(pos,numeroMelhorias*10)

    def testarPosicao(self, pos, numeroMelhorias):
        # executa cada acao disponivel com a quantidade sendo numeroMelhorias*probabilidadeDaAcao
        # marca o tempo de cada execucao e a media dos acertos
        # apos executar td, atualiza a politica aumentando a probabilidade das acoes que tiveram mais acertos
        # e diminuindo a probabilidade das acoes que tiveram menos acertos levando em conta a quantidade de acertos
        # print("Testando posicao ", pos, " numeroMelhorias: ", numeroMelhorias)
        acoesdisponiveis = {"U":self.politicaAtual[pos[0]][pos[1]][0], "D":self.politicaAtual[pos[0]][pos[1]][1], "L":self.politicaAtual[pos[0]][pos[1]][2], "R":self.politicaAtual[pos[0]][pos[1]][3]}
        resultados = {"U":[0,0], "D":[0,0], "L":[0,0], "R":[0,0]}
        for acao in acoesdisponiveis:
            if acoesdisponiveis[acao] ==0:
                continue
            for i in range(numeroMelhorias):
                resultado = self.testarAcao(pos,acao)   # executa a acao ate o final e retorna a pontuacao do personagem
                resultados[acao][0] += resultado
                resultados[acao][1] += 1
        soma = 0
        # print(f"resultados: {resultados}")
        for acao in resultados:
            if resultados[acao][1] == 0: # se uma acao tiver probabilidade 0
                continue
            soma += resultados[acao][0]/resultados[acao][1]
        # print(f"resultados: {resultados} soma: {soma}")
        for i, acao in enumerate(resultados):
            if soma == 0:
                porcAtual = 0
            else:
                porcAtual = ((resultados[acao][0]/resultados[acao][1])/soma)
            self.politicaAtual[pos][i] = (self.politicaAtual[pos][i]+porcAtual)/2

    def testarAcao(self, pos, acao):
        jogador = Jogador(*pos,None,self.politicaAtual)
        jogador.mover(acao)
        contador = 0
        #jogador.labirinto.render()
        while jogador.labirinto.ver(*pos) != '$' and contador < 100:
            jogador.decidir()
            #jogador.labirinto.render()
            contador += 1
        return jogador.pontos




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
                                    "#.$......#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "#........#"+
                                    "##########")).reshape((10,10))
monteCarlo(mapa)