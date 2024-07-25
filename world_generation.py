from __future__ import annotations

from perlin_noise import PerlinNoise
import pygame
import random
import assets
import time

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class WorldGeneration():
    def __init__(self, world_size: int = 16, chunk_size: int = 16, image_size: int = 64) -> None:
        self.noise = PerlinNoise(10, time.time_ns())
        self.water_frequency = 0.35
        
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
        
        terrain: list[dict] = []
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                absolute_position = (absolute_cords[0] * self.image_size + x * self.image_size, absolute_cords[1] * self.image_size + y * self.image_size)

                perlin_position = (chunk_coords[0] * self.chunk_size + x, chunk_coords[1] * self.chunk_size + y)
                print(perlin_position)

                #print(self.global_x / self.global_axis_size)
                #print(self.global_y / self.global_axis_size)

                #value_at_position = self.noise([absolute_position[0]/absolute_position_max[0], absolute_position[1]/absolute_position_max[1]])
                #sigmoid_value = translate(value_at_position, -0.5, 1, 0, 1)
                sprite_name = "grass"
                #if sigmoid_value < self.water_frequency: sprite_name = "water"

                sprite: pygame.Surface = assets.sprites["terrain"][f"{sprite_name}.png"]

                block = {
                    "sprite": sprite,
                    "position": absolute_position,
                    "is_passable": True
                }

                terrain.append(block)
            
            color: str = "grass" if color == "water" else "water"

        new_chunk = Chunk(absolute_cords, terrain)

        return new_chunk

class Chunk():
    def __init__(self, position: tuple[int, int], terrain: list[dict]):
        self.position: tuple[int, int] = position
        self.terrain: list[dict] = terrain