import pygame
import sys

# Configuración del juego
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Inicializar Pygame y crear la ventana
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Definir las coordenadas y velocidades iniciales de los cuadrados
square1_x = 100
square1_y = 100
square1_vel_x = 5
square1_vel_y = 2
square1_width = 50
square1_height = 50

square2_x = 200
square2_y = 200
square2_vel_x = -3
square2_vel_y = -4
square2_width = 50
square2_height = 50

# Bucle principal del juego
running = True
while running:
    # Mantener la velocidad de fotogramas constante
    clock.tick(FPS)

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar las coordenadas de los cuadrados
    square1_x += square1_vel_x
    square1_y += square1_vel_y

    square2_x += square2_vel_x
    square2_y += square2_vel_y

    # Verificar colisión
    square1_rect = pygame.Rect(square1_x, square1_y, square1_width, square1_height)
    square2_rect = pygame.Rect(square2_x, square2_y, square2_width, square2_height)
    if square1_rect.colliderect(square2_rect):
        sys.exit()  # Terminar el juego si colisionan

    # Renderizar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (square1_x, square1_y, square1_width, square1_height))
    pygame.draw.rect(screen, WHITE, (square2_x, square2_y, square2_width, square2_height))
    pygame.display.flip()

# Salir del juego
pygame.quit()