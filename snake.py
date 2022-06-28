import pygame
import random

pause = False


class Snake:
    def __init__(self, length):
        self.posX = [200]*length
        self.posY = [200]*length
        self.length = length
        self.direction = "RIGHT"

    def move_left(self):
        self.direction = "LEFT"

    def move_right(self):
        self.direction = "RIGHT"

    def move_up(self):
        self.direction = "UP"

    def move_down(self):
        self.direction = "DOWN"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.posX[i] = self.posX[i - 1]
            self.posY[i] = self.posY[i - 1]
        if self.direction == "LEFT":
            self.posX[0] -= 12
        if self.direction == "RIGHT":
            self.posX[0] += 12
        if self.direction == "UP":
            self.posY[0] -= 12
        if self.direction == "DOWN":
            self.posY[0] += 12

    def update(self):
        self.walk()

    def render(self, screen):
        self.drawMenu(screen)
        for i in range(self.length):
            pygame.draw.circle(screen, pygame.Color("black"), (self.posX[i], self.posY[i]), 8)

    def increase_length(self):
        self.length += 1
        self.posX.append(-1)
        self.posY.append(-1)

    @staticmethod
    def drawMenu(screen):
        pygame.draw.line(screen, pygame.Color("blue"), [70, 50], [1130, 50], 10)
        pygame.draw.line(screen, pygame.Color("blue"), [70, 50], [70, 650], 10)
        pygame.draw.line(screen, pygame.Color("blue"), [1130, 650], [1130, 50], 10)
        pygame.draw.line(screen, pygame.Color("blue"), [1130, 650], [70, 650], 10)


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(90, 1110)
        self.y = random.randint(70, 640)

    def render(self, screen):
        pygame.draw.circle(screen, pygame.Color("red"), (self.x, self.y), 8)

    def move(self):
        self.x = random.randint(90, 1110)
        self.y = random.randint(70, 640)


class App:
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
            self.update()
            try:
                if not pause:
                    self.render()
            except Exception:
                self.game_over()
                pause = True
                self.reset()
            if self.snake.posX[0] >= 1120 or self.snake.posX[0] < 80 or self.snake.posY[0] \
                    >= 640 or self.snake.posY[0] < 60:
                self.game_over()
                pause = True
                self.reset()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")
        pygame.init()

        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake(5)
        self.food = Food(self.screen)

    def update(self):
        self.events()
        self.snake.update()

    def events(self):
        global pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.running = False
            if keys[pygame.K_RETURN]:
                pause = False
            if not pause:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.snake.move_left()
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    self.snake.move_up()
                if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    self.snake.move_down()
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.snake.move_right()

    def render(self):
        self.screen.fill((0, 255, 255))
        self.snake.render(self.screen)
        self.food.render(self.screen)
        self.display_score()
        pygame.display.flip()
        self.clock.tick(30)

        if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.food.x, self.food.y):
            self.food.move()
            self.snake.increase_length()

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.snake.posX[i], self.snake.posY[i]):
                raise "Game over"

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if x2 <= x1 + 15 <= x2 + 20:
            if y2 <= y1 + 15 <= y2 + 20:
                return True
        return False

    def game_over(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont('arial', 30)
        showScore = font.render(f"Game over!", True, (255, 0, 255))
        self.screen.blit(showScore, (500, 250))
        showScore2 = font.render(f"Press Enter if your want to play again, otherwise press Esc", True, (255, 0, 255))
        self.screen.blit(showScore2, (220, 350))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        mes = font.render(f"score: {self.snake.length-5}", True, (255, 0, 255))
        self.screen.blit(mes, (80, 5))

    def reset(self):
        self.snake = Snake(5)
        self.food = Food(self.screen)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
