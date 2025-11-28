# funciones.py
import pygame
import math
import time

def walking_animation(walk, ventana, pn_x, pn_y, frame_counter):
    frame = (frame_counter // 3) % len(walk)
    ventana.blit(walk[frame], (pn_x, pn_y))

def jumping_animation(jump, ventana, pn_x, pn_y, angulo):
    # calcula índice de sprite según angulo
    index = min(int(angulo / (math.pi/8)), len(jump)-1)
    ventana.blit(jump[index], (pn_x, pn_y))
