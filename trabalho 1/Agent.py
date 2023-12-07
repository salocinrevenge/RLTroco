import random

class Agent():
    actions = ['up', 'down', 'left', 'right']
    def __init__(self, x, y, environment, gamma = 0.9, display=True):
        self.environment = environment
        self.x = x
        self.y = y
        self.gamma = gamma
        self.display = display

    def action_idx(self, action: str):
        return self.actions.index(action)

    def startQ(self, shape, start_value = float("-inf")):
        """
        livroQ é uma lista de listas de dicionarios,
        ele armazena 
        
        """
        self.livro_Q: list[list[dict]] = []
        for i in range(shape[0]):
            self.livro_Q.append([])
            for _ in range(shape[1]):
                self.livro_Q[i].append(dict())
                for acao in self.actions:
                    self.livro_Q[i][-1][acao] = start_value

    def startV(self, shape):
        """
        livroV é uma lista de listas de dicionarios,
        ele armazena 
        
        """ 
        self.book_V: list[list] = []
        for i in range(shape[0]):
            self.book_V.append([])
            for _ in range(shape[1]):
                
                self.book_V[i].append(float("-inf"))
    
    def startPolicy(self, shape, randomPolicy):
        """
        A policy é uma matriz de caracteres que guarda a acao principal
        a ser tomada ate o momento
        
        """
        self.policy: list[list[str]] = []
        for i in range(shape[0]):
            self.policy.append([])
            for j in range(shape[1]):
                if self.environment.symbols[self.environment.original_map[i][j]] == "wall":
                    self.policy[i].append("wall")
                    continue
                if randomPolicy:
                    self.policy[i].append(random.choice(self.actions))
                else:
                    self.policy[i].append(self.actions[0])
        
        if self.display:
            self.render = self.environment.render.addConteudo(self.policy)

    def startReturns(self, shape):
        """
        returns é uma colecao de pares estado acao guardando um
        dicionario para armazenar o valor maximo de reforcos obtidos,
        o numero de vezes que o par estado acao foi visitado e o ultimo
        episodio em que o par estado acao foi visitado
        """
        self.returns: list[list[dict]] = []
        for i in range(shape[0]):
            self.returns.append([])
            for j in range(shape[1]):
                self.returns[i].append(dict())
                for acao in self.actions:
                    self.returns[i][j][acao] = {"value": 0, "count": 0, "lastEpisode": 0}

    def setEnvironment(self, environment):
        self.environment = environment
    
    def setPos(self, position):
        self.x = position[1]
        self.y = position[0]

    def move(self, action):
        return self.environment.move(self, action)
    
    def get_action(self):
        return self.policy[self.y][self.x]
