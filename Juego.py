import os
import pygame
import math
import time
import random

# Rutas para las imagenes

# --- SISTEMA DE RUTAS COMPATIBLE ---
# Ubicación absoluta del archivo main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Función para formar una ruta válida para cualquier OS
def ruta(*subrutas):
    return os.path.join(BASE_DIR, *subrutas)


# Funciones
def walking_animation(walk, pn_x, pn_y):
    frame = int(time.time() * 10) % len(walk)
    ventana.blit(walk[frame], (pn_x, pn_y))
    frame = (frame + 1) % len(walk)

def jumping_animation(jump, pn_x, pn_y, angulo):
    if angulo < 0.375:
        ventana.blit(jump[0], (pn_x, pn_y))
    if angulo >= 0.375 and angulo < 0.75:
        ventana.blit(jump[1], (pn_x, pn_y))
    if angulo >= 0.75 and angulo < 1.125:
        ventana.blit(jump[2], (pn_x, pn_y))
    if angulo >= 1.125 and angulo < 1.5:
        ventana.blit(jump[3], (pn_x, pn_y))
    if angulo >= 1.5 and angulo < 1.875:
        ventana.blit(jump[4], (pn_x, pn_y))
    if angulo >= 1.875 and angulo < 2.25:
        ventana.blit(jump[5], (pn_x, pn_y))
    if angulo >= 2.25 and angulo < 2.625:
        ventana.blit(jump[6], (pn_x, pn_y))
    if angulo >= 2.625 and angulo <= math.pi:
        ventana.blit(jump[7], (pn_x, pn_y))

# Inicializar
pygame.init()

# Medidas
# ANCHO = 1280
# ALTO = 720
ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ANCHO = ventana.get_width()
ALTO = ventana.get_height()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
MARRON = (180, 100, 60)

# Ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# Imagenes
menu = pygame.image.load(ruta("texturas", "menu.png"))
fondo = pygame.image.load(ruta("texturas", "background.png")).convert()
stayR = pygame.image.load(ruta("texturas", "stay_right.png")).convert_alpha()
stayL = pygame.image.load(ruta("texturas", "stay_left.png")).convert_alpha()
# Cargar nubes
c1 = pygame.image.load(ruta("texturas", "clouds", "c1.png")).convert_alpha()
c2 = pygame.image.load(ruta("texturas", "clouds", "c2.png")).convert_alpha()
c3 = pygame.image.load(ruta("texturas", "clouds", "c3.png")).convert_alpha()
# Cargar ícono
icono = pygame.image.load(ruta("texturas", "icono.png")).convert_alpha()
icono.set_colorkey(NEGRO)
c1.set_colorkey(NEGRO)
c2.set_colorkey(NEGRO)
c3.set_colorkey(NEGRO)
clouds = [c1, c2, c3]
stayR.set_colorkey(NEGRO)
stayL.set_colorkey(NEGRO)
pygame.display.set_icon(icono)
enemy_right = []

# --- Enemigos ---
enemy_right = []
for i in range(1, 4):
    img = pygame.image.load(ruta("texturas", "enemy", "right", f"e_r{i}.png")).convert_alpha()
    enemy_right.append(img)

enemy_left = []
for i in range(1, 4):
    img = pygame.image.load(ruta("texturas", "enemy", "left", f"e_l{i}.png")).convert_alpha()
    enemy_left.append(img)

# --- Caminata del jugador ---
walk_right = []
for i in range(1, 9):
    img = pygame.image.load(ruta("texturas", "walk", "right", f"run_r{i}.png")).convert_alpha()
    walk_right.append(img)

walk_left = []
for i in range(1, 9):
    img = pygame.image.load(ruta("texturas", "walk", "left", f"run_l{i}.png")).convert_alpha()
    walk_left.append(img)

# --- Salto del jugador ---
jump_right = []
for i in range(1, 9):
    img = pygame.image.load(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png")).convert_alpha()
    jump_right.append(img)

jump_left = []
for i in range(1, 9):
    img = pygame.image.load(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png")).convert_alpha()
    jump_left.append(img)


# Datos
pr_x1 = 800
pr_x2 = 220
pr_x3 = 340
pr_x4 = 542
pr_y = 100
vr_x1 = random.randint(1, 3)
vr_x2 = random.randint(1, 3)
vr_x3 = random.randint(1, 3)
vr_x4 = random.randint(1, 3)

pn_x = 640
pn_y = 0
ph_x = 580
vn_x = 0
angulo = 0.0
velocidad = 5
direccion = -1
control = 0
cloud1 = clouds[random.randint(0, 2)]
cloud2 = clouds[random.randint(0, 2)]
cloud3 = clouds[random.randint(0, 2)]
cloud4 = clouds[random.randint(0, 2)]

pe_x1 = -60
pe_y1 = 610
pe_x2 = 1224
pe_y2 = 610
ve = [4,6,8]
vemax = [7,8,9]
ve1 = random.choice(ve)
ve2 = random.choice(ve)
tiempo = time.perf_counter()

# --- Música y efectos ---
pygame.mixer.music.load(ruta("Sounds", "normal.mp3"))  # carga música
pygame.mixer.music.play(-1)                            # reproducir en loop
volume = 0                                             # variable para controlar volumen
pygame.mixer.music.set_volume(0.5)                     # volumen inicial 50%


# Hitbox
player_h = 93
player_w = 59
enemy_h = 64
enemy_w = 56


# Bucle menu
menu_ejecucion = True
while menu_ejecucion:
    reloj.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu_ejecucion = False
        elif event.type == pygame.QUIT:
            pygame.quit()
    ventana.blit(menu, [0, 0])
    pygame.display.update()
    
# Bucle principal
jugando = True
while jugando:
    reloj.tick(60)
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jugando = False
            if event.key == pygame.K_RIGHT:
                vn_x = velocidad
            if event.key == pygame.K_LEFT:
                vn_x = -velocidad
            if event.key == pygame.K_UP:
                angulo = 0.001
            if event.key == pygame.K_u:
                volume = 1
            if event.key == pygame.K_j:
                volume = -1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                direccion = -1
                vn_x = 0
            if event.key == pygame.K_LEFT:
                direccion = 1
                vn_x = 0
            if event.key == pygame.K_u:
                volume_down = 0
            if event.key == pygame.K_j:
                volume = 0
            print(pn_x)
            print(pn_y)

    # Salto
    pn_y = ph_x - (math.sin(angulo)) * 200
    if angulo > 0:
        angulo += 0.1
    if angulo >= math.pi:
        angulo = 0.0

    # Movimiento de los enemigos
    pe_x1 += ve1
    pe_x2 -= ve2
    if pe_x1 > ANCHO:
        pe_x1 = -77
        if time.perf_counter() < tiempo+20.0:
            ve1 = random.choice(ve)
        else:
            ve1 = random.choice(vemax)
    pr_x2 += vr_x2
    if pe_x2 < -60:
        pe_x2 = 1300
        if time.perf_counter() < tiempo+20:
            ve2 = random.choice(ve)
        else:
            ve2 = random.choice(vemax)
    print(time.perf_counter()-tiempo)

    # Movimiento de las nubes
    pr_x1 += vr_x1
    if pr_x1 > ANCHO:
        pr_x1 = -77
        vr_x1 = random.randint(1, 3)
    pr_x2 += vr_x2
    if pr_x2 > ANCHO:
        pr_x2 = -77
        vr_x2 = random.randint(1, 3)
    pr_x3 += vr_x3
    if pr_x3 > ANCHO:
        pr_x3 = -77
        vr_x3 = random.randint(1, 3)
    pr_x4 += vr_x4
    if pr_x4 > ANCHO:
        pr_x4 = -77
        vr_x4 = random.randint(1, 3)

    # Velocidad del player

    pn_x += vn_x

    # Verificar límites de la ventana para el player
    if pn_x < 0:
        pn_x = 0
    if pn_x > ANCHO - 60:
        pn_x = ANCHO - 60

    if pn_y < 0:
        pn_y = 0
    if pn_y > ALTO - 60:
        pn_y = ALTO - 60

    # Dibujos
    ventana.blit(fondo, [0, 0])
    if control % 25 == 0:
        cloud1 = clouds[random.randint(0, 2)]
    if control % 22 == 0:
        cloud2 = clouds[random.randint(0, 2)]
    if control % 17 == 0:
        cloud3 = clouds[random.randint(0, 2)]
    if control % 14 == 0:
        cloud4 = clouds[random.randint(0, 2)]
    ventana.blit(cloud1, [pr_x1, pr_y - 60])
    ventana.blit(cloud2, [pr_x2, pr_y - 20])
    ventana.blit(cloud3, [pr_x3, pr_y - 10])
    ventana.blit(cloud4, [pr_x4, pr_y])
    control += 1

    # Animaciones player
    if vn_x < 0:
        if angulo == 0.0:
            walking_animation(walk_left, pn_x, pn_y)
        else:
            jumping_animation(jump_left, pn_x, pn_y, angulo)
    if vn_x > 0:
        if angulo == 0.0:
            walking_animation(walk_right, pn_x, pn_y)
        else:
            jumping_animation(jump_right, pn_x, pn_y, angulo)
    if vn_x == 0 and direccion == -1:
        if angulo == 0.0:
            ventana.blit(stayR, (pn_x, pn_y))
        else:
            jumping_animation(jump_right, pn_x, pn_y, angulo)
    if vn_x == 0 and direccion == 1:
        if angulo == 0.0:
            ventana.blit(stayL, (pn_x, pn_y))
        else:
            jumping_animation(jump_left, pn_x, pn_y, angulo)

    # Animacion enemigo
    walking_animation(enemy_left, pe_x2, pe_y2)
    walking_animation(enemy_right, pe_x1, pe_y1)
    #pygame.draw.rect(ventana, VERDE, (pn_x, pn_y, player_w, player_h))
    #pygame.draw.rect(ventana, NEGRO, (pe_x1, pe_y1, enemy_w, enemy_h))
    #pygame.draw.rect(ventana, NEGRO, (pe_x2, pe_y2, enemy_w, enemy_h))

    # Colision
    player = pygame.Rect(pn_x, pn_y, player_w, player_h) # crea la hitbox del player
    enemy_1 = pygame.Rect(pe_x1, pe_y1, enemy_w, enemy_h) # crea la hitbox del enemigo 1
    enemy_2 = pygame.Rect(pe_x2, pe_y2, enemy_w, enemy_h) # crea la hitbox del enemigo 2
    if player.colliderect(enemy_1) or player.colliderect(enemy_2): # verifica la colision con los enemigos
        jugando = False

    # Control de musica
    if volume == -1:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
    if volume == 1:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
    # Actualizar
    pygame.display.update()
# Salir
pygame.quit()
