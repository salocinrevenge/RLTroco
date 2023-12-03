#!/usr/bin/env python3

from Environment import Environment
from LearningStrategies import *
from Renderer import Renderer
from argparse import ArgumentParser
import numpy as np
import random

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--room', '-r', type=str, required=True)
    parser.add_argument('--episodes', '-e', type=int, default=100_000)
    parser.add_argument('--exploration-chance', '-c', type=float, default=0.3, dest='exploration_chance')
    parser.add_argument('--learning-strategy', '-l', type=str, dest='learning_strategy', required=True)
    parser.add_argument('--no-display', '-d', action='store_true', dest='no_display')
    parser.add_argument('--stochastic', '-s', type=float, dest='stochastic', default=0.0)

    return parser.parse_args()

if __name__ == '__main__':
    np.random.seed(42)
    random.seed(42)
    args = parse_args()

    room_path = args.room
    num_episodes = args.episodes
    exploration_chance = args.exploration_chance

    learning_strategy = args.learning_strategy.lower()

    if learning_strategy in ["montecarlo","monte","monte-carlo","mc"]:
        learning_strategy = MonteCarlo()
    elif learning_strategy in ["sarsa" , "s"]:
        learning_strategy = SARSA(0.5)
    elif learning_strategy in ["qlearning","q-learning","q"]:
        learning_strategy = QLearning()
    elif learning_strategy in ["linear","lfa","l"]:
        raise NotImplementedError("Linear Function Approximation not implemented")
    else:
        raise ValueError(f"Invalid learning strategy {args.learning_strategy}")

    environment = Environment(room_path, args.stochastic, not args.no_display)
    agent = environment.getAgent()
    learning_strategy.setup(environment, agent)

    learning_strategy.train(num_episodes, exploration_chance=exploration_chance)
    print("Done")

    if not args.no_display:
        renderer = Renderer(environment, environment.map, "Ambiente")
        renderer.addConteudo(agent.policy)
