#!/usr/bin/env python3

from Environment import Environment
from LearningStrategies import *
from Renderer import Renderer
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--room', '-r', type=str)
    parser.add_argument('--episodes', '-e', type=int, default=100_000)
    parser.add_argument('--exploration-chance', '-c', type=float, default=0.3, dest='exploration_chance')
    parser.add_argument('--strategy', '-s', type=str, dest='learning_strategy')
    parser.add_argument('--no-display', '-d', action='store_true', dest='no_display')

    return parser.parse_args()



if __name__ == '__main__':

    args = parse_args()

    room_path = args.room
    num_episodes = args.episodes
    exploration_chance = args.exploration_chance

    match args.learning_strategy.lower():
        case "montecarlo" | "monte" | "monte-carlo" | "mc":
            learning_strategy = MonteCarlo()
        case "sarsa" | "s":
            raise NotImplementedError("SARSA not implemented")
            learning_strategy = SARSA()
        case "qlearning" | "q-learning" | "q":
            raise NotImplementedError("Q-Learning not implemented")
            learning_strategy = QLearning()
        case "linear" | "lfa" | "l":
            raise NotImplementedError("Linear Function Approximation not implemented")
            learning_strategy = LinearFunctionApproximation()
        case _:
            raise ValueError(f"Invalid learning strategy {args.learning_strategy}")

    environment = Environment(room_path, not args.no_display)
    agent = environment.getAgent()
    learning_strategy.setup(environment, agent)

    learning_strategy.train(num_episodes, chanceExploracao=exploration_chance)
    print("Done")

    if not args.no_display:
        renderer = Renderer(environment, environment.mapa, "Ambiente")
        renderer.addConteudo(agent.policy)
