# main.py
import pygame
from settings import *
from funciones import walking_animation, jumping_animation
from utils import monitor_usage, gpu_usage
import random
import time
import psutil
import math

# --- Inicialización ---
pygame.init()

# Resolución interna del juego
GAME_WIDTH, GAME_HEIGHT = 1280, 720
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# Pantalla full-screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

reloj = pygame.time.Clock()
FPS = 30

# --- Carga de imágenes ---
menu = pygame.image.load(ruta("texturas", "menu.png")).convert_alpha()
fondo = pygame.image.load(ruta("texturas", "background.png")).convert()
stayR = pygame.image.load(ruta("texturas", "stay_right.png")).convert_alpha()
stayL = pygame.image.load(ruta("texturas", "stay_left.png")).convert_alpha()
icono = pygame.image.load(ruta("texturas", "icono.png")).convert_alpha()
icono.set_colorkey(NEGRO)
pygame.display.set_icon(icono)

# Nubes
clouds = [pygame.image.load(ruta("texturas", "clouds", f"c{i}.png")).convert_alpha() for i in range(1,4)]
for c in clouds: c.set_colorkey(NEGRO)

# Enemigos y jugador
enemy_right = [pygame.image.load(ruta("texturas", "enemy", "right", f"e_r{i}.png")).convert_alpha() for i in range(1,4)]
enemy_left = [pygame.image.load(ruta("texturas", "enemy", "left", f"e_l{i}.png")).convert_alpha() for i in range(1,4)]
walk_right = [pygame.image.load(ruta("texturas", "walk", "right", f"run_r{i}.png")).convert_alpha() for i in range(1,9)]
walk_left = [pygame.image.load(ruta("texturas", "walk", "left", f"run_l{i}.png")).convert_alpha() for i in range(1,9)]
jump_right = [pygame.image.load(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png")).convert_alpha() for i in range(1,9)]
jump_left = [pygame.image.load(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png")).convert_alpha() for i in range(1,9)]

# --- Datos iniciales ---
pn_x, pn_y = 640, 0
vn_x, velocidad = 0, 5
angulo, direccion = 0.0, -1
frame_counter, control = 0, 0
pr_x1, pr_x2, pr_x3, pr_x4 = 800, 220, 340, 542
pr_y = 100
vr_x1, vr_x2, vr_x3, vr_x4 = [random.randint(1,3) for _ in range(4)]
cloud1, cloud2, cloud3, cloud4 = [random.choice(clouds) for _ in range(4)]
pe_x1, pe_y1, pe_x2, pe_y2 = -60, 610, 1224, 610
ve, vemax = [4,6,8], [7,8,9]
ve1, ve2 = random.choice(ve), random.choice(ve)
tiempo = time.perf_counter()

# Hitboxes
player_w, player_h = 59, 93
enemy_w, enemy_h = 56, 64
player_rect = pygame.Rect(pn_x, pn_y, player_w, player_h)
enemy1_rect = pygame.Rect(pe_x1, pe_y1, enemy_w, enemy_h)
enemy2_rect = pygame.Rect(pe_x2, pe_y2, enemy_w, enemy_h)

# Variables de monitor
last_monitor_time = time.perf_counter()
monitor_interval = 0.5

# --- Bucle menu ---
menu_ejecucion = True
while menu_ejecucion:
    reloj.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            menu_ejecucion = False
        elif event.type == pygame.QUIT:
            pygame.quit()
    screen.fill(NEGRO)
    x_offset = (SCREEN_WIDTH - GAME_WIDTH)//2
    y_offset = (SCREEN_HEIGHT - GAME_HEIGHT)//2
    screen.blit(pygame.transform.scale(menu, (GAME_WIDTH, GAME_HEIGHT)), (x_offset, y_offset))
    pygame.display.update()

# --- Bucle principal ---
jugando = True
while jugando:
    start_frame = time.perf_counter()

    # Medición CPU/GPU
    current_time = time.perf_counter()
    if current_time - last_monitor_time >= monitor_interval:
        cpu = psutil.cpu_percent(interval=0.0)
        gpu = gpu_usage()
        print(f"CPU: {cpu:.1f}% | GPU: {gpu}%")
        last_monitor_time = current_time

    reloj.tick(FPS)

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: jugando = False
            if event.key == pygame.K_RIGHT: vn_x = velocidad
            if event.key == pygame.K_LEFT: vn_x = -velocidad
            if event.key == pygame.K_UP: angulo = 0.001
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                vn_x = 0
                direccion = 1 if event.key==pygame.K_LEFT else -1

    # --- Movimiento jugador ---
    pn_x += vn_x
    pn_y = 580 - math.sin(angulo)*200
    if angulo > 0: angulo += 0.1
    if angulo >= math.pi: angulo = 0.0
    pn_x = max(0, min(GAME_WIDTH-60, pn_x))
    pn_y = max(0, min(GAME_HEIGHT-60, pn_y))

    # --- Movimiento enemigos ---
    pe_x1 += ve1
    if pe_x1 > GAME_WIDTH: 
        pe_x1 = -77
        ve1 = random.choice(ve if time.perf_counter()<tiempo+20 else vemax)
    pe_x2 -= ve2
    if pe_x2 < -60: 
        pe_x2 = GAME_WIDTH + 60
        ve2 = random.choice(ve if time.perf_counter()<tiempo+20 else vemax)

    # --- Movimiento nubes ---
    if control % 10 == 0:
        vr_x1, vr_x2, vr_x3, vr_x4 = [random.randint(1,3) for _ in range(4)]
    pr_x1 += vr_x1; pr_x2 += vr_x2; pr_x3 += vr_x3; pr_x4 += vr_x4
    for idx, pr_x in enumerate([pr_x1, pr_x2, pr_x3, pr_x4]):
        if pr_x > GAME_WIDTH:
            if idx==0: pr_x1=-77
            if idx==1: pr_x2=-77
            if idx==2: pr_x3=-77
            if idx==3: pr_x4=-77

    # --- Dibujos ---
    game_surface.blit(fondo, (0,0))
    if control % 25 == 0: cloud1 = random.choice(clouds)
    if control % 22 == 0: cloud2 = random.choice(clouds)
    if control % 17 == 0: cloud3 = random.choice(clouds)
    if control % 14 == 0: cloud4 = random.choice(clouds)
    for cx, cy, cloud in [(pr_x1, pr_y-60, cloud1), (pr_x2, pr_y-20, cloud2),
                          (pr_x3, pr_y-10, cloud3), (pr_x4, pr_y, cloud4)]:
        if 0 <= cx <= GAME_WIDTH:
            game_surface.blit(cloud, (cx, cy))

    # --- Animaciones jugador ---
    if vn_x < 0:
        if angulo==0.0: walking_animation(walk_left, game_surface, pn_x, pn_y, frame_counter)
        else: jumping_animation(jump_left, game_surface, pn_x, pn_y, angulo)
    elif vn_x > 0:
        if angulo==0.0: walking_animation(walk_right, game_surface, pn_x, pn_y, frame_counter)
        else: jumping_animation(jump_right, game_surface, pn_x, pn_y, angulo)
    else:
        if direccion==-1:
            if angulo==0: game_surface.blit(stayR, (pn_x, pn_y))
            else: jumping_animation(jump_right, game_surface, pn_x, pn_y, angulo)
        else:
            if angulo==0: game_surface.blit(stayL, (pn_x, pn_y))
            else: jumping_animation(jump_left, game_surface, pn_x, pn_y, angulo)

    # --- Animaciones enemigos ---
    if 0 <= pe_x1 <= GAME_WIDTH: walking_animation(enemy_right, game_surface, pe_x1, pe_y1, frame_counter)
    if 0 <= pe_x2 <= GAME_WIDTH: walking_animation(enemy_left, game_surface, pe_x2, pe_y2, frame_counter)

    # --- Colisiones ---
    player_rect.topleft = (pn_x, pn_y)
    enemy1_rect.topleft = (pe_x1, pe_y1)
    enemy2_rect.topleft = (pe_x2, pe_y2)
    if player_rect.colliderect(enemy1_rect) or player_rect.colliderect(enemy2_rect):
        jugando = False

    # --- Render final centrado ---
    x_offset = (SCREEN_WIDTH - GAME_WIDTH)//2
    y_offset = (SCREEN_HEIGHT - GAME_HEIGHT)//2
    screen.fill(NEGRO)
    screen.blit(game_surface, (x_offset, y_offset))
    pygame.display.update()

    frame_counter += 1
    control += 1

pygame.quit()
