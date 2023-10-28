from Environment import Environment
from MonteCarlo import MonteCarlo
from QLearning import QLearning
from SARSA import SARSA
from LinearFunctionApproximation import LinearFunctionApproximation
from Renderer import Renderer

class Professor():
    learningStrategys = {"Monte Carlo": MonteCarlo(), "Q-Learning": QLearning(), "SARSA": SARSA(), "Linear Function Approximation": LinearFunctionApproximation()}
    
    def __init__(self, caminhoSala = "sala", learningStrategy = None, nEpisodios = 1000):
        self.learningStrategy = self.learningStrategys[learningStrategy]
        self.env = Environment(path = caminhoSala)
        self.aluno = self.env.getAgent() 
        self.learningStrategy.setup(self.env, self.aluno)
        self.ensinar(nEpisodios)

    def ensinar(self, nEpisodios):
        self.learningStrategy.train(nEpisodios, chanceExploracao = 0.3)
        print("treinei")
        render = Renderer(self.env, self.env.mapa, "Ambiente", (800, 800))
        render.addConteudo(self.aluno.policy)

if __name__ == '__main__':
    professor = Professor(caminhoSala="sala7.txt", learningStrategy="Monte Carlo", nEpisodios=10000)