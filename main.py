from __future__ import annotations

import threading
import pygame
import socket
import json
import sys

with open("env.json") as f: env = json.loads(f.read())

IMAGE_SIZE = 64

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
clock = pygame.time.Clock()

game_manager: None | HostGameManager | ClientGameManager = None
in_game = False
is_host = False

from world_generation import WorldGeneration, Chunk
import connection
import assets


def lobby_init(_is_host):
    global game_manager, ui, is_host
    ui = []
    is_host = _is_host
    if _is_host:
        game_manager = HostGameManager()
    else:
        game_manager = ClientGameManager()

class GameManager():
    pass

class HostGameManager(GameManager):
    def __init__(self):
        global ui
        self.playing = False
        self.player = Player()
        players.append(self.player)
        self.player.change_name(env["NAME"])
        self.players: list[connection.HostConnection] = []

        self.s = socket.socket()
        self.s.bind(("", env["PORT"]))
        self.s.listen()
        threading.Thread(target=self.connection_accept).start()

        ui = [Button((100, 100), (320, 64), assets.sprites["ui"]["start.png"], self.start_game)]

    def tick(self):
        self.player.move((keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w]))

    def connection_accept(self):
        while True:
            c, addr = self.s.accept()
            print(f"Accepted connection from {addr}")
            self.players.append(connection.HostConnection(c, Player()))

    def send(self, c: connection.HostConnection, data):
        c.c.send(f"{json.dumps(data)}§".encode())

    def start_game(self):
        global in_game, chunks
        in_game = True
        chunks = generate_world()
        chunks_string_list = []
        for chunk in chunks:
            chunks_string_list.append(str(chunk))

        ui = []
        for player in self.players:
            self.send(player, {"type": "start_game"})
            #self.send(player, {"type": "load_chunks", "body": chunks_string_list})

class ClientGameManager(GameManager):
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((env["IP"], env["PORT"]))
        self.connection = connection.ClientConnection(self.s)
        self.send({"type": "name_register", "body": env["NAME"]})

    def tick(self):
        self.connection.player.move((keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w]))

    def send(self, data):
        self.s.send(f"{json.dumps(data)}§".encode())


class ButtonPrimitive():
    def __init__(self, position: tuple[int, int], size: tuple[int, int], func):
        self.position = position
        self.size = size
        self.func = func

    def tick(self):
        if mouse[0] > self.position[0] and mouse[1] > self.position[1] and mouse[0] < self.position[0] + self.size[0] and mouse[1] < self.position[1] + self.size[1] and mouse_pressed[0]:
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


class Player():
    def __init__(self):
        self.position = [0, 0]
        self.name = "player"

    def change_name(self, name):
        self.name = name

    def move(self, velocity):
        self.position[0] += velocity[0]
        self.position[1] += velocity[1]


chunks: list[Chunk] = []

def generate_world() -> list[Chunk]:
    world_generator: WorldGeneration = WorldGeneration(2, 16, IMAGE_SIZE) # world is 32 chunks by 32 chunks; chunks are 16x16
    return world_generator.world # just the entire world for now

#chunks = generate_world()

def render_chunks(screen: pygame.Surface) -> None:
    for chunk in chunks:
        chunk_position: tuple[int, int] = chunk.position
        chunk_terrain: list[dict] = chunk.terrain
        chunk_entities: list[dict] = chunk.entities
        for terrain in chunk_terrain:
            spritePath = terrain["sprite"]
            sprite = assets.sprites[spritePath[0]][spritePath[1]]
            sprite_position = terrain["position"]
            screen.blit(sprite, sprite_position)
        for entity in chunk_entities:
            spritePath = terrain["sprite"]
            sprite = assets.sprites[spritePath[0]][spritePath[1]]
            sprite_position = entity["position"]
            screen.blit(sprite, sprite_position)



ui: list[Button] = [
    Button((100, 100), (320, 64), assets.sprites["ui"]["join.png"], lambda: lobby_init(False)),
    Button((100, 200), (320, 64), assets.sprites["ui"]["host.png"], lambda: lobby_init(True))
]

players: list[Player] = []

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

    if game_manager != None:
        game_manager.tick()

    if in_game:
        render_chunks(screen)

    for element in ui:
        element.tick()

    print([x.position for x in players], end="\r")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()