import pygame

from src.bomb.fire import Fire


class FireRight(Fire):
    image = pygame.image.load('img/Bomb3.png')

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
