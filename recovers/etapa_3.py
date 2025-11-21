import os
import pygame
import math
import time
import random

# Funciones
def walking_animation(walk, pn_x, pn_y):
    frame = int(time.time() * 10) % len(walk)
    ventana.blit(walk[frame], (pn_x, pn_y))
    frame = (frame + 1) % 8

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
    if angulo >= 2.625 and angulo < 3.11:
        ventana.blit(jump[7], (pn_x, pn_y))

# Inicializar
pygame.init()

# Medidas
ANCHO = 1280
ALTO = 720

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
MARRON = (180, 100, 60)

# Ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
print("directorio", os.getcwd())

# Imagenes
fondo = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\background.png").convert()
stayR = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\stay_right.png").convert()
stayL = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\stay_left.png").convert()
c1 = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\clouds\c1.png").convert()
c2 = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\clouds\c2.png").convert()
c3 = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\clouds\c3.png").convert()
c1.set_colorkey(NEGRO)
c2.set_colorkey(NEGRO)
c3.set_colorkey(NEGRO)
clouds = [c1, c2, c3]
stayR.set_colorkey(NEGRO)
stayL.set_colorkey(NEGRO)

walk_right = []
for i in range(1, 9):
    image = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\walk\right\run_r{}.png".format(i)).convert()
    walk_right.append(image)
for image in walk_right:
    image.set_colorkey(NEGRO)

walk_left = []
for i in range(1, 9):
    image = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\walk\left\run_l{}.png".format(i)).convert()
    walk_left.append(image)
for image in walk_left:
    image.set_colorkey(NEGRO)

jump_right = []
for i in range(1, 9):
    image = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\jump\jump_right\jump_r{}.png".format(i)).convert()
    jump_right.append(image)
for image in jump_right:
    image.set_colorkey(NEGRO)

jump_left = []
for i in range(1, 9):
    image = pygame.image.load(os.getcwd() + r"\Desktop\Game\texturas\jump\jump_left\jump_l{}.png".format(i)).convert()
    jump_left.append(image)
for image in jump_left:
    image.set_colorkey(NEGRO)

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

pn_x = 0
pn_y = 0
ph_x = 570
vn_x = 0
vn_y = 0
angulo = 0.0
velocidad = 5
direccion = -1
control = 0
cloud1 = clouds[random.randint(0, 2)]
cloud2 = clouds[random.randint(0, 2)]
cloud3 = clouds[random.randint(0, 2)]
cloud4 = clouds[random.randint(0, 2)]

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                direccion = -1
                vn_x = 0
            if event.key == pygame.K_LEFT:
                direccion = 1
                vn_x = 0
            print(pn_x)
            print(pn_y)

    # Salto
    pn_y = ph_x - (math.sin(angulo)) * 200
    if angulo > 0:
        angulo += 0.1
    if angulo >= math.pi:
        angulo = 0.0

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

    # Velocidad
    pn_x += vn_x

    # Verificar límites de la ventana para el pixel verde
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

    # Actualizar
    pygame.display.update()

# Salir
pygame.quit()
