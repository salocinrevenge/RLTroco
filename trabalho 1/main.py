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

            if is_nth_bit_on(environment.walls[y, x], 0):
                x_linha = [x, x+1]
                y_linha = [y+1, y+1]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            if is_nth_bit_on(environment.walls[y, x], 1):
                x_linha = [x+1, x+1]
                y_linha = [y, y+1]
                plt.plot(x_linha, y_linha, color='black', linewidth=self.grossura)
            if is_nth_bit_on(environment.walls[y, x], 2):
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

    def numbers_to_arrows(number):
        match number:
            case 0:
                # return '↑'
                return '↓'
            case 1:
                return '→'
            case 2:
                # return '↓'
                return '↑'
            case 3:
                return '←'
            case _:
                return '?'



class Environment:

    def __init__(self, stochastic_threshold=0):
        
        self.rewards = np.full((3, 3), -1, dtype=np.int64)
        self.rewards[0,0] = 100
        self.terminal_states = [np.asarray([0,0])]

        self.cur_state = np.asarray([2,2])
        self.stochastic_threshold = stochastic_threshold
        self.renderer = Render()
        
        self.input_to_movement = {
            0: np.asarray([1,  0]),
            2: np.asarray([-1,  0]),
            3: np.asarray([ 0, -1]),
            1: np.asarray([ 0,  1]),
        }
        self.wall_code = {
            'U': 0,
            'R': 1,
            'D': 2,
            'L': 3
        }

        self.walls = np.zeros((3, 3), dtype=np.int64)
        self.walls[-1, :] += 2**self.wall_code['U']
        self.walls[:, -1] += 2**self.wall_code['R']
        self.walls[0,  :] += 2**self.wall_code['D']
        self.walls[:,  0] += 2**self.wall_code['L']


    def render(self):
        self.renderer.render(self)

    
    def react(self, input:str) -> int:  # executa a acao se possivel e retorna a recompensa
        if random.random() < self.stochastic_threshold:
            input = random.choice(list('UDLR'))
            input = self.wall_code[input]
        
        
        movement_allowed = not is_nth_bit_on(self.walls[self.cur_state[0], self.cur_state[1]], input)

        if movement_allowed:
            self.cur_state += self.input_to_movement[input]
        
        return self.rewards[self.cur_state[0], self.cur_state[1]]

    def in_terminal_state(self):
        return any((self.cur_state == i).all() for i in self.terminal_states)

    def reset(self):
        self.cur_state = np.asarray([2,2])
    
    def get_size(self):
        return self.rewards.shape

class LearningStrategy:

    def __init__(self, environment: Environment):
        self.environment = environment
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
        self.policy = np.empty(self.environment.get_size(), dtype=np.int64) % 4
        self.Q = np.zeros(self.environment.get_size() + (4,), dtype=np.float64)
        self.returns = []
        for i in range(self.environment.get_size()[0]):
            self.returns.append([])
            for j in range(self.environment.get_size()[1]):
                self.returns[i].append([])
                for _ in range(4):
                    self.returns[i][j].append([])


    def run_episode(self, max_steps=1000):

        self.environment.cur_state = np.asarray([random.randrange(self.environment.get_size()[0]), random.randrange(self.environment.get_size()[1])])   # comeca em um estado aleatorio
        action = random.randrange(4)  # escolhe uma acao aleatoria
        step_count = 0  # conta o numero de passos
        steps = []  # guarda os passos
        while not self.environment.in_terminal_state() and step_count < max_steps:  # enquanto nao estiver em um estado terminal
            step_count +=1  # incrementa o numero de passos
            reward = self.environment.react(action) # reage a acao e recebe a recompensa
            steps.append((self.environment.cur_state.copy(), action, reward)) # guarda o passo
            action = self.get_next_action() # escolhe uma acao de acordo com a politica
        G = 0   # inicializa o retorno
        for step in reversed(steps):
            G = G*self.gamma + step[2]  # calcula o retorno
            if not any(((step[0] == i[0]).all() and step[1] == i[1]) for i in self.returns[self.environment.cur_state[0]][self.environment.cur_state[1]][step[1]]):
                self.returns[self.environment.cur_state[0]][self.environment.cur_state[1]][step[1]].append((step[0], step[1],G))
                self.Q[self.environment.cur_state[0], self.environment.cur_state[1], step[1]] = np.mean([i[2] for i in self.returns[self.environment.cur_state[0]][self.environment.cur_state[1]][step[1]]])
                self.policy[self.environment.cur_state[0], self.environment.cur_state[1]] = np.argmax(self.Q[self.environment.cur_state[0], self.environment.cur_state[1]])
            # self.update(reward)
    
    

    def train(self, num_iter):
        for _ in range(num_iter):
            self.run_episode()
           
            # input()

    def get_next_action(self):
        return self.policy[self.environment.cur_state[0], self.environment.cur_state[1]]


# class Agent:

#     def __init__(self, strategy: LearningStrategy):
#         self.strategy = strategy
#         self.environment = self.strategy.environment
    

#     def act(self):
#         input = self.strategy.get_next_action()
#         reward = self.environment.react(input)
#         self.strategy.update(reward)






if __name__ == '__main__':
    env = Environment()
    # env.render()
    strategy = MonteCarlo(env)
    strategy.train(int(10000))

    numbers_to_arrows = np.vectorize(Render.numbers_to_arrows)
    print(numbers_to_arrows(strategy.policy))