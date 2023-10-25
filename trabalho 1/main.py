import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import product


def is_nth_bit_on(number, n):
    return bool((number >> n) & 1)


class Render:
    def __init__(self) -> None:
        self.grossura = 2
    
    def render(self, environment):
        # usa matplotlib para renderizar o ambiente

        # eixos
        plt.axis('on')

        # desenha as grades de 1 em 1
        plt.xticks(np.arange(0, 11, 1))
        plt.yticks(np.arange(0, 11, 1))
        plt.grid(True, which='both')

        # desenha as paredes
        for y, x in product(range(environment.walls.shape[0]), range(environment.walls.shape[1])):
            if environment.walls[y, x] == 0:
                continue

            if is_nth_bit_on(environment.walls[y, x], 2):
                x_linha = [x, x+1]
                y_linha = [y+1, y+1]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            if is_nth_bit_on(environment.walls[y, x], 1):
                x_linha = [x+1, x+1]
                y_linha = [y, y+1]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            if is_nth_bit_on(environment.walls[y, x], 0):
                x_linha = [x, x+1]
                y_linha = [y, y]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            if is_nth_bit_on(environment.walls[y, x], 3):
                x_linha = [x, x]
                y_linha = [y, y+1]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            
        
        # desenha os estados terminais
        for state in environment.terminal_states:
            plt.scatter(state[1]+0.5, state[0]+0.5, color='blue', marker='*', s=100)
        # desenha o agente usando um circulo vermelho
        plt.scatter(environment.cur_state[1]+0.5, environment.cur_state[0]+0.5, color='red', marker='o', s=100)

        # faz a imagem quadrada
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


class Environment:

    def __init__(self, stochastic_threshold=0):
        
        self.rewards = np.full((10, 10), -1, dtype=np.int64)
        self.rewards[0,0] = 100

        self.cur_state = np.asarray([9,9])
        self.stochastic_threshold = stochastic_threshold
        self.renderer = Render()
        
        self.input_to_movement = {
            'U': np.asarray([1,  0]),
            'D': np.asarray([-1,  0]),
            'L': np.asarray([ 0, -1]),
            'R': np.asarray([ 0,  1]),
        }
        self.wall_code = {
            'U': 0,
            'R': 1,
            'D': 2,
            'L': 3
        }

        self.walls = np.zeros((10, 10), dtype=np.int64)
        self.walls[0, :]  += 2**self.wall_code['U']
        self.walls[:, -1] += 2**self.wall_code['R']
        self.walls[-1, :] += 2**self.wall_code['D']
        self.walls[:, 0]  += 2**self.wall_code['L']

        self.terminal_states = [np.asarray([0,0])]

    def render(self):
        self.renderer.render(self)

    
    def react(self, input:str) -> int:
        if random.random() < self.stochastic_threshold:
            input = random.choice(list('UDLR'))
        
        movement_allowed = not is_nth_bit_on(self.walls[self.cur_state[0], self.cur_state[1]], self.wall_code[input])

        if movement_allowed:
            self.cur_state += self.input_to_movement(input)
        
        return self.rewards[self.cur_state[0], self.cur_state[1]]

    def in_terminal_state(self):
        return any((self.cur_state == i).all() for i in self.terminal_states)

    def reset(self):
        self.cur_state = np.asarray([9,9])

class LearningStrategy:

    def __init__(self, environment: Environment):
        self.environment = environment
        self.V = np.zeros(self.environment.rewards.shape)
        self.Q = np.zeros(self.environment.rewards.shape)
        self.G = ...
        self.gamma = 0.9

    def update(self):
        pass

    def run_episode(self):
        pass

    def get_next_action(self):
        random.choice(list('UDLR'))


class MonteCarlo(LearningStrategy):

    def __init__(self, environment: Environment):
        super().__init__(environment)

    def update(self):
        pass

    def run_episode(self):
        pass

    def get_next_action(self):
        return super().get_next_action()


class Agent:

    def __init__(self, strategy: LearningStrategy):
        self.strategy = strategy
        self.environment = self.strategy.environment
    

    def act(self):
        input = self.strategy.get_next_action()
        reward = self.environment.react(input)
        self.strategy.update(reward)



if __name__ == '__main__':
    env = Environment()
    env.render()