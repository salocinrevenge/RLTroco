from Agent import Agent
from Renderer import Renderer
import time
import random
class Environment:
    default_symbols = {"agent": '@', "wall": '#', "path": '.', "goal":'$'}
    def __init__(self, path, stochastic, display=True) -> None:
        self.display = display
        self.original_map = self.load_map(path)
        self.map = self.copy_map(self.original_map)
        self.wait_time = 0
        self.stochastic = stochastic

        if self.display:
            self.render = Renderer(self, self.map, "Ambiente")

    def copy_map(self, mapa):
        mapaCopia = []
        for linha in mapa:
            mapaCopia.append([])
            for celula in linha:
                mapaCopia[-1].append(celula)
        return mapaCopia

    def getAgent(self) -> Agent:
        return self.agent

    def in_terminal_state(self):
        return self.original_map[self.agent.y][self.agent.x] == self.default_symbols["goal"]

    def load_map(self, path):
        """
        Dado o caminho path, le um arquivo txt e retorna uma matriz
        O txt consiste de uma linha contendo o numero n (número de
        linhas do mapa) e m (número de caracteres diferentes no mapa),
        seguido de m linhas explicando o que sao os caracteres no 
        arquivo e por fim n linhas contendo o mapa que sao caracteres
        """
        grid = []
        self.symbols = dict()
        self.rewards = {"agent": 0, "wall": 0, "path": 0, "goal":0}
        with open(path, 'r') as file:
            m, n = map(int, file.readline().split())
            for _ in range(m):
                line = file.readline().split()
                self.symbols[line[0]] = line[1]
                self.rewards[line[1]] = int(line[2])
            for i in range(n):
                line = file.readline()
                grid.append([])
                for j in range(len(line)):
                    char = line[j]
                    if char == '\n':
                        continue
                    if self.symbols[char] == 'agent':
                        self.agent = Agent(x=j, y=i, environment=self, display=self.display)
                        char = self.default_symbols["path"]
                    grid[-1].append(self.default_symbols[self.symbols[char]])
        return grid
    
    def move(self, agent, acao):
        """
        Dada uma acao, move o agente no mapa
        a acao pode ser "up", "down", "left" ou "right"
        """
        if random.random() < self.stochastic:
            acao = random.choice(agent.actions)
        time.sleep(self.wait_time)
        direction = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        posicaofinal = (agent.y+direction[acao][0], agent.x+direction[acao][1])
        if self.map[posicaofinal[0]][posicaofinal[1]] != self.default_symbols["wall"]:
            # seta a posicao atual como caminho
            self.map[agent.y][agent.x] = self.original_map[agent.y][agent.x]
            
            # seta a posicao final como o agente
            self.map[posicaofinal[0]][posicaofinal[1]] = self.default_symbols["agent"]
            
            # atualiza a posicao do agente
            agent.setPos(posicaofinal)
        # retorna o reforco da posicao final 
        return self.rewards[self.symbols[self.original_map[agent.y][agent.x]]]

    def util(self, pos, acao):
        """
        Dada uma posicao e uma acao, retorna o que tem na posicao destino
        """
        direcao = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        posicaofinal = (pos[0]+direcao[acao][0], pos[1]+direcao[acao][1])
        return self.symbols[self.map[posicaofinal[0]][posicaofinal[1]]] != "wall"

    def get_size(self):
        return len(self.map), len(self.map[0])
    
    def setAgentPos(self, i, j):
        self.map[self.agent.y][self.agent.x] = self.original_map[self.agent.y][self.agent.x]
        self.agent.setPos((i, j))
        self.map[i][j] = self.default_symbols["agent"]
        return self.rewards[self.symbols[self.original_map[self.agent.y][self.agent.x]]]