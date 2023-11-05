from Professor import Professor

if __name__ == '__main__':
    sala = input("Digite o numero da sala: ")
    professor = Professor(caminhoSala=f"sala{sala}.txt", learningStrategy="Monte Carlo", nEpisodios=10000, chanceExploracao = 0.3)
