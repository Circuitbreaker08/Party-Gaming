import pygame
import os

pygame.init()

sprites = {}

root = os.getcwd()
os.chdir(os.path.join(root, "assets/sprites"))

for directory in os.listdir():
    sprites.update({directory: {}})
    os.chdir(os.path.join(root, "assets/sprites", directory))
    for file in os.listdir():
        sprites[directory].update({file: pygame.image.load(file).convert_alpha()})