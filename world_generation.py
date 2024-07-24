from __future__ import annotations

import pygame
import random
import assets

class WorldGeneration():
    def __init__(self, world_size: int = 16, chunk_size: int = 16) -> None:
        self.chunk_size: int = chunk_size
        self.world_size: int = world_size
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
        color = "black"
        
        terrain: list[dict] = []
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                # Flip flop the color for checkerboard (temporary)
                color: str = "black" if color == "white" else "white"

                sprite: pygame.Surface = assets.sprites["terrain"][f"checker_{color}.png"]

                block = {
                    "sprite": sprite,
                    "position": (absolute_cords[0] + x, absolute_cords[1] + y),
                }

                terrain.append(block)
        
        new_chunk = Chunk(absolute_cords, terrain)

        return new_chunk

class Chunk():
    def __init__(self, position: tuple[int, int], terrain: list[dict]):
        self.position: tuple[int, int] = position
        self.terrain: list[dict] = terrain