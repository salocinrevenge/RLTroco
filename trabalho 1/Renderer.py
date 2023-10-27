import pygame
from threading import Thread

class Renderer():
    def __init__(self, chefe, conteudo, titulo=None, dimensoes=(800, 800)):
        self.chefe = chefe
        self.conteudo = conteudo
        self.titulo = titulo
        self.dimensoes = dimensoes
        self.running = True
        if not self.titulo:
            self.titulo = type(chefe).__name__   # titulo é o nome da classe
        
        # cria uma thread que roda o pygame
        mostrador = Thread(target=self.mostrar)

        # Inicia a thread
        mostrador.start()

    def desligar(self):
        self.running = False

    def mostrar(self):
        # renderiza o ambiente
        pygame.init()
        self.screen = pygame.display.set_mode(self.dimensoes)
        pygame.display.set_caption(self.titulo)
        self.screen.fill((255, 255, 255))

        while self.running:
            # Botao de fechar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
            # limpa a tela
            self.screen.fill((0,0,0))
            
            # desenha o conteudo

            # Atualizar a tela
            pygame.display.update()
# se main
if __name__ == '__main__':
    Renderer(None, None)
        
