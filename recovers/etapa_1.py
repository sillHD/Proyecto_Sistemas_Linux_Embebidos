import pygame
import math
import time
#funciones
def walking_animation(walk,pn_x,pn_y):
    frame = int(time.time()*10)%len(walk)
    ventana.blit(walk[frame],(pn_x, pn_y))
    frame = (frame+1)%8

def jumping_animation(jump,pn_x,pn_y,angulo):
    if angulo < 0.375:
        ventana.blit(jump[0],(pn_x, pn_y))
    if angulo >= 0.375 and angulo < 0.75:
        ventana.blit(jump[1],(pn_x, pn_y))
    if angulo >= 0.75 and angulo < 1.125:
        ventana.blit(jump[2],(pn_x, pn_y))
    if angulo >= 1.125 and angulo < 1.5:
        ventana.blit(jump[3],(pn_x, pn_y))
    if angulo >= 1.5 and angulo < 1.875:
        ventana.blit(jump[4],(pn_x, pn_y))
    if angulo >= 1.875 and angulo < 2.25:
        ventana.blit(jump[5],(pn_x, pn_y))
    if angulo >= 2.25 and angulo < 2.625:
        ventana.blit(jump[6],(pn_x, pn_y))
    if angulo >= 2.625 and angulo < 3.11:
        ventana.blit(jump[7],(pn_x, pn_y))

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

# imagenes
fondo = pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\background.jpg").convert()
stayR = pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\stay_right.png").convert()
stayL = pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\stay_left.png").convert()
stayR.set_colorkey(NEGRO) 
stayL.set_colorkey(NEGRO) # la linea 31 y 32 vuelven transparente el fondo de la imagen del player cuando no se mueve

walk_right = [pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r1.png").convert(), # formamos un vector para las imagenes cuando el player este caminando hacia la derecha
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r2.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r3.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r4.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r5.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r6.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r7.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\right\run_r8.png").convert()]
for image in walk_right: # asi hacemos que el fondo de las imagenes del vector se vuelva transparente
     image.set_colorkey(NEGRO)

walk_left =  [pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l1.png").convert(), # lo mismo que el vector de arriba pero para la izquierda
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l2.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l3.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l4.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l5.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l6.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l7.png").convert(),
              pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\walk\left\run_l8.png").convert()]
for image in walk_left: # lo mismo que el for de arriba pero para el vector walk_left
     image.set_colorkey(NEGRO)

jump_right = [pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r1.png").convert(), # este vector contiene las animaciones para cuando el player salte
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r2.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r3.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r4.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r5.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r6.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r7.png").convert(),
        pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_right\jump_r8.png").convert()]
for image in jump_right: # la misma funcion que los de arriba
     image.set_colorkey(NEGRO)

jump_left = [pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l1.png").convert(), # lo mismo que el vector de arriba pero cuando salte hacia la izquierda
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l2.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l3.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l4.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l5.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l6.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l7.png").convert(),
            pygame.image.load(r"C:\Users\Ismael CR\Desktop\Game\texturas\jump\jump_left\jump_l8.png").convert()]
for image in jump_left: # la misma funcion que los de arriba
     image.set_colorkey(NEGRO)
# Datos
pr_x = 800
pr_y = 100
vr_x = 5
vr_y = 5

pn_x = 0
pn_y = 590
vn_x = 0
vn_y = 0
angulo = 0.0
velocidad = 5 # controla la velocidad del player
direccion = -1 # determina la direccion de la imagen cuando el player no se esta moviendo
rango_salto = 200 # controla el tamaño del salto

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
    # Salto y animacion de salto
    pn_y = 625 - (math.sin(angulo)) * rango_salto
    if angulo > 0:
        angulo += 0.1
    if angulo >= math.pi:
        angulo = 0.0

    # Lógica
    pr_x += vr_x
    if pr_x > ANCHO:
        pr_x = -60

    pn_x += vn_x
    pn_y += vn_y

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
    ventana.blit(fondo,[0,0])
    if vn_x < 0:     
        if angulo == 0.0:
            walking_animation(walk_left,pn_x,pn_y)
        else:
            jumping_animation(jump_left,pn_x,pn_y,angulo)
    if vn_x > 0:
        if angulo == 0.0:
            walking_animation(walk_right,pn_x,pn_y)
        else: 
            jumping_animation(jump_right,pn_x,pn_y,angulo)
    if vn_x == 0 and direccion == -1:
        if angulo == 0.0:
            ventana.blit(stayR,(pn_x, pn_y))
        else:
            jumping_animation(jump_right,pn_x,pn_y,angulo)
    if vn_x == 0 and direccion == 1:
        if angulo == 0.0:
            ventana.blit(stayL,(pn_x, pn_y))
        else:
            jumping_animation(jump_left,pn_x,pn_y,angulo)
    pygame.draw.rect(ventana, MARRON, (pr_x, pr_y, 60, 60))

    # Actualizar
    pygame.display.update()

# Salir
pygame.quit()
