import pygame
import math
import sys
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

# Datos
pr_x = 800
pr_y = 100
vr_x = 5
vr_y = 5

pn_x = 0
pn_y = 660
vn_x = 0
vn_y = 0
angulo = 0.0
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
                vn_x = 10
            if event.key == pygame.K_LEFT:
                vn_x = -10
            if event.key == pygame.K_UP:
                angulo = 0.001   

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                vn_x = 0
            if event.key == pygame.K_LEFT:
                vn_x = 0 
    print(pn_x,pn_y)
    # Salto
    pn_y = 660 - (math.sin(angulo))*200  
    if angulo >0:
        angulo += 0.1 
    if angulo >= math.pi:
        angulo = 0.0

    # Lógica
    pr_x += vr_x
    if pr_x > ANCHO:
        pr_x = -60

    pn_x += vn_x
    pn_y += vn_y


    # Dibujos
    ventana.fill(NEGRO)
    pygame.draw.rect(ventana, MARRON, (pr_x, pr_y, 60, 60))

    pygame.draw.rect(ventana, VERDE, (pn_x, pn_y, 60, 60))


    # Actualizar
    pygame.display.update()



# Salir
pygame.quit()