#!/usr/bin/env python3

from Environment import Environment
from LearningStrategies import *
from Renderer import Renderer
from argparse import ArgumentParser
import numpy as np
import random
import csv

def salvar(dicionario, nome):
  with open(nome, "w", newline="") as arquivo:
    writer = csv.DictWriter(arquivo, fieldnames=dicionario.keys())
    writer.writeheader()
    for i in range(len(dicionario["sala"])):
        writer.writerow({key: dicionario[key][i] for key in dicionario.keys()})

if __name__ == '__main__':
    salas = [1,2,3,3.1,3.2,4,5,6,7,8,9,10,11,12]
    for i in range(len(salas)):
        salas[i] = "salas/sala"+str(salas[i])+".txt"
    approxis = [False, True]
    estocasticos = [0.0, 0.1, 0.5, 0.7]
    exploration_chance = [0, 0.3, 0.5]
    learning_strategys = [MonteCarlo(), SARSA(0.5), QLearning()]
    episodes = [1000, 10000, 100000]

    # para teste de corretude
    approxis = [False]
    estocasticos = [0.0]
    exploration_chance = [0]
    learning_strategys = [MonteCarlo()]
    episodes = [1000]

    n = 0
    nExp = 0
    for episode in episodes:
        for learning_strategy in learning_strategys:
            for exploration in exploration_chance:
                for estocastico in estocasticos:
                    for approx in approxis:
                        dicionario = dict()
                        # dicionario["exploration"] = exploration
                        # dicionario["estocastico"] = estocastico
                        # dicionario["approx"] = approx
                        # dicionario["episode"] = episode
                        # dicionario["strategy"] = learning_strategy.__class__.__name__
                        dicionario["sala"] = []
                        dicionario["tempo"] = []
                        dicionario["taxa"] = []
                        dicionario["recompensa"] = []
                        dicionario["passos"] = []

                        for sala in salas:
                            np.random.seed(42)
                            random.seed(42)
                            environment = Environment(sala, estocastico, display= False)
                            agent = Agent(x=0, y=0, environment=environment, display=environment.display)
                            environment.agent = agent
                            learning_strategy.setup(environment, agent)

                            tempo = learning_strategy.train(episode, exploration_chance=exploration, appx=approx, display=False)
                            teste = learning_strategy.test(display = False)
                            dicionario["tempo"].append(tempo)
                            dicionario["sala"].append(sala)
                            dicionario["taxa"].append(teste["sucesso"])
                            dicionario["recompensa"].append(teste["recompensa"])
                            dicionario["passos"].append(teste["steps"])
                            n+=1
                            print(f"{n} experimentos executados de {len(salas)*len(approxis)*len(estocasticos)*len(exploration_chance)*len(learning_strategys)*len(episodes)}")
                        salvar(dicionario, str(nExp)+".csv")
                        nExp+=1
