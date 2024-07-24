import pygame
import random
import assets

class WorldGeneration():
    def __init__(self, world_size: int = 16, chunk_size: int = 16) -> None:
        self.chunk_size: int = chunk_size
        self.world_size: int = world_size
        self.world: dict = self.generate()
    
    def generate(self) -> dict:
        world: dict = {}
        
        for x in range(self.world_size):
            for y in range(self.world_size):
                chunk_id: str = f"{x},{y}"
                chunk_data: list[int] = self.generate_chunk((x,y))
                world.update(chunk_id, chunk_data)

        return world
    
    def generate_chunk(self, chunk_coords) -> list[int]:
        blocks: list[pygame.Surface] = []
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                
                # Checkerboard Pattern
                y = (x + y) % 2
                spriteColor: str = "black" if y == 0 else "white"

                spriteName: pygame.Surface = assets.sprites["terrain"][f"checker_{spriteColor}.png"]
                
                blocks.append(spriteName)
        
        return blocks