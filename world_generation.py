from __future__ import annotations

from perlin_noise import PerlinNoise
import pygame
import random
import assets
import time
import json

class WorldGeneration():
    def __init__(self, world_size: int = 16, chunk_size: int = 16, image_size: int = 64) -> None:
        self.noise = PerlinNoise(5, time.time_ns())
        self.water_frequency = 0.3
        self.tree_frequency = 7 # 1 / tree_frequency
        
        self.chunk_size: int = chunk_size
        self.world_size: int = world_size
        self.image_size: int = image_size

        self.world: list[Chunk] = self.generate()
    
    def generate(self) -> list[Chunk]:
        world: list[Chunk] = []
        
        for x in range(self.world_size):
            for y in range(self.world_size):
                chunk_data: Chunk = self.generate_chunk((x,y))
                world.append(chunk_data)

        return world
    
    def generate_chunk(self, chunk_coords: tuple[int, int]) -> Chunk:
        absolute_cords = (chunk_coords[0] * self.chunk_size, chunk_coords[1] * self.chunk_size)
        
        # for temporary checkerboard
        color = "grass"
        
        max_perlin_position = self.world_size * self.chunk_size

        terrain: list[dict] = []
        entities: list[dict] = []
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                absolute_position = (absolute_cords[0] * self.image_size + x * self.image_size, absolute_cords[1] * self.image_size + y * self.image_size)

                perlin_position = (chunk_coords[0] * self.chunk_size + x, chunk_coords[1] * self.chunk_size + y)

                value_at_position = self.noise([perlin_position[0]/max_perlin_position, perlin_position[1]/max_perlin_position])
                sprite_name = "grass"
                if value_at_position <= self.water_frequency - 0.5: sprite_name = "water"

                sprite: pygame.Surface = assets.sprites["terrain"][f"{sprite_name}.png"]

                block = {
                    "sprite": sprite,
                    "position": absolute_position,
                    "is_passable": sprite_name == "grass"
                }

                if sprite_name == "grass" and random.randrange(0, self.tree_frequency) == 0:
                    tree_stump = {
                        "sprite": assets.sprites["terrain"]["CrappyTree.png"],
                        "position": absolute_position,
                        "is_passable": False
                    }
                    tree_middle1 = {
                        "sprite": ["terrain", "checker_black.png"],
                        "position": absolute_position,
                        "is_passable": True
                    }
                    tree_top = {
                        "sprite": ["terrain", "checker_black.png"],
                        "position": absolute_position,
                        "is_passable": True
                    }
                    entities.append(tree_stump)
                    #entities.append(tree_middle1)
                    #entities.append(tree_top)

                terrain.append(block)
            
            color: str = "grass" if color == "water" else "water"

        new_chunk = Chunk(absolute_cords, terrain, entities)

        return new_chunk

class Chunk():
    def __init__(self, position: tuple[int, int] = (-1,-1), terrain: list[dict] = [], entites: list[dict] = []):
        self.position: tuple[int, int] = position
        self.terrain: list[dict] = terrain
        self.entities: list[dict] = entites
    
    def load_from_string(self, string):
        splits = string.split("\n")
        self.position = tuple(splits)
        self.terrain = json.loads(splits[1])
        self.entities = json.loads(splits[2])

    def __str__(self) -> str:
        return f"{self.position}\n{json.dumps(self.terrain)}\n{json.dumps(self.entities)}"