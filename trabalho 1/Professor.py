from Environment import Environment
from MonteCarlo import MonteCarlo
from QLearning import QLearning
from SARSA import SARSA
from LinearFunctionApproximation import LinearFunctionApproximation

class Professor():
    learningStrategys = {"Monte Carlo": MonteCarlo(), "Q-Learning": QLearning(), "SARSA": SARSA(), "Linear Function Approximation": LinearFunctionApproximation()}
    
    def __init__(self, caminhoSala = "sala", learningStrategy = None):
        self.learningStrategy = self.learningStrategys[learningStrategy]
        self.env = Environment(path = caminhoSala)
        self.aluno = self.env.getAgent()
        self.learningStrategy.setup(self.env, self.aluno)

    def ensinar(self):
        self.learningStrategy.train(10000)
        print("treinei")

if __name__ == '__main__':
    professor = Professor(caminhoSala="sala.txt", learningStrategy="Monte Carlo")
    professor.ensinar()