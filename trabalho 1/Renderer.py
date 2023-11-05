import pygame
from threading import Thread
import time

class Renderer():
    def __init__(self, chefe, conteudo, titulo=None, dimensoes=(800, 800), visual = True):
        self.visual = visual
        self.chefe = chefe
        self.conteudo = conteudo
        self.conteudos = [conteudo] # para trocar entre janelas
        self.iConteudoAtual = 0 # para marcar qual o atual dentre os varios
        self.titulo = titulo
        self.dimensoes = dimensoes
        self.running = True
        if not self.titulo:
            self.titulo = type(chefe).__name__   # titulo é o nome da classe
        
        self.tamanhosprite = 64
        self.escala = (self.dimensoes[0]/len(self.conteudo[0]), self.dimensoes[1]/len(self.conteudo))
        while self.escala[0] < self.tamanhosprite//8 or self.escala[1] < self.tamanhosprite//8: # redimensiona pra pp
            self.dimensoes =(int(self.dimensoes[0] *1.1), int(self.dimensoes[1]*1.1))
            self.escala = (self.dimensoes[0]/len(self.conteudo[0]), self.dimensoes[1]/len(self.conteudo))

        if visual:
            self.carregarSprites()

        # cria uma thread que roda o pygame
        mostrador = Thread(target=self.mostrar)

        # Inicia a thread
        mostrador.start()

    def addConteudo(self,conteudo):
        self.conteudos.append(conteudo)

    def desligar(self):
        self.running = False

    def carregarSprites(self):
        self.sprites = dict()
        self.sprites["path"] = pygame.transform.scale(pygame.image.load("imgs/path.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["wall"] = pygame.transform.scale(pygame.image.load("imgs/wall.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["goal"] = pygame.transform.scale(pygame.image.load("imgs/goal.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["agent"] = pygame.transform.scale(pygame.image.load("imgs/agent.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["right"] = pygame.transform.scale(pygame.image.load("imgs/right.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["up"] = pygame.transform.scale(pygame.image.load("imgs/up.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["left"] = pygame.transform.scale(pygame.image.load("imgs/left.png"), (int(self.escala[0]), int(self.escala[1])))
        self.sprites["down"] = pygame.transform.scale(pygame.image.load("imgs/down.png"), (int(self.escala[0]), int(self.escala[1])))


    def mostrar(self):
        # renderiza o ambiente
        if self.visual:
            pygame.init()
            self.screen = pygame.display.set_mode(self.dimensoes)
            pygame.display.set_caption(self.titulo)
            self.screen.fill((0, 0, 0))

        if self.visual:
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
                            self.conteudo = self.conteudos[self.iConteudoAtual]

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_p:
                            self.iConteudoAtual = 0
                            self.conteudo = self.conteudos[self.iConteudoAtual]

                # limpa a tela
                self.screen.fill((0,0,0))
                
                # desenha o conteudo
                for i in range(len(self.conteudo)):
                    for j in range(len(self.conteudo[0])):
                        celula = self.conteudo[i][j]
                        # se o conteudo de celula estiver no dicionario de sprites
                        if celula in self.sprites:
                            objeto = celula
                        else:
                            objeto = self.chefe.simbolos[celula]
                        self.screen.blit(self.sprites[objeto], (j*self.escala[0], i*self.escala[1]))

                # Atualizar a tela
                pygame.display.update()
        else:
            print(self.conteudo)
            time.sleep(10)

        
