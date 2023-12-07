import random
from Environment import Environment
from Agent import Agent
import numpy as np
import time
import matplotlib.pyplot as plt

class LearningStrategy():
    def train(self, episodes):
        pass

    def setup(self, environment, agent):
        self.environment: Environment = environment
        self.agent: Agent = agent
        
    def show_loss(self, rewards, window_size=None):
        # se não for numpy array, transformar em um
        if not isinstance(rewards, np.ndarray):
            rewards = np.asarray(rewards)

        if window_size is not None:
            # calcular a média móvel
            rewards = np.convolve(rewards, np.ones(window_size), 'valid') / window_size

        # Criar o gráfico
        plt.plot(rewards)
        # Adicionar um título
        plt.title("Gráfico de recompensas")

        # Adicionar um eixo x
        plt.xlabel("Episódio")

        # Adicionar um eixo y
        plt.ylabel("Recompensa")

        # Exibir o gráfico
        plt.show()


class MonteCarlo(LearningStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.episode_R = []
        self.episode_length = []
        self.Q = None
        self.W = np.random.rand(3)
        self.time = []


    def get_Q(self, x, y, action, linear_approximation = False):
        if not linear_approximation:
            return self.Q[x,y,action]
        
        terms = np.array([x,y,action])
        return np.dot(self.W, terms).astype(int)

    
    def train(self, episodes, randomPolicy = True, exploration_chance = 0):
        # Initialize
        begin_training_time = time.time()
        shape = self.environment.get_size()
        self.agent.startPolicy(shape, randomPolicy)
        self.agent.startReturns(shape)
        self.Q = np.zeros((shape[0],shape[1], len(self.agent.actions)))
        self.agent.startV(shape)
        current_exploration_chance = exploration_chance
        rewards = []
        for ep in range(episodes):
            start_time = time.time()
            if ep % (episodes//10) == 0:
                print(f"{ep=}")
                path = self.path_from((1,1))
                print('Tamanho do episódio:', len(path))
                print('Recompensa', sum([i[2] for i in path]))
                path_dict = {}
                for s,a,r in path:
                    path_dict[s] = a
                self.environment.render.show_path(path_dict)
            # escolhe posicao aleatoria valida para o agente
            while True:
                state = (random.randrange(0, shape[0]), random.randrange(0, shape[1]))
                if self.environment.original_map[state[0]][state[1]] in {self.environment.default_symbols["path"], self.environment.default_symbols["goal"]}:
                    break
            # escolhe uma acao diferente da dita pela politica atual
            for _ in range(len(self.agent.actions)*2):    # limite maximo de tentativas
                action = random.choice(self.agent.actions)
                if action != self.agent.policy[state[0]][state[1]]:
                    # se a acao nao te leva para uma parede
                    if self.environment.util(state, action): 
                        break
            else:
                action = self.agent.policy[state[0]][state[1]]
            self.episode(state, action, max_steps= shape[1]*shape[0], exploration_chance = exploration_chance)
            g = 0
            for t in range(len(self.agent.recalls)-1, -1, -1): 
                memory = self.agent.recalls[t]  # memoria = (estado, acao, reforco)
                g = self.agent.gamma*g + memory[2]
                # verifica se o par estado acao ja foi inserido em returns
                if self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["lastEpisode"] != ep:
                    self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["lastEpisode"] = ep
                    self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["value"] += g
                    self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["count"] += 1
                    media = self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["value"]/self.agent.returns[memory[0][0]][memory[0][1]][memory[1]]["count"]
                    self.Q[memory[0][0],memory[0][1],self.agent.action_idx(memory[1])] = media
                    self.agent.book_V[memory[0][0]][memory[0][1]] = media
                    self.agent.policy[memory[0][0]][memory[0][1]] = max(self.agent.actions, key = lambda action: self.get_Q(memory[0][0],memory[0][1],self.agent.action_idx(action)))    # recebe a action que maximiza o valor de Q
            # atualiza a chance de exploracao
            rewards.append(np.asarray(self.episode_R[ep]).sum())
            current_exploration_chance *= 0.999
            end_time = time.time()
            time_difference_seconds = end_time - start_time
            self.time.append(time_difference_seconds)

        end_training_time = time.time()
        print(f"Tempo total de treinamento: {end_training_time - begin_training_time} segundos")
        self.show_loss(rewards, window_size=(len(rewards)//10))

            
    def episode(self, state, action, max_steps, exploration_chance=0):
        step_count = 0
        self.agent.recalls = []
        reward = self.environment.setAgentPos(state[0], state[1])
        episode_R = [reward]

        while (not self.environment.in_terminal_state()) and (step_count < max_steps):  # enquanto nao estiver em um estado terminal
            step_count +=1  # incrementa o numero de passos
            last_pos = (self.agent.y, self.agent.x)
            reward = self.environment.move(self.agent,action) # realiza a acao e recebe a recompensa
            episode_R.append(reward)
            self.agent.recalls.append((last_pos, action, reward)) # guarda o passo
            if random.random() < exploration_chance:
                for _ in range(len(self.agent.actions)*2):    # limite maximo de tentativas
                    action = random.choice(self.agent.actions)
                    # se a acao nao te leva para uma parede
                    if self.environment.util(state, action): break
            else:
                action = self.agent.get_action() # escolhe uma acao de acordo com a politica
        self.episode_R.append(episode_R)
        self.episode_length.append(step_count)
    
    def path_from(self, starting_point):
        shape = self.environment.get_size()
        max_steps = shape[0] * shape[1]
        step_count = 0
        state = starting_point
        self.environment.setAgentPos(state[0], state[1])
        tuples = []
        while (not self.environment.in_terminal_state()) and (step_count < max_steps):
            action =  self.agent.policy[state[0]][state[1]]
            R = self.environment.move(self.agent, action)
            tuples.append((state,action,R))
            state = (self.agent.y, self.agent.x)
            step_count+=1
        return tuples


class SARSA(LearningStrategy):

    def __init__(self, lam):
        super().__init__()
        self.lam = lam
        self.episode_R = []
        self.episode_length = []
        self.Q = None
        self.W = np.random.rand(3)
        self.time = []

    def get_Q(self, x, y, action, linear_approximation = False):
        if not linear_approximation:
            return self.Q[x,y,action]
        
        terms = np.array([x,y,action])
        return np.dot(self.W, terms).astype(int)
        

    def get_greedy_action(self,state):
        return max(self.agent.actions, key = lambda action: self.get_Q(state[0], state[1], self.agent.action_idx(action)))
    
    def get_epsilon_greedy(self, exploration_chance, state):
        if random.random() < exploration_chance:
            return random.choice(self.agent.actions)
        else:
            return max(self.agent.actions, key = lambda action: self.get_Q(state[0], state[1], self.agent.action_idx(action)))
                
    def train(self, episodes, random_policy=True, exploration_chance=0.3, alpha=0.001):
        begin_training_time = time.time()
        shape = self.environment.get_size()
        ec = exploration_chance
        num_states = shape[0]*shape[1]
        linear_decay = exploration_chance/episodes
        self.Q = np.zeros((shape[0],shape[1], len(self.agent.actions)))
        rewards = []
        E = dict()
        for ep in range(episodes):
            start_time = time.time()
            episode_R = []
            if ep % (episodes//10) == 0: 
                print(f"{ep=}")
                path = self.path_from((1,1))
                print('Tamanho do episódio:', len(path))
                print('Recompensa', sum([i[2] for i in path]))
                path_dict = {}
                for s,a,r in path:
                    path_dict[s] = a
                self.environment.render.show_path(path_dict)

            E = dict()         
            
            # escolhe posicao aleatoria valida para o agente
            while True:
                S = (random.randrange(0, shape[0]), random.randrange(0, shape[1]))
                if self.environment.original_map[S[0]][S[1]] in {self.environment.default_symbols["path"], self.environment.default_symbols["goal"]}:
                    break
            self.environment.setAgentPos(S[0], S[1])

            A = self.get_epsilon_greedy(ec,S)
            A_idx = self.agent.action_idx(A)

            step_count = 0
            while (not self.environment.in_terminal_state()) and (step_count < num_states):

                R = self.environment.move(self.agent, A)
                episode_R.append(R)
                S_prime = (self.agent.y, self.agent.x)
                A_prime = self.get_epsilon_greedy(ec, S_prime)
                A_prime_idx = self.agent.action_idx(A)
                
                pair = (S, A)
                E[pair] = E[pair] + 1 if pair in E.keys() else 1

                delta = R + self.agent.gamma * self.get_Q(S_prime[0], S_prime[1], A_prime_idx) - self.get_Q(S[0], S[1], A_idx)

                for (s, a) in E.keys():
                    a_idx = self.agent.action_idx(a)
                    self.Q[s[0],s[1], a_idx] += alpha * delta * E[(s,a)]
                    E[(s,a)] *= self.agent.gamma * self.lam
                
                S = S_prime
                A = A_prime
                step_count += 1
            self.episode_R.append(episode_R)
            self.episode_length.append(step_count)
            ec-=linear_decay
            rewards.append(np.asarray(self.episode_R[ep]).sum())
            end_time = time.time()
            time_difference_seconds = end_time - start_time
            self.time.append(time_difference_seconds)
            

        self.agent.startPolicy(shape, random_policy)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if(self.environment.original_map[i][j] == '#'): self.agent.policy[i][j] = "wall"
                else: 
                    self.agent.policy[i][j] = max(self.agent.actions, key = lambda action: self.get_Q(i,j, self.agent.action_idx(action)))
        
        end_training_time = time.time()
        print(f"Tempo total de treinamento: {end_training_time - begin_training_time} segundos")
        self.show_loss(rewards, window_size=(len(rewards)//10))

    def path_from(self, starting_point):
        shape = self.environment.get_size()
        max_steps = shape[0] * shape[1]
        step_count = 0
        S = starting_point
        self.environment.setAgentPos(S[0], S[1])
        tuples = []
        while (not self.environment.in_terminal_state()) and (step_count < max_steps):
            A = self.get_greedy_action(S)
            R = self.environment.move(self.agent, A)
            tuples.append((S,A,R))
            S = (self.agent.y, self.agent.x)
            step_count+=1
        return tuples
                

    

class LinearFunctionApproximation(LearningStrategy):
    """
    O metodo se baseia em 10 sensores, 9 deles em volta do agente e um sensor de distancia até o objetivo (cheiro)
    O agente executa eles e segue a política dada pela saída da rede
    
    
    
    """
    def __init__(self) -> None:
        super().__init__()
        # preenche um vetor de 10 pesos aleatórios variando de -1 a 1
        self.W = np.random.rand(10) * 2 - 1

    def forward(self):
        # retorna a aproximação linear para o estado e a ação
        inputs = self.environment.get_sensors(self.agent, 10, ("radius",1,"smell"))
        return np.dot(self.W, inputs)
        

class QLearning(LearningStrategy):
    def __init__(self):
        super().__init__()
        self.episode_R = []
        self.episode_length = []
        self.Q = None
        self.W = np.random.rand(3)
        self.time = []

    def get_Q(self, x, y, action, linear_approximation = False):
        if not linear_approximation:
            return self.Q[x,y,action]
        
        terms = np.array([x,y,action])
        return np.dot(self.W, terms).astype(int)

    def get_greedy_action(self,state):
        return max(self.agent.actions, key = lambda action: self.get_Q(state[0], state[1], self.agent.action_idx(action)))
    
    def get_epsilon_greedy(self, exploration_chance, state):
        if random.random() < exploration_chance:
            return random.choice(self.agent.actions)
        else:
            return max(self.agent.actions, key = lambda action: self.get_Q(state[0], state[1], self.agent.action_idx(action)))
                
    def train(self, episodes, random_policy=True, exploration_chance=0.3, alpha=0.003):
        shape = self.environment.get_size()
        ec = exploration_chance
        num_states = shape[0]*shape[1]
        linear_decay = exploration_chance/episodes
        self.Q = np.zeros((shape[0],shape[1], len(self.agent.actions)))

        for ep in range(episodes):
            start_time = time.time()
            episode_R = []
            if ep % (episodes//10) == 0: 
                print(f"{ep=}")
                path = self.path_from((1,1))
                print('Tamanho do episódio:', len(path))
                print('Recompensa', sum([i[2] for i in path]))
                path_dict = {}
                for s,a,r in path:
                    path_dict[s] = a
                self.environment.render.show_path(path_dict)

            # escolhe posicao aleatoria valida para o agente
            while True:
                S = (random.randrange(0, shape[0]), random.randrange(0, shape[1]))
                if self.environment.original_map[S[0]][S[1]] in {self.environment.default_symbols["path"], self.environment.default_symbols["goal"]}:
                    break
            self.environment.setAgentPos(S[0], S[1])

            #A = random.choice(self.agent.actions)
            step_count = 0
            while (not self.environment.in_terminal_state()) and (step_count < num_states):
                A = self.get_epsilon_greedy(ec,S)
                A_idx = self.agent.action_idx(A)

                R = self.environment.move(self.agent, A)

                episode_R.append(R)

                S_prime = (self.agent.y, self.agent.x)
                A_prime = self.get_greedy_action(S_prime)
                A_prime_idx = self.agent.action_idx(A)


                self.Q[S[0], S[1], A_idx] += alpha*(R + self.agent.gamma * self.get_Q(S_prime[0], S_prime[1], A_prime_idx) - self.get_Q(S[0], S[1], A_idx))

                
                S = S_prime
                step_count += 1
                
            self.episode_R.append(episode_R)
            self.episode_length.append(step_count)
            ec-=linear_decay
            end_time = time.time()
            time_difference_seconds = end_time - start_time
            self.time.append(time_difference_seconds)
            

        self.agent.startPolicy(shape, random_policy)
        self.agent.startV(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                if(self.environment.original_map[i][j] == '#'): self.agent.policy[i][j] = "wall"
                else: 
                    self.agent.policy[i][j] = max(self.agent.actions, key = lambda action: self.get_Q(i,j, self.agent.action_idx(action)))
                    self.agent.book_V[i][j] = max(self.Q[i,j,:])

    def path_from(self, starting_point):
        shape = self.environment.get_size()
        max_steps = shape[0] * shape[1]
        step_count = 0
        S = starting_point
        self.environment.setAgentPos(S[0], S[1])
        tuples = []
        while (not self.environment.in_terminal_state()) and (step_count < max_steps):
            A = self.get_greedy_action(S)
            R = self.environment.move(self.agent, A)
            tuples.append((S,A,R))
            S = (self.agent.y, self.agent.x)
            step_count+=1
        return tuples