import Environment
import Agente

class Professor():
    def __init__(self, caminhoSala = "sala" ,learningStrategy = None):
        self.learningStrategy = learningStrategy
        self.env = Environment(path = caminhoSala)
        self.aluno = Agente(self.env)
        self.env.setAgente(self.aluno)

    def ensinar(self):
        pass