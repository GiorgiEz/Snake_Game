import pygame


class Snake:
    def __init__(self, length, screen):
        self.posX = [200]*length
        self.posY = [200]*length
        self.length = length
        self.direction = "RIGHT"
        self.block = pygame.image.load("images/block.jpg").convert_alpha()
        self.block = pygame.transform.rotozoom(self.block, 0, 0.6)
        self.screen = screen

    def move_left(self):
        self.direction = "LEFT"

    def move_right(self):
        self.direction = "RIGHT"

    def move_up(self):
        self.direction = "UP"

    def move_down(self):
        self.direction = "DOWN"

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.posX[i] = self.posX[i - 1]
            self.posY[i] = self.posY[i - 1]
        if self.direction == "LEFT":
            self.posX[0] -= 15
        if self.direction == "RIGHT":
            self.posX[0] += 15
        if self.direction == "UP":
            self.posY[0] -= 15
        if self.direction == "DOWN":
            self.posY[0] += 15

    def drawSnake(self):
        for i in range(self.length):
            self.screen.blit(self.block, (self.posX[i], self.posY[i]))

    def increaseLength(self):
        self.length += 1
        self.posX.append(-1)
        self.posY.append(-1)

