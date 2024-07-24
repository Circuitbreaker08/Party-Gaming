import pygame
import socket
import sys

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
clock = pygame.time.Clock()

import world_generation
import connection
import assets

class GameManager():
    pass

class HostGameManager(GameManager):
    def __init__(self):
        self.connection = connection.HostConnection()

class ClientGameManager(GameManager):
    def __tick__(self):
        self.connection = connection.ClientConnection()


class ButtonPrimitive():
    def __init__(self, position: tuple[int, int], size: tuple[int, int], func):
        self.position = position
        self.size = size
        self.func = func

    def tick(self):
        if mouse[0] > self.position[0] and mouse[1] > self.position[1] and mouse[0] < self.position[0] + self.size[0] and mouse[1] < self.position[1] + self.size[1] and mouse[0]:
            self.func()


class ButtonColor(ButtonPrimitive):
    def __init__(self, position, size, color, func):
        self.position = position
        self.size = size
        self.color = color
        self.func = func

    def tick(self):
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.position, self.size))
        super().tick()


class Button(ButtonPrimitive):
    def __init__(self, position, size, sprite, func):
        self.position = position
        self.size = size
        self.sprite = sprite
        self.func = func
        
    def tick(self):
        screen.blit(self.sprite, self.position)
        super().tick()


class Chunk():
    def __init__(self, position: tuple[int, int], terrain: dict[tuple[int, int], dict]):
        self.position = position
        self.terrain = terrain

    def tick(self):
        for entity in self.terrain.values():
            entity.tick()

chunks = []

ui: list[Button] = [
    Button((100, 100), (320, 64), assets.sprites["ui"]["join.png"], lambda: print("Join")),
    Button((100, 200), (320, 64), assets.sprites["ui"]["host.png"], lambda: print("Host"))
]

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

    for chunk in chunks:
        chunk.tick()

    for element in ui:
        element.tick()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()