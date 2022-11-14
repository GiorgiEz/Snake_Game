import pygame, random

pause, score = False, 0

class Snake:
    def __init__(self, length, screen):
        self.posX = [200] * length
        self.posY = [200] * length
        self.length = length
        self.direction = "RIGHT"
        self.block = pygame.image.load("images/square.png").convert_alpha()
        self.block = pygame.transform.rotozoom(self.block, 0, 0.1)
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


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(90, 1110)
        self.y = random.randint(80, 610)

    def drawFood(self):
        apple = pygame.image.load("images/apple.png").convert_alpha()
        apple = pygame.transform.rotozoom(apple, 0, 0.7)
        self.screen.blit(apple, (self.x, self.y))

    def move(self):
        self.x = random.randint(100, 1100)
        self.y = random.randint(80, 610)


class Run:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.food = None

    def run(self):
        global pause
        self.init()
        while self.running:
            self.checkForCollisions()

    def checkForCollisions(self):
        global pause
        while self.running:
            self.update()
            try:
                if not pause:
                    self.collisions()
                    self.render()
            except Exception:
                self.deathScreen()
            if self.snake.posX[0] >= 1110 or self.snake.posX[0] < 80 or \
                    self.snake.posY[0] >= 620 or self.snake.posY[0] < 60:
                self.deathScreen()

    def deathScreen(self):
        global pause
        self.game_over()
        pause = True
        self.resetGame()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake(5, self.screen)
        self.food = Food(self.screen)

    def update(self):
        self.events()
        self.snake.move()

    def events(self):
        global pause, score
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False
            if keys[pygame.K_RETURN]:
                if pause:
                    score = 0
                pause = False
            if not pause:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    if self.snake.direction != "RIGHT":
                        self.snake.move_left()
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    if self.snake.direction != "DOWN":
                        self.snake.move_up()
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    if self.snake.direction != "UP":
                        self.snake.move_down()
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    if self.snake.direction != "LEFT":
                        self.snake.move_right()

    def render(self):
        self.screen.fill((0, 150, 0))
        self.snake.drawSnake()
        self.food.drawFood()
        self.display_score()
        self.drawBarriers(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def collisions(self):
        global score
        if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.food.x, self.food.y, 20, 20):
            self.food.move()
            self.snake.increaseLength()
            score += 1

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.snake.posX[i], self.snake.posY[i], 10, 0):
                raise "Game over"

    @staticmethod
    def is_collision(x1, y1, x2, y2, k, l):
        if x2 - l <= x1 <= x2 + k:
            if y2 - l <= y1 <= y2 + k:
                return True
        return False

    @staticmethod
    def drawBarriers(screen):
        pygame.draw.line(screen, (255, 200, 0), [70, 54], [1130, 54], 10)
        pygame.draw.line(screen, (255, 200, 0), [70, 50], [70, 650], 10)
        pygame.draw.line(screen, (255, 200, 0), [1130, 650], [1130, 50], 10)
        pygame.draw.line(screen, (255, 200, 0), [1130, 645], [70, 645], 10)

    def game_over(self):
        self.screen.fill((0, 170, 0))
        font = pygame.font.SysFont('georgia', 50)
        font1 = pygame.font.SysFont('georgia', 30)
        showScore = font.render(f"Game over! You score is {score}", True, (0, 0, 255))
        self.screen.blit(showScore, (300, 220))
        reset = font1.render(f"Press Enter to play again or press Esc to exit", True, (0, 0, 255))
        self.screen.blit(reset, (300, 320))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('georgia', 30)
        message = font.render(f"score: {self.snake.length - 5}", True, (0, 0, 255))
        self.screen.blit(message, (80, 5))

    def resetGame(self):
        self.snake = Snake(5, self.screen)
        self.food = Food(self.screen)


if __name__ == "__main__":
    app = Run()
    app.run()

