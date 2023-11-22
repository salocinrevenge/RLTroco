import random
from Environment import Environment
from Agent import Agent

class LearningStrategy():
    def train(self, episodes):
        pass

    def setup(self, environment, agent):
        self.environment: Environment = environment
        self.agent: Agent = agent

class MonteCarlo(LearningStrategy):
    def __init__(self) -> None:
        pass

    
    def train(self, episodes, politicaAleatoria = True, chanceExploracao = 0):
        # Initialize
        formato = self.environment.get_size()
        self.agent.iniciaPolicy(formato, politicaAleatoria)
        self.agent.iniciaQ(formato)
        self.agent.iniciaRetorno(formato)

        for ep in range(episodes):
            if ep % (episodes//10) == 0:
                print(f"{ep=}")
            # escolhe posicao aleatoria valida para o agente
            while True:
                estado = (random.randrange(0, formato[0]), random.randrange(0, formato[1]))
                if self.environment.mapaOriginal[estado[0]][estado[1]] in {self.environment.simbolosPadrao["path"], self.environment.simbolosPadrao["goal"]}:
                    break
            # escolhe uma acao diferente da dita pela politica atual
            for _ in range(len(self.agent.acoes)*2):    # limite maximo de tentativas
                acao = random.choice(self.agent.acoes)
                if acao != self.agent.policy[estado[0]][estado[1]]:
                    # se a acao nao te leva para uma parede
                    if self.environment.util(estado, acao): 
                        break
            else:
                acao = self.agent.policy[estado[0]][estado[1]]
            self.episode(estado, acao, max_steps= formato[1]*formato[0], chanceExploracao = chanceExploracao)
            g = 0
            for t in range(len(self.agent.lembrancas)-1, -1, -1): 
                memoria = self.agent.lembrancas[t]  # memoria = (estado, acao, reforco)
                g = self.agent.gamma*g + memoria[2]
                # verifica se o par estado acao ja foi inserido em returns
                if self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["lastEpisode"] != ep:
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["lastEpisode"] = ep
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["value"] += g
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["count"] += 1
                    media = self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["value"]/self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["count"]
                    self.agent.livro_Q[memoria[0][0]][memoria[0][1]][memoria[1]] = media
                    self.agent.policy[memoria[0][0]][memoria[0][1]] = max(self.agent.acoes, key = lambda acao: self.agent.livro_Q[memoria[0][0]][memoria[0][1]][acao])    # recebe a acao que maximiza o valor de Q

    def episode(self, estado, acao, max_steps, chanceExploracao=0):
        step_count = 0
        self.agent.lembrancas = []
        self.environment.setAgentPos(estado[0], estado[1])

        while (not self.environment.in_terminal_state()) and (step_count < max_steps):  # enquanto nao estiver em um estado terminal
            step_count +=1  # incrementa o numero de passos
            posAnterior = (self.agent.y, self.agent.x)
            reward = self.environment.mover(self.agent,acao) # realiza a acao e recebe a recompensa
            self.agent.lembrancas.append((posAnterior, acao, reward)) # guarda o passo
            if random.random() < chanceExploracao:
                for _ in range(len(self.agent.acoes)*2):    # limite maximo de tentativas
                    acao = random.choice(self.agent.acoes)
                    # se a acao nao te leva para uma parede
                    if self.environment.util(estado, acao): break
            else:
                acao = self.agent.get_action() # escolhe uma acao de acordo com a politica


class SARSA(LearningStrategy):

    def __init__(self, lam):
        super().__init__()
        self.lam = lam

    def get_epsilon_greedy(self, exploration_chance, estado):
        if random.random() < exploration_chance:
            return random.choice(self.agent.acoes)
        else:
            return max(self.agent.acoes, key = lambda acao: self.agent.livro_Q[estado[0]][estado[1]][acao])
                
    def train(self, episodes, politicaAleatoria=True, chanceExploracao=0, alpha=0.1):

        formato = self.environment.getSize()
        self.agent.iniciaQ(formato, 0)

        for ep in range(episodes):
            if ep % (episodes//10) == 0: print(f"{ep=}")
            
            E = dict()

            # escolhe posicao aleatoria valida para o agente
            while True:
                estado = (random.randrange(0, formato[0]), random.randrange(0, formato[1]))
                if self.environment.mapaOriginal[estado[0]][estado[1]] in {self.environment.simbolosPadrao["path"], self.environment.simbolosPadrao["goal"]}:
                    break
            
            S = (self.agent.y, self.agent.x)
            A = random.choice(self.agent.acoes)

            step_count = 0
            max_steps = 1e4
            while (not self.environment.in_terminal_state()) and (step_count < max_steps):
                R = self.environment.mover(self.agent, A)
                S_prime = (self.agent.y, self.agent.x)
                A_prime = self.get_epsilon_greedy(chanceExploracao, S_prime)
                pair = (S, A)
                E[pair] = E[pair] + 1 if pair in E.keys() else 1

                delta = R + self.agent.gamma * self.agent.livro_Q[S[0]][S[1]][A] - self.agent.livro_Q[S_prime[0]][S_prime[1]][A_prime]

                for (s, a) in E.keys():
                    self.agent.livro_Q[S[0]][S[1]][A] += alpha * delta * E[(s,a)]
                    E[(S,A)] *= self.agent.gamma * self.lam
                
                S = S_prime
                A = A_prime

        self.agent.iniciaPolicy(formato, politicaAleatoria)
        for i in range(len(self.agent.livro_Q)):
            for j in range(len(self.agent.livro_Q[0])):
                self.agent.policy[i][j] = max(self.agent.acoes, key = lambda acao: self.agent.livro_Q[i][j][acao])
    

class LinearFunctionApproximation(LearningStrategy):
    ...

class QLearning(LearningStrategy):
    ...