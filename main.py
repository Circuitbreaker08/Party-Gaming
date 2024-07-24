import pygame
import socket
import json
import sys

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
clock = pygame.time.Clock()

from world_generation import WorldGeneration, Chunk
import connection
import assets

with open("env.json") as f: env = json.loads(f.read())

class GameManager():
    pass

class HostGameManager(GameManager):
    def __init__(self):
        self.s = socket.socket()
        self.s.bind("", env["PORT"])
        self.s.listen()
        self.connection = connection.HostConnection(self.s)

class ClientGameManager(GameManager):
    def __tick__(self):
        self.s = socket.socket()
        self.connection = connection.ClientConnection(self.s)


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

chunks = []

world_generator: WorldGeneration = WorldGeneration(32, 16) # world is 32 chunks by 32 chunks; chunks are 16x16
chunks: list[Chunk] = []
chunks = world_generator.world # just the entire world for now

def renderChunks(screen: pygame.Surface):
    for chunk in chunks:
        chunk_position: tuple[int, int] = chunk.position
        chunk_terrain: list[dict] = chunk.terrain
        for terrain in chunk_terrain:
            sprite = terrain["sprite"]
            sprite_position = terrain["position"]
            screen.blit(sprite, sprite_position)


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

    renderChunks(screen)

    for element in ui:
        element.tick()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()