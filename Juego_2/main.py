# main.py - Space War optimizado tomando ideas de Juego_1
import pygame
import random
print(">>> MAIN EJECUTADO DESDE:", __file__)

from settings import *
from funciones import *
from utils import monitor_usage   # monitor de CPU/GPU

# ============================================================
# INICIALIZACIÓN
# ============================================================
pygame.init()

# Intentar iniciar el audio, pero no morir si no hay dispositivo (WSL, etc.)
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
    AUDIO_AVAILABLE = False

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()
FPS = 60

# ============================================================
# CARGAR RECURSOS
# ============================================================
# Imágenes de meteoritos
meteor_images = []
meteor_list_files = [
    "Meteorito1.png", "Meteorito3.png", "Meteorito4.png",
    "Meteorito5.png", "Meteorito6.png", "Meteorito7.png",
    "Meteorito2.png", "Ovni.png"
]

for img in meteor_list_files:
    try:
        meteor_img = pygame.image.load(ruta('Textturas', img)).convert()
        meteor_img.set_colorkey(BLACK)
        meteor_images.append(meteor_img)
    except pygame.error as e:
        print(f"Error cargando {img}: {e}")

# Fondo
try:
    background = pygame.image.load(ruta('Textturas', 'Fondo2.png')).convert()
except pygame.error as e:
    print(f"Error cargando fondo: {e}")
    # En caso de fallo, fondo negro
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)

# Sonidos
laser_sound = None
explosion_sound = None

if AUDIO_AVAILABLE:
    try:
        laser_sound = pygame.mixer.Sound(ruta('Sounds', 'Lasersound.ogg'))
        explosion_sound = pygame.mixer.Sound(ruta('Sounds', 'Explosion.wav'))
    except pygame.error as e:
        print(f"Error cargando sonidos: {e}")

# Música de fondo opcional
if AUDIO_AVAILABLE:
    try:
        pygame.mixer.music.load(ruta('Sounds', 'Playersong.ogg'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # loop infinito
    except pygame.error:
        pass

# ============================================================
# FUNCIÓN PARA REINICIAR PARTIDA
# ============================================================
def new_game():
    """Crea todos los sprites y devuelve (all_sprites, meteor_list, lasers, player, score)."""
    all_sprites = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    player = Player(laser_sound)
    player.all_sprites = all_sprites
    player.lasers = lasers
    all_sprites.add(player)

    # Crear meteoritos iniciales
    for _ in range(9):
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    score = 0
    return all_sprites, meteor_list, lasers, player, score


# ============================================================
# VARIABLES DEL JUEGO
# ============================================================
score = 0
game_over = True
running = True
first_run = True   # para mostrar pantalla de inicio solo la primera vez

# ============================================================
# LOOP PRINCIPAL
# ============================================================
while running:

    if game_over:
        # Pantalla de inicio solo la primera vez
        if first_run:
            if not show_start_screen(screen, clock, background):
                break
            first_run = False

        all_sprites, meteor_list, lasers, player, score = new_game()
        game_over = False

    clock.tick(FPS)
    monitor_usage()   # imprime uso CPU/GPU cada 0.5 s

    # ---- EVENTOS ----
    for event in pygame.event.get():
        # Cerrar ventana con la X
        if event.type == pygame.QUIT:
            running = False

        # Tecla presionada
        elif event.type == pygame.KEYDOWN:
            # Disparar con ESPACIO o W
            if event.key in (pygame.K_SPACE, pygame.K_w):
                player.shoot()
            # Salir solo con ESC
            elif event.key == pygame.K_ESCAPE:
                running = False

        # ---- ACTUALIZAR ----
    all_sprites.update()

    # ---- CONTROLES POR TECLADO (continuos) ----
    keys = pygame.key.get_pressed()

    # DEBUG: ver si Pygame detecta las teclas
    if keys[pygame.K_a]:
        print("A PRESIONADA")
    if keys[pygame.K_SPACE]:
        print("SPACE PRESIONADA")
    if keys[pygame.K_w]:
        print("W PRESIONADA")

    # Disparar con ESPACIO o W
    if keys[pygame.K_SPACE] or keys[pygame.K_w]:
        player.shoot()

    # Salir con ESC
    if keys[pygame.K_ESCAPE]:
        running = False



    # ---- COLISIONES (Meteorito-Laser) ----
    hits = pygame.sprite.groupcollide(meteor_list, lasers, True, True)
    for _ in hits:
        score += 5
        if explosion_sound and AUDIO_AVAILABLE:
            try:
                explosion_sound.play()
            except Exception:
                pass
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # ---- COLISIONES (Meteorito-Jugador) ----
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for _ in hits:
        player.shield -= 25
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    # ---- DIBUJAR ----
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 40, SCREEN_WIDTH // 2, 5)

    # Barra de escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()
