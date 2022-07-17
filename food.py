import pygame
import random


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(90, 1110)
        self.y = random.randint(80, 620)

    def drawFood(self):
        apple = pygame.image.load("images/apple.jpg").convert_alpha()
        apple = pygame.transform.rotozoom(apple, 0, 0.6)
        self.screen.blit(apple, (self.x, self.y))

    def move(self):
        self.x = random.randint(100, 1100)
        self.y = random.randint(80, 620)