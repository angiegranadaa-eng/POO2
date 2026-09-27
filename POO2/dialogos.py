import pygame
from config import ANCHO_PANTALLA, ALTO_PANTALLA, COLOR_CAJA_DIALOGO, COLOR_BORDE, COLOR_TEXTO

class SistemaDialogo:
    def __init__(self):
        pygame.font.init()
        self.fuente_nombre = pygame.font.SysFont("arial", 20, bold=True)
        self.fuente_texto = pygame.font.SysFont("arial", 16)
        self.cientifica_actual = None
        self.activo = False

        self.ancho = ANCHO_PANTALLA - 80
        self.alto = 140
        self.rect = pygame.Rect(40, ALTO_PANTALLA - 160, self.ancho, self.alto)

    def abrir(self, cientifica):
        self.cientifica_actual = cientifica
        self.activo = True

    def cerrar(self):
        self.activo = False
        self.cientifica_actual = None

    def _dividir_texto(self, texto, ancho_maximo):
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()
            if self.fuente_texto.size(prueba)[0] <= ancho_maximo:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)
        return lineas

    def dibujar(self, superficie):
        if not self.activo or not self.cientifica_actual:
            return

        # Dibujar caja de diálogo
        pygame.draw.rect(superficie, COLOR_CAJA_DIALOGO, self.rect, border_radius=12)
        pygame.draw.rect(superficie, COLOR_BORDE, self.rect, width=3, border_radius=12)

        # Nombre y área científica
        encabezado = f"{self.cientifica_actual.nombre} ({self.cientifica_actual.rama})"
        surf_nombre = self.fuente_nombre.render(encabezado, True, COLOR_BORDE)
        superficie.blit(surf_nombre, (self.rect.x + 20, self.rect.y + 15))

        # Texto dividido en líneas
        lineas = self._dividir_texto(self.cientifica_actual.dialogo, self.ancho - 40)
        y_offset = self.rect.y + 50
        for linea in lineas:
            surf_linea = self.fuente_texto.render(linea, True, COLOR_TEXTO)
            superficie.blit(surf_linea, (self.rect.x + 20, y_offset))
            y_offset += 24

        # Indicador de cierre
        surf_pista = self.fuente_texto.render("[Presiona ESPACIO o E para cerrar]", True, (150, 150, 150))
        superficie.blit(surf_pista, (self.rect.x + self.ancho - surf_pista.get_width() - 20, self.rect.y + self.alto - 30))
