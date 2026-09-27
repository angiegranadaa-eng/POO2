import sys
import random
import pygame

from config import (
    ANCHO_PANTALLA, ALTO_PANTALLA, FPS, TITULO_JUEGO,
    COLOR_FONDO, COLOR_BORDE, COLOR_TEXTO,
    ESTADO_MENU, ESTADO_JUEGO, ESTADO_VICTORIA, ESTADO_GAMEOVER,
    PUNTOS_OBJETIVO
)
from player import Jugador
from enemigos import Enemigo

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(TITULO_JUEGO)
    reloj = pygame.time.Clock()

    # Cargar fondo del calabozo
    try:
        fondo_img = pygame.image.load("fondo_inicio.png").convert()
        fondo_img = pygame.transform.scale(fondo_img, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except FileNotFoundError:
        fondo_img = None

    jugador = Jugador(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 100)
    enemigos = []
    puntuacion = 0
    estado = ESTADO_MENU

    fuente_titulo = pygame.font.SysFont("arial", 36, bold=True)
    fuente_hud = pygame.font.SysFont("arial", 22, bold=True)

    timer_enemigos = 0

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        # --- 1. EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if estado == ESTADO_MENU and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    estado = ESTADO_JUEGO
                    puntuacion = 0
                    jugador.salud = 100
                    enemigos.clear()

                elif estado in (ESTADO_VICTORIA, ESTADO_GAMEOVER) and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    estado = ESTADO_MENU

        # --- 2. LÓGICA DEL JUEGO ---
        teclas = pygame.key.get_pressed()

        if estado == ESTADO_JUEGO:
            jugador.manejar_entradas(teclas)

            # Disparo con ESPACIO o tecla J
            if teclas[pygame.K_SPACE] or teclas[pygame.K_j]:
                jugador.disparar()

            jugador.actualizar_balas()

            # Generar enemigos periódicamente
            timer_enemigos += 1
            if timer_enemigos >= 25:
                enemigos.append(Enemigo())
                timer_enemigos = 0

            # Actualizar enemigos y colisiones
            for enemigo in enemigos[:]:
                enemigo.actualizar()

                # Colisión de Bala con Enemigo
                for bala in jugador.balas[:]:
                    if enemigo.rect.colliderect(bala.rect):
                        if bala in jugador.balas:
                            jugador.balas.remove(bala)
                        if enemigo in enemigos:
                            enemigos.remove(enemigo)
                        puntuacion += 100
                        break

                # Colisión de Enemigo con Jugador
                if enemigo.rect.colliderect(jugador.rect):
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                    jugador.salud -= 20
                    if jugador.salud <= 0:
                        estado = ESTADO_GAMEOVER

                # Enemigo escapó por abajo
                elif enemigo.rect.top > ALTO_PANTALLA:
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)

            # Condición de Victoria (Alcanzar 1000 Puntos)
            if puntuacion >= PUNTOS_OBJETIVO:
                estado = ESTADO_VICTORIA

        # --- 3. DIBUJADO EN PANTALLA ---
        pantalla.fill(COLOR_FONDO)

        if estado == ESTADO_MENU:
            if fondo_img:
                pantalla.blit(fondo_img, (0, 0))
            txt = fuente_titulo.render("Presiona [ENTER] para iniciar el Calabozo", True, COLOR_BORDE)
            pantalla.blit(txt, (ANCHO_PANTALLA // 2 - txt.get_width() // 2, ALTO_PANTALLA - 80))

        elif estado == ESTADO_JUEGO:
            if fondo_img:
                # Dibujamos el fondo con cierta transparencia para ambiente
                pantalla.blit(fondo_img, (0, 0))

            jugador.dibujar(pantalla)
            for enemigo in enemigos:
                enemigo.dibujar(pantalla)

            # Interfaz de Usuario (HUD)
            txt_pts = fuente_hud.render(f"PUNTOS: {puntuacion} / {PUNTOS_OBJETIVO}", True, COLOR_BORDE)
            txt_salud = fuente_hud.render(f"SALUD: {jugador.salud}%", True, COLOR_TEXTO)
            pantalla.blit(txt_pts, (30, 20))
            pantalla.blit(txt_salud, (30, 50))

        elif estado == ESTADO_VICTORIA:
            txt_vic = fuente_titulo.render("¡NIVEL COMPLETADO! Alcanzaste 1000 Puntos", True, COLOR_BORDE)
            txt_sub = fuente_hud.render("Presiona [ENTER] para volver al Menú", True, COLOR_TEXTO)
            pantalla.blit(txt_vic, (ANCHO_PANTALLA // 2 - txt_vic.get_width() // 2, ALTO_PANTALLA // 2 - 40))
            pantalla.blit(txt_sub, (ANCHO_PANTALLA // 2 - txt_sub.get_width() // 2, ALTO_PANTALLA // 2 + 20))

        elif estado == ESTADO_GAMEOVER:
            txt_go = fuente_titulo.render("¡GAME OVER! Perdiste toda tu salud", True, COLOR_BORDE)
            txt_sub = fuente_hud.render("Presiona [ENTER] para intentar de nuevo", True, COLOR_TEXTO)
            pantalla.blit(txt_go, (ANCHO_PANTALLA // 2 - txt_go.get_width() // 2, ALTO_PANTALLA // 2 - 40))
            pantalla.blit(txt_sub, (ANCHO_PANTALLA // 2 - txt_sub.get_width() // 2, ALTO_PANTALLA // 2 + 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
