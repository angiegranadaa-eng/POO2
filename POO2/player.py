import pygame
from config import ANCHO_PANTALLA, ALTO_PANTALLA, COLOR_JUGADOR, COLOR_BALA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA

# --- CLASE AUXILIAR: GESTOR DE HOJAS DE SPRITES ---
# Se encarga de cargar y cortar la imagen completa en fotogramas individuales.
class SpriteSheet:
    def __init__(self, filename):
        try:
            # Cargamos la imagen una sola vez
            self.sheet = pygame.image.load(filename).convert_alpha()
        except (FileNotFoundError, pygame.error):
            print(f"Error: No se pudo cargar la hoja de sprites: {filename}")
            self.sheet = None

    def obtener_fotogramas(self, x, y, ancho, alto, count, escala=1):
        """Corta múltiples fotogramas secuenciales en una fila y los escala."""
        if not self.sheet: return [] # Retornamos lista vacía si no hay hoja

        fotogramas = []
        for i in range(count):
            # Calculamos las coordenadas exactas del cuadro
            rect_hoja = pygame.Rect(x + (i * ancho), y, ancho, alto)

            # Creamos una superficie transparente para el fotograma
            surface = pygame.Surface((ancho, alto)).convert_alpha()
            #surface.fill((0, 0, 0, 0)) # Opcional: limpiar con transparente

            # Copiamos el fragmento de la hoja en la superficie
            surface.blit(self.sheet, (0, 0), rect_hoja)

            # Escalamos la imagen si es necesario
            if escala != 1:
                surface = pygame.transform.scale(surface, (int(ancho * escala), int(alto * escala)))

            # Guardamos el fotograma nítido
            fotogramas.append(surface)

        return fotogramas


# --- CLASE: GESTOR DE ESTADOS DE PERSONAJE ---
# Define qué animación se reproduce según las acciones del personaje.
class PlayerState:
    # Constantes para los estados
    IDLE = "idle"
    WALK_FRONT = "walk_front"
    WALK_SIDE = "walk_side"
    ATTACK = "attack"
    DEATH = "death"

    def __init__(self, spritesheet, escala=1.6):
        # Diccionario que almacena las listas de fotogramas para cada animación
        self.animaciones = {
            self.IDLE: spritesheet.obtener_fotogramas(0, 0 * ALTO_CUADRO_MAGA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA, 4, escala),
            self.WALK_FRONT: spritesheet.obtener_fotogramas(0, 1 * ALTO_CUADRO_MAGA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA, 4, escala),
            self.WALK_SIDE: spritesheet.obtener_fotogramas(0, 2 * ALTO_CUADRO_MAGA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA, 4, escala),
            # El ataque es secuencial, solo tomamos un fotograma por ahora
            self.ATTACK: [spritesheet.obtener_fotogramas(0, 3 * ALTO_CUADRO_MAGA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA, 1, escala)[0]],
            self.DEATH: [spritesheet.obtener_fotogramas(3 * ANCHO_CUADRO_MAGA, 3 * ALTO_CUADRO_MAGA, ANCHO_CUADRO_MAGA, ALTO_CUADRO_MAGA, 1, escala)[0]]
        }

        self.current_state = self.IDLE # Estado por defecto
        self.flipped_side = False      # Bandera para girar el sprite lateral

    def get_active_animation(self):
        """Retorna la lista de fotogramas de la animación activa."""
        return self.animaciones[self.current_state]

    def get_current_frame(self, index):
        """Retorna el fotograma actual, aplicándole espejo si está girado."""
        anim = self.get_active_animation()
        if not anim: return None # Debería haber una imagen de respaldo

        frame = anim[index % len(anim)]

        # Volteamos la imagen lateralmente si vamos a la izquierda
        if self.current_state == self.WALK_SIDE and self.flipped_side:
            return pygame.transform.flip(frame, True, False) # Voltear horizontal

        return frame

    def set_state(self, new_state, flipped=False):
        """Cambia el estado y la bandera de volteado."""
        if self.current_state != new_state:
            self.current_state = new_state
            # Reiniciar otros valores si es necesario
        self.flipped_side = flipped


# --- CLASE PRINCIPAL: JUGADOR (HEREDA DE PYGAME.SPRITE) ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Inicializamos la clase padre
        super().__init__()

        self.escala = 1.6 # Cuánto más grande se verá
        self.spritesheet = SpriteSheet("jugador_maga.png")

        # Si no hay hoja, salimos para evitar errores
        if not self.spritesheet.sheet:
            self.image = pygame.Surface((32*self.escala, 48*self.escala)).convert_alpha()
            self.image.fill(COLOR_JUGADOR)
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.alive = False
            return

        self.alive = True

        # Instanciamos el gestor de estados
        self.state = PlayerState(self.spritesheet, self.escala)

        # --- Configuración obligatoria para pygame.sprite.Sprite ---
        # self.image es la imagen visible actual
        self.image = self.state.get_current_frame(0)
        # self.rect es el rectángulo de colisión y posición
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # --- Variables de movimiento ---
        self.velocidad = 6
        self.balas = pygame.sprite.Group() # Grupo de sprites para las balas
        self.cooldown_disparo = 0
        self.salud = 100

        # --- Variables de control de animación ---
        self.frame_index = 0             # Fotograma actual
        self.update_timer = 0             # Temporizador de animación
        self.frame_cooldown = 10         # Velocidad (cuántos FPS antes de cambiar de fotograma)

    def manejar_entradas(self, teclas):
        if not self.alive: return

        dx, dy = 0, 0

        # Bandera para voltear lateralmente
        flipped = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= self.velocidad
            flipped = True # Volteamos si vamos a la izquierda
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += self.velocidad

        se_movio = (dx != 0 or dy != 0)

        # --- Actualización de Estados Profesionales ---
        # Decidimos qué animación usar basado en el movimiento y dx
        if se_movio:
            if dx != 0:
                # Caminata Lateral (volteada si dx < 0)
                self.state.set_state(PlayerState.WALK_SIDE, flipped)
            else:
                # Caminata Frente (sin voltear)
                self.state.set_state(PlayerState.WALK_FRONT, False)
        else:
            # Idle (sin voltear)
            self.state.set_state(PlayerState.IDLE, False)

        # Mover y limitar a la pantalla
        self.rect.x = max(0, min(self.rect.x + dx, ANCHO_PANTALLA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, ALTO_PANTALLA - self.rect.height))

        if self.cooldown_disparo > 0:
            self.cooldown_disparo -= 1

    def disparar(self):
        if self.cooldown_disparo == 0 and self.alive:
            self.balas.add(Bala(self.rect.centerx, self.rect.top))
            self.cooldown_disparo = 10

    def actualizar_balas(self):
        # El grupo de balas se actualiza solo
        self.balas.update()

    def update(self):
        """Actualiza el fotograma de animación (llamada automática)."""
        if not self.alive: return

        # Lógica de actualización de animación (frame rate)
        # Solo animamos el IDLE y los WALKS (el ataque es estático por ahora)
        if self.state.current_state in (PlayerState.IDLE, PlayerState.WALK_FRONT, PlayerState.WALK_SIDE):
            anim = self.state.get_active_animation()
            if anim and len(anim) > 1:
                self.update_timer += 1
                if self.update_timer >= self.frame_cooldown:
                    self.frame_index = (self.frame_index + 1) % len(anim)
                    # Actualizamos self.image (lo que Pygame dibuja)
                    self.image = self.state.get_current_frame(self.frame_index)
                    self.update_timer = 0
            else:
                # Asegurar que mostramos el fotograma de ataque/muerte
                self.image = self.state.get_current_frame(0)
        else:
             self.image = self.state.get_current_frame(0)

    def dibujar(self, superficie):
        # El dibujo se maneja automáticamente por el grupo de sprites,
        # pero mantendremos este método por si acaso para las balas.
        for bala in self.balas:
            bala.dibujar(superficie)

        # superficie.blit(self.image, self.rect) # Este se maneja en main.py


# --- CLASE AUXILIAR: BALA (TAMBIÉN HEREDA DE SPRITE) ---
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 18)).convert_alpha()
        self.image.fill(COLOR_BALA)
        pygame.draw.rect(self.image, COLOR_BALA, self.image.get_rect(), border_radius=3)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.velocidad = 12

    def update(self):
        """Mueve la bala y se elimina si sale de pantalla."""
        self.rect.y -= self.velocidad
        if self.rect.bottom < 0:
            self.kill() # Elimina de todos los grupos automáticamente

    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)
