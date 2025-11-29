"""
Simple launcher/menu Pygame para elegir entre Juego_1 y Juego_2.
Ejecuta los scripts como procesos separados usando el mismo intérprete Python.

Uso: desde la raíz del workspace ejecutar:
    python .\Juego_Menu\main_menu.py

- Pulsa el botón "Juego 1" o "Juego 2" para lanzar el juego correspondiente.
- Cierra el juego para volver al menú.
- Pulsa ESC o cierra la ventana para salir del menú.
"""

import os
import sys
import subprocess
import pygame
from pygame.locals import *

# Paths relativos (asume que se ejecuta desde workspace root o desde cualquier sitio; se resuelven vía __file__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JUEGO1_PATH = os.path.join(BASE_DIR, 'Juego_1', 'main_opl.py')
JUEGO2_PATH = os.path.join(BASE_DIR, 'Juego_2', 'main.py')

# Comprueba existencia
AVAILABLE = {
    'Juego 1': os.path.exists(JUEGO1_PATH),
    'Juego 2': os.path.exists(JUEGO2_PATH),
}

# Pygame UI
pygame.init()
WIDTH, HEIGHT = 640, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Selector de Juegos')
font = pygame.font.SysFont(None, 32)
small = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

# Botones: (label, rect)
button_w, button_h = 220, 64
gap = 30
x_center = WIDTH // 2 - button_w // 2
btn1_rect = pygame.Rect(x_center, 80, button_w, button_h)
btn2_rect = pygame.Rect(x_center, 80 + button_h + gap, button_w, button_h)

INFO_TEXT = 'Usa ARRIBA/ABAJO para seleccionar; ENTER para lanzar el juego.'


def draw_button(rect, label, enabled=True, selected=False):
    """Dibuja botón. `selected` resalta la opción activa (navegación por teclado)."""
    base = (40, 160, 40) if enabled else (120, 120, 120)
    if selected:
        # color más brillante para la selección
        color = tuple(min(255, c + 60) for c in base)
        border = (255, 215, 0)  # dorado
    else:
        color = base
        border = None

    pygame.draw.rect(screen, color, rect, border_radius=8)
    if border:
        pygame.draw.rect(screen, border, rect, width=3, border_radius=8)

    text = font.render(label, True, (255, 255, 255))
    tx = rect.x + (rect.w - text.get_width()) // 2
    ty = rect.y + (rect.h - text.get_height()) // 2
    screen.blit(text, (tx, ty))


def launch_game(path):
    """Lanza el juego indicado y espera hasta que termine."""
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        return
    print(f"Lanzando: {path}")
    # Usar el mismo intérprete
    try:
        # Cerrar la ventana del menú antes de lanzar el juego para que
        # la ventana del juego sea la única visible.
        global screen, font, small, clock
        try:
            pygame.display.quit()
        except Exception:
            pass

        # Bloquea hasta que el proceso termine; cuando termine, reabrimos el menú
        subprocess.run([sys.executable, path], check=False)
    finally:
        # Re-inicializar la ventana del menú (si pygame sigue disponible)
        try:
            # Asegurarse de que pygame esté inicializado
            if not pygame.get_init():
                pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Selector de Juegos')
            # Recrear fuentes y reloj en caso de que se hayan cerrado
            font = pygame.font.SysFont(None, 32)
            small = pygame.font.SysFont(None, 20)
            clock = pygame.time.Clock()
        except Exception:
            # Si la re-inicialización falla, informamos pero no rompemos el menú caller
            print('Advertencia: no se pudo reabrir la ventana del menú automaticamente.')
    except Exception as e:
        print('Error al lanzar el juego:', e)


running = True
# selección por teclado: 0 -> Juego 1, 1 -> Juego 2
selected = 0
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # Navegación: ARRIBA/ABAJO; activar con ENTER
            if event.key == K_UP:
                selected = max(0, selected - 1)
            elif event.key == K_DOWN:
                selected = min(1, selected + 1)
            elif event.key in (K_RETURN, K_KP_ENTER):
                # Lanzar el juego seleccionado (si está disponible)
                if selected == 0 and AVAILABLE['Juego 1']:
                    launch_game(JUEGO1_PATH)
                elif selected == 1 and AVAILABLE['Juego 2']:
                    launch_game(JUEGO2_PATH)

    screen.fill((18, 24, 34))

    # Título
    title = font.render('Menu de Inicio - Selecciona un Juego (usa flechas + ENTER)', True, (230, 230, 230))
    screen.blit(title, ((WIDTH - title.get_width()) // 2, 16))

    # Botones (resaltar según selección)
    draw_button(btn1_rect, 'Juego 1', enabled=AVAILABLE['Juego 1'], selected=(selected == 0))
    draw_button(btn2_rect, 'Juego 2', enabled=AVAILABLE['Juego 2'], selected=(selected == 1))

    # Estado disponibilidad
    available_text = 'Disponibilidad: ' + ', '.join(f"{k}: {'OK' if v else 'Falta'}" for k, v in AVAILABLE.items())
    st = small.render(available_text, True, (200, 200, 200))
    screen.blit(st, (12, HEIGHT - 28))

    # Info
    info = small.render(INFO_TEXT, True, (200, 200, 200))
    screen.blit(info, (12, HEIGHT - 48))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print('Menu cerrado.')
