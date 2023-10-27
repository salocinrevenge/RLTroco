import Agent
class Environment:
    simbolosPadrao = {"agent": '@', "wall": '#', "path": '.', "goal":'$'}
    def __init__(self, path = None) -> None:
        if path:
            self.mapaOriginal = self.carregarMapa(path)
        self.mapa = self.mapaOriginal.copy()

    def getAgent(self):
        return self.agent


    def carregarMapa(self, path):
        """
        Dado o caminho path, le um arquivo txt e retorna uma matriz
        O txt consiste de uma linha contendo o numero n (número de
        linhas do mapa) e m (número de caracteres diferentes no mapa),
        seguido de m linhas explicando o que sao os caracteres no 
        arquivo e por fim n linhas contendo o mapa que sao caracteres
        """
        mapa = []
        simbolos = dict()
        reforcos = {"agent": 0, "wall": 0, "path": 0, "goal":0}
        with open(path, 'r') as arquivo:
            n, m = map(int, arquivo.readline().split())
            for _ in range(m):
                linha = arquivo.readline().split()
                simbolos[linha[1]] = linha[0]
                reforcos[linha[1]] = int(linha[2])
            for i in range(n):
                linha = arquivo.readline()
                mapa.append([])
                for j in range(len(linha)):
                    char = linha[j]
                    if char == simbolos["agent"]:
                        self.agent = Agent(x=j, y=i, environment=self)
                        char = self.simbolosPadrao["path"]
                    if char != '\n':
                        mapa[-1].append(self.simbolosPadrao[simbolos[char]])
        return mapa