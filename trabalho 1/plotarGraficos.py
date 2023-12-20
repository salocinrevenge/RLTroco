import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Matriz que define os quadrados
matriz = []

# le do teclado os caracteres
nLinhas = int(input())

for _ in range(nLinhas):
    matriz.append(list(input().split()))


# Carrega as imagens
baixo = mpimg.imread("imgs/down.png")
cima = mpimg.imread("imgs/up.png")
esquerda = mpimg.imread("imgs/left.png")
direita = mpimg.imread("imgs/right.png")
lava = mpimg.imread("imgs/lava.png")
objetivo = mpimg.imread("imgs/goal.png")

dim = 5
# Plota os quadrados
for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        caractere = matriz[i][j]
        match caractere:
            case "↓":
                imagem =baixo
            case "←":
                imagem =esquerda
            case "→":
                imagem =direita
            case "↑":
                imagem =cima
            case "H":
                imagem =lava
            case "G":
                imagem =objetivo
        plt.imshow(imagem, extent=(j*dim, j*dim + dim, (len(matriz[0])-i-1)*dim, (len(matriz[0])-i-1)*dim + dim))

plt.xlim(0, len(matriz[0])*dim)
plt.ylim(0, len(matriz)*dim)

# Mostra a imagem
plt.show()