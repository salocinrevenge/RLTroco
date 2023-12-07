import pygame
from threading import Thread
import numpy as np
import matplotlib.pyplot as plt

class Renderer():
    def __init__(self, chief, content, title=None, dimensions=(800, 800)):
        self.chief = chief
        self.content = content
        self.contents = [content] # para trocar entre janelas
        self.iConteudoAtual = 0 # para marcar qual o atual dentre os varios
        self.title = title
        self.dimensions = dimensions
        self.running = True
        if not self.title:
            self.title = type(chief).__name__   # title é o nome da classe
        
        
        # redimensiona o ambiente para caber na tela
        self.tamanhosprite = 64
        self.escala = (self.dimensions[0]/len(self.content[0]), self.dimensions[1]/len(self.content))
        while self.escala[0] < self.tamanhosprite//8 or self.escala[1] < self.tamanhosprite//8: # redimensiona pra pp
            self.dimensions =(int(self.dimensions[0] *1.1), int(self.dimensions[1]*1.1))
            self.escala = (self.dimensions[0]/len(self.content[0]), self.dimensions[1]/len(self.content))

        self.load_sprites()

        # cria uma thread que roda o pygame
        displayer = Thread(target=self.show) # shower = mostrador

        # Inicia a thread
        displayer.start()

    def addConteudo(self,conteudo):
        self.contents.append(conteudo)

    def desligar(self):
        self.running = False

    def load_sprites(self):
        self.sprites = dict()
        self.sprites["path"] = pygame.transform.scale(pygame.image.load("imgs/path.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["wall"] = pygame.transform.scale(pygame.image.load("imgs/wall.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["goal"] = pygame.transform.scale(pygame.image.load("imgs/goal.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["agent"] = pygame.transform.scale(pygame.image.load("imgs/agent.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["right"] = pygame.transform.scale(pygame.image.load("imgs/right.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["up"] = pygame.transform.scale(pygame.image.load("imgs/up.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["left"] = pygame.transform.scale(pygame.image.load("imgs/left.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["down"] = pygame.transform.scale(pygame.image.load("imgs/down.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["acid"] = pygame.transform.scale(pygame.image.load("imgs/acid.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["lava"] = pygame.transform.scale(pygame.image.load("imgs/lava.png"), (int(self.escala[0]), int(self.escala[1])))

        self.asciiSprites = dict()
        self.asciiSprites["path"]   = '⬛'
        self.asciiSprites["wall"]   = '🧱'
        self.asciiSprites["goal"]   = '⚽'
        self.asciiSprites["agent"]  = '👾' 
        self.asciiSprites["right"]  = '->' #'➡️'
        self.asciiSprites["up"]     = '⬆️⬆️'
        self.asciiSprites["left"]   = '<-' 
        self.asciiSprites["down"]   = '⬇️⬇️'
        self.asciiSprites["lava"]   = '🌋'
        self.asciiSprites["acid"]   = '🦠'

    def create_heatmap(data, cmap='viridis', title='Heatmap'):
        """
        Create a heatmap from a list of lists of floats.

        Parameters:
        - data: List of lists of floats representing the heatmap data.
        - cmap: Colormap for the heatmap (default is 'viridis').
        - title: Title for the heatmap (default is 'Heatmap').
        """
        data = np.array(data, dtype=float)

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Display the heatmap using imshow
        im = ax.imshow(data, cmap=cmap)

        # Add a colorbar to the right of the heatmap
        cbar = ax.figure.colorbar(im, ax=ax)

        # Set the title
        ax.set_title(title)

        # Show the plot
        plt.show()

    def showAscii(self):
        for i in range(len(self.content)):
            for j in range(len(self.content[0])):
                cell = self.content[i][j]
                # se o content de cell estiver no dicionario de sprites
                if cell in self.asciiSprites:
                    obj = cell
                else:
                    obj = self.chief.symbols[cell]
                print(self.asciiSprites.get(obj,'❌'),end='')
            print('')

    def show(self):
        # renderiza o ambiente
        pygame.init()
        self.screen = pygame.display.set_mode(self.dimensions)
        pygame.display.set_caption(self.title)
        self.screen.fill((0, 0, 0))

        while self.running:
            pygame.time.delay(10)  # delay de 10ms
            # Botao de fechar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                # se apertar "p"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.iConteudoAtual = 1
                        self.content = self.contents[self.iConteudoAtual]

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.iConteudoAtual = 0
                        self.content = self.contents[self.iConteudoAtual]

            # limpa a tela
            self.screen.fill((0,0,0))
            
            # desenha o conteudo
            for k in range(self.iConteudoAtual+1):
                for i in range(len(self.contents[k])):
                    for j in range(len(self.contents[k][0])):
                        celula = self.contents[k][i][j]
                        # se o conteudo de celula estiver no dicionario de sprites
                        if celula in self.sprites:
                            objeto = celula
                        else:
                            objeto = self.chief.symbols[celula]
                        self.screen.blit(self.sprites[objeto], (j*self.escala[0], i*self.escala[1]))

            # Atualizar a tela
            pygame.display.update()


    def show_path(self, path):
        for i in range(len(self.content)):
            for j in range(len(self.content[0])):
                cell = self.content[i][j]
                if((i,j) in path.keys()):
                    cell = path[(i,j)]
                # se o content de cell estiver no dicionario de sprites
                if cell in self.asciiSprites:
                    obj = cell
                else:
                    obj = self.chief.symbols[cell]
                print(self.asciiSprites.get(obj,'❌'),end='')
            print('')
        
