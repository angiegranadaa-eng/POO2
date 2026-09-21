class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5

    def mover(self, teclas):
        if teclas["izquierda"]:
            self.x -= self.velocidad
        if teclas["derecha"]:
            self.x += self.velocidad