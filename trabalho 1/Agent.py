class Agente():
    def __init__(self, x=None, y = None, environment = None) -> None:
        if environment:
            self.environment = environment
        if x:
            self.x = x
        if y:
            self.y = y
    def setEnvironment(self, environment):
        self.environment = environment
    
    def setPos(self, x, y):
        self.x = x
        self.y = y