import pygame
import math
from config import COLOR_CIENTIFICA, COLOR_BORDE

class Cientifica:
    def __init__(self, nombre, rama, dialogo, x, y):
        self.nombre = nombre
        self.rama = rama
        self.dialogo = dialogo
        self.rect = pygame.Rect(x, y, 32, 32)

    def cerca_de_jugador(self, jugador_rect, distancia_maxima=50):
        c_centro = self.rect.center
        j_centro = jugador_rect.center
        distancia = math.hypot(c_centro[0] - j_centro[0], c_centro[1] - j_centro[1])
        return distancia <= distancia_maxima

    def dibujar(self, superficie, cerca=False):
        pygame.draw.rect(superficie, COLOR_CIENTIFICA, self.rect, border_radius=6)
        if cerca:
            pygame.draw.rect(superficie, COLOR_BORDE, self.rect.inflate(8, 8), 2, border_radius=8)

def cargar_cientificas():
    return [
        Cientifica(
            nombre="Ada Lovelace",
            rama="Matemática e Informática",
            dialogo="¡Hola! Creé el primer algoritmo pensado para ser procesado por una máquina. ¡Bienvenida a Pixel Pioneers!",
            x=250, y=200
        ),
        Cientifica(
            nombre="Marie Curie",
            rama="Física y Química",
            dialogo="¡Gusto en conocerte! Fui la primera persona en recibir dos Premios Nobel en distintas ciencias.",
            x=550, y=200
        ),
        Cientifica(
            nombre="Rosalind Franklin",
            rama="Biofísica y Cristalografía",
            dialogo="¡Hola! Con la famosa 'Fotografía 51' logré capturar la estructura de doble hélice del ADN.",
            x=400, y=420
        )
    ]
