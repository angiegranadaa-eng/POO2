import pygame
# Importamos lo que creamos en las otras pestañas (archivos)
from config import ANCHO_PANTALLA, ALTO_PANTALLA, FPS, COLOR_FONDO
from player import Jugador
from cientificas import lista_cientificas

def iniciar_juego():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    reloj = pygame.time.Clock()
    
    jugador = Jugador(100, 200)
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                
        pantalla.fill(COLOR_FONDO)
        
        # Aquí dibujarías al jugador y a las científicas usando las otras pestañas...
        
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    iniciar_juego()