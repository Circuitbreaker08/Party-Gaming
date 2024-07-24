import pygame
import socket
import sys

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
clock = pygame.time.Clock()

import assets

class Button():
    def __init__(self, position: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int], func):
        self.position = position
        self.size = size
        self.color = color
        self.func = func

    def tick(self):
        if mouse[0] > self.position[0] and mouse[1] > self.position[1] and mouse[0] < self.position[0] + self.size[0] and mouse[1] < self.position[1] + self.size[1] and mouse[0]:
            self.func()
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.position, self.size))

ui: list[Button] = [Button((100, 100), (64, 64), (255, 0, 0), lambda: print("Hello World"))]

running = True
while running:
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for element in ui:
        element.tick()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()