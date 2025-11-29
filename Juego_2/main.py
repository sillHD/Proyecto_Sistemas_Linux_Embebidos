# main.py
import pygame
import random
from settings import *
from funciones import *

# ============================================================
# INICIALIZACIÓN
# ============================================================
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()
FPS = 60

# ============================================================
# CARGAR RECURSOS
# ============================================================
# Imágenes de meteoritos
meteor_images = []
meteor_list_files = ["Meteorito1.png", "Meteorito3.png", "Meteorito4.png",
                     "Meteorito5.png", "Meteorito6.png", "Meteorito7.png",
                     "Meteorito2.png", "Ovni.png"]

for img in meteor_list_files:
    try:
        meteor_images.append(pygame.image.load(ruta('Textturas', img)).convert())
    except pygame.error as e:
        print(f"Error cargando {img}: {e}")

# Fondo
try:
    background = pygame.image.load(ruta('Textturas', 'Fondo2.png')).convert()
except pygame.error as e:
    print(f"Error cargando fondo: {e}")

# Sonidos
laser_sound = None
explosion_sound = None
try:
    laser_sound = pygame.mixer.Sound(ruta('Sounds', 'Lasersound.ogg'))
    explosion_sound = pygame.mixer.Sound(ruta('Sounds', 'Explosion.wav'))
except pygame.error as e:
    print(f"Error cargando sonidos: {e}")

# ============================================================
# GRUPO DE SPRITES
# ============================================================
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
lasers = pygame.sprite.Group()

player = Player(laser_sound)
player.all_sprites = all_sprites
player.lasers = lasers
all_sprites.add(player)

# ============================================================
# VARIABLES DEL JUEGO
# ============================================================
score = 0
game_over = True
running = True

# ============================================================
# LOOP PRINCIPAL
# ============================================================
while running:
    if game_over:
        # Pantalla de inicio
        show_start_screen(screen, clock, background)
        
        # Reiniciar sprites
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        lasers = pygame.sprite.Group()
        
        player = Player(laser_sound)
        player.all_sprites = all_sprites
        player.lasers = lasers
        all_sprites.add(player)
        
        # Crear meteoritos iniciales
        for i in range(9):
            meteor = Meteor(meteor_images)
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        
        score = 0
        game_over = False

    clock.tick(FPS)

    # ---- EVENTOS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Disparar con ESPACIO
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False

    # ---- ACTUALIZAR ----
    all_sprites.update()

    # ---- COLISIONES (Meteorito-Laser) ----
    hit = pygame.sprite.groupcollide(meteor_list, lasers, True, True)
    for hits in hit:
        score += 5
        if explosion_sound:
            try:
                explosion_sound.play()
            except:
                pass
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # ---- COLISIONES (Meteorito-Jugador) ----
    hit = pygame.sprite.spritecollide(player, meteor_list, True)
    for hits in hit:
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
