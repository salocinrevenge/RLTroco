from Agent import Agent
from Renderer import Renderer
import time
import random
class Environment:
    simbolosPadrao = {"agent": '@', "wall": '#', "path": '.', "goal":'$'}
    def __init__(self, path, stochastic, display=True) -> None:
        self.display = display
        self.mapaOriginal = self.carregarMapa(path)
        self.mapa = self.copiarMapa(self.mapaOriginal)
        self.tempoEspera = 0
        self.stochastic = stochastic

        if self.display:
            self.render = Renderer(self, self.mapa, "Ambiente")

    def copiarMapa(self, mapa):
        mapaCopia = []
        for linha in mapa:
            mapaCopia.append([])
            for celula in linha:
                mapaCopia[-1].append(celula)
        return mapaCopia

    def getAgent(self) -> Agent:
        return self.agent

    def in_terminal_state(self):
        return self.mapaOriginal[self.agent.y][self.agent.x] == self.simbolosPadrao["goal"]


    def carregarMapa(self, path):
        """
        Dado o caminho path, le um arquivo txt e retorna uma matriz
        O txt consiste de uma linha contendo o numero n (número de
        linhas do mapa) e m (número de caracteres diferentes no mapa),
        seguido de m linhas explicando o que sao os caracteres no 
        arquivo e por fim n linhas contendo o mapa que sao caracteres
        """
        mapa = []
        self.simbolos = dict()
        self.reforcos = {"agent": 0, "wall": 0, "path": 0, "goal":0}
        with open(path, 'r') as arquivo:
            m, n = map(int, arquivo.readline().split())
            for _ in range(m):
                linha = arquivo.readline().split()
                self.simbolos[linha[0]] = linha[1]
                self.reforcos[linha[1]] = int(linha[2])
            for i in range(n):
                linha = arquivo.readline()
                mapa.append([])
                for j in range(len(linha)):
                    char = linha[j]
                    if char == '\n':
                        continue
                    if self.simbolos[char] == 'agent':
                        self.agent = Agent(x=j, y=i, environment=self, display=self.display)
                        char = self.simbolosPadrao["path"]
                    mapa[-1].append(self.simbolosPadrao[self.simbolos[char]])
        return mapa
    
    def mover(self, agent, acao):
        """
        Dada uma acao, move o agente no mapa
        a acao pode ser "up", "down", "left" ou "right"
        """
        if random.random() < self.stochastic:
            acao = random.choice(agent.acoes)
        time.sleep(self.tempoEspera)
        direcao = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        posicaofinal = (agent.y+direcao[acao][0], agent.x+direcao[acao][1])
        if self.mapa[posicaofinal[0]][posicaofinal[1]] != self.simbolosPadrao["wall"]:
            # seta a posicao atual como caminho
            self.mapa[agent.y][agent.x] = self.mapaOriginal[agent.y][agent.x]
            
            # seta a posicao final como o agente
            self.mapa[posicaofinal[0]][posicaofinal[1]] = self.simbolosPadrao["agent"]
            
            # atualiza a posicao do agente
            agent.setPos(posicaofinal)
        # retorna o reforco da posicao final 
        return self.reforcos[self.simbolos[self.mapaOriginal[agent.y][agent.x]]]

    def util(self, pos, acao):
        """
        Dada uma posicao e uma acao, retorna o que tem na posicao destino
        """
        direcao = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        posicaofinal = (pos[0]+direcao[acao][0], pos[1]+direcao[acao][1])
        return self.simbolos[self.mapa[posicaofinal[0]][posicaofinal[1]]] != "wall"

    def get_size(self):
        return len(self.mapa), len(self.mapa[0])
    
    def setAgentPos(self, i, j):
        self.mapa[self.agent.y][self.agent.x] = self.mapaOriginal[self.agent.y][self.agent.x]
        self.agent.setPos((i, j))
        self.mapa[i][j] = self.simbolosPadrao["agent"]