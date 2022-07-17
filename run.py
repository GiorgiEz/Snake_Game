import pygame
from snake import Snake
from food import Food

pause = False
score = 0

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
            self.update()
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
            if self.snake.posX[0] >= 1110 or self.snake.posX[0] < 80 or self.snake.posY[0] >= 620 or self.snake.posY[0] < 60:
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
        pygame.mixer.init()
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
                pygame.mixer.music.unpause()
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
        self.screen.fill((0,165,0))
        self.snake.drawSnake()
        self.food.drawFood()
        self.display_score()
        self.drawLBarriers(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def collisions(self):
        global score
        if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.food.x, self.food.y, 20, 20):
            self.food.move()
            self.snake.increaseLength()
            score += 1

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.posX[0], self.snake.posY[0], self.snake.posX[i], self.snake.posY[i], 10, 0):
                self.playSound("crash")
                raise "Game over"

    @staticmethod
    def is_collision(x1, y1, x2, y2, k, l):
        if x2 - l <= x1 <= x2 + k:
            if y2 - l <= y1 <= y2 + k:
                return True
        return False

    @staticmethod
    def drawLBarriers(screen):
        pygame.draw.line(screen, (255,200,0), [70, 54], [1130, 54], 10)
        pygame.draw.line(screen, (255,200,0), [70, 50], [70, 650], 10)
        pygame.draw.line(screen, (255,200,0), [1130, 650], [1130, 50], 10)
        pygame.draw.line(screen, (255,200,0), [1130, 645], [70, 645], 10)

    def playSound(self, sound):
        s = pygame.mixer.Sound(f"sounds/{sound}.mp3")
        pygame.mixer.Sound.play(s)

    def playBackgroundMusic(self):
        pygame.mixer.music.load("sounds/bgMusic.mp3")
        pygame.mixer.music.play()

    def game_over(self):
        self.screen.fill((0,170,0))
        font = pygame.font.SysFont('georgia', 50)
        font1 = pygame.font.SysFont('georgia', 30)
        showScore = font.render(f"Game over! Your score is {score}", True, (0, 0, 255))
        self.screen.blit(showScore, (300, 220))
        reset = font1.render(f"Press Enter to play again or press Esc to exit", True, (0, 0, 255))
        self.screen.blit(reset, (300, 320))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('georgia', 30)
        message = font.render(f"score: {self.snake.length-5}", True, (0, 0, 255))
        self.screen.blit(message, (80, 5))

    def resetGame(self):
        self.snake = Snake(5, self.screen)
        self.food = Food(self.screen)


if __name__ == "__main__":
    app = Run()
    app.run()