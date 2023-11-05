from Environment import Environment
from MonteCarlo import MonteCarlo
from QLearning import QLearning
from SARSA import SARSA
from LinearFunctionApproximation import LinearFunctionApproximation
from Renderer import Renderer
from Agent import Agent

class Professor():
    learningStrategys = {"Monte Carlo": MonteCarlo(), "Q-Learning": QLearning(), "SARSA": SARSA(), "Linear Function Approximation": LinearFunctionApproximation()}
    
    def __init__(self, caminhoSala = "sala", learningStrategy = None, nEpisodios = 1000, chanceExploracao = 0):
        self.learningStrategy = self.learningStrategys[learningStrategy]
        self.env = Environment(path = caminhoSala)
        self.aluno = Agent(gamma = 0.9)
        self.env.setAgent(self.aluno)
        self.aluno.setEnvironment(self.env)
        self.learningStrategy.setup(self.env, self.aluno)
        self.chanceExploracao = chanceExploracao
        self.ensinar(nEpisodios)

    def ensinar(self, nEpisodios):
        self.learningStrategy.train(nEpisodios, chanceExploracao = self.chanceExploracao)
        render = Renderer(self.env, self.env.mapa, "Ambiente")
        render.addConteudo(self.aluno.policy)

if __name__ == '__main__':
    sala = input("Digite o numero da sala: ")
    professor = Professor(caminhoSala=f"sala{sala}.txt", learningStrategy="Monte Carlo", nEpisodios=10000, chanceExploracao = 0.3)
