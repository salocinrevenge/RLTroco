from LearningStrategy import LearningStrategy
import random
class MonteCarlo(LearningStrategy):
    def __init__(self) -> None:
        pass

    def setup(self, environment, agent):
        self.environment = environment
        self.agent = agent
    
    def train(self, episodes, politicaAleatoria = True):
        # Initialize
        formato = self.environment.get_size()
        self.agent.iniciaPolicy(formato, politicaAleatoria)
        self.agent.iniciaQ(formato)
        self.agent.iniciaRetorno(formato)

        for ep in range(episodes):
            print(f"{ep=}")
            acao = random.choice(self.agent.acoes)

            #escolhe posicao aleatoria valida para o agente
            while True:
                estado = (random.randrange(0, formato[0]), random.randrange(0, formato[1]))
                if self.environment.mapaOriginal[estado[0]][estado[1]] in {self.environment.simbolosPadrao["path"], self.environment.simbolosPadrao["goal"]}:
                    break
            self.episode(estado, acao, max_steps= formato[1]*formato[0])
            g = 0
            for t in range(len(self.agent.lembrancas)-1, -1, -1): 
                memoria = self.agent.lembrancas[t]  # memoria = (estado, acao, reforco)
                g = self.agent.gamma*g + memoria[2]
                # verifica se o par estado acao ja foi inserido em returns
                if self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["lastEpisode"] != ep:
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["lastEpisode"] = ep
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["value"] = g
                    self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["count"] += 1
                    media = self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["value"]/self.agent.returns[memoria[0][0]][memoria[0][1]][memoria[1]]["count"]
                    self.agent.livro_Q[memoria[0][0]][memoria[0][1]][memoria[1]] = media
                    self.agent.policy[memoria[0][0]][memoria[0][1]] = max(self.agent.acoes, key = lambda acao: self.agent.livro_Q[memoria[0][0]][memoria[0][1]][acao])    # recebe a acao que maximiza o valor de Q

    def episode(self, estado, acao, max_steps):
        step_count = 0
        self.agent.lembrancas = []
        self.environment.setAgentPos(estado[0], estado[1])
        while not self.environment.in_terminal_state() and step_count < max_steps:  # enquanto nao estiver em um estado terminal
           step_count +=1  # incrementa o numero de passos
           reward = self.environment.mover(self.agent,acao) # realiza a acao e recebe a recompensa
           self.agent.lembrancas.append(((self.agent.y,self.agent.x), acao, reward)) # guarda o passo
           acao = self.agent.get_action() # escolhe uma acao de acordo com a politica
