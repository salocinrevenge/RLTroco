import random
from Renderer import Renderer
class Agent():
    acoes = ['up', 'down', 'left', 'right']
    def __init__(self, x=None, y = None, environment= None, gamma = 0.99) -> None:
        if environment:
            self.environment = environment

        if x:
            self.x = x
        if y:
            self.y = y
        self.gamma = gamma

    def iniciaQ(self, formato):
        """
        livroQ é uma lista de listas de dicionarios,
        ele armazena 
        
        """
        self.livro_Q = []
        for i in range(formato[0]):
            self.livro_Q.append([])
            for _ in range(formato[1]):
                self.livro_Q[i].append(dict())
                for acao in self.acoes:
                    self.livro_Q[i][-1][acao] = float("-inf")
    
    def iniciaPolicy(self, formato, politicaAleatoria):
        """
        A policy é uma matriz de caracteres que guarda a acao principal
        a ser tomada ate o momento
        
        """
        self.policy = []
        for i in range(formato[0]):
            self.policy.append([])
            for _ in range(formato[1]):
                if politicaAleatoria:
                    self.policy[i].append(random.choice(self.acoes))
                else:
                    self.policy[i].append(self.acoes[0])
        self.render = self.environment.render.addConteudo(self.policy)

    def iniciaRetorno(self, formato):
        """
        returns é uma colecao de pares estado acao guardando um
        dicionario para armazenar o valor maximo de reforcos obtidos,
        o numero de vezes que o par estado acao foi visitado e o ultimo
        episodio em que o par estado acao foi visitado
        """
        self.returns = []
        for i in range(formato[0]):
            self.returns.append([])
            for j in range(formato[1]):
                self.returns[i].append(dict())
                for acao in self.acoes:
                    self.returns[i][j][acao] = {"value": 0, "count": 0, "lastEpisode": 0}

    def setEnvironment(self, environment):
        self.environment = environment
    
    def setPos(self, x, y):
        self.x = x
        self.y = y

    def mover(self, acao):
        return self.environment.mover(self, acao)
    
    def get_action(self):
        return self.policy[self.y][self.x]