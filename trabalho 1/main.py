import numpy as np
import random


def is_nth_bit_on(number, n):
    return bool((number >> n) & 1)


class Environment:

    def __init__(self, stochastic_threshold=0):
        
        self.rewards = np.full((10, 10), -1, dtype=np.int)
        self.rewards[0,0] = 100

        self.cur_state = np.asarray([9,9])
        self.stochastic_threshold = stochastic_threshold

        
        self.input_to_movement = {
            'U': np.asarray([-1,  0]),
            'D': np.asarray([ 1,  0]),
            'L': np.asarray([ 0, -1]),
            'R': np.asarray([ 0,  1]),
        }
        self.wall_code = {
            'U': 0,
            'R': 1,
            'D': 2,
            'L': 3
        }

        self.walls = np.zeros((10, 10), dtype=np.uint)
        self.walls[0, :]  += 2**self.wall_code['U']
        self.walls[:, -1] += 2**self.wall_code['R']
        self.walls[-1, :] += 2**self.wall_code['D']
        self.walls[:, 0]  += 2**self.wall_code['L']

    
    def react(self, input:str) -> int:
        if random.random() < self.stochastic_threshold:
            input = random.choice(list('UDLR'))
        
        movement_allowed = not is_nth_bit_on(self.walls[self.cur_state[0], self.cur_state[1]], self.wall_code[input])

        if movement_allowed:
            self.cur_state += self.input_to_movement(input)
        
        return self.rewards[self.cur_state[0], self.cur_state[1]]


class LearningStrategy:

    def __init__(self, update:function):
        self.update = update


class Agent:

    def __init__(self, environment: Environment, strategy: LearningStrategy):
        self.environment = environment
        self.strategy = strategy
    

    def act(self):
        input = ...
        reward = self.environment.react(input)
        self.strategy.update(reward)


