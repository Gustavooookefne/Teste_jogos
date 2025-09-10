import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Multiplayer Local")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)

FPS = 60
GRAVITY = 0.3
JUMP_STRENGTH = -7
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self, x, color):
        self.x = x
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30
        self.color = color
        self.alive = True
        self.score = 0

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        # Não deixa sair da tela
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.width = PIPE_WIDTH
        self.passed = []

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, self.width, self.height))
        bottom_y = self.height + PIPE_GAP
        bottom_height = HEIGHT - bottom_y
        pygame.draw.rect(SCREEN, GREEN, (self.x, bottom_y, self.width, bottom_height))

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.height)

    def get_bottom_rect(self):
        bottom_y = self.height + PIPE_GAP
        bottom_height = HEIGHT - bottom_y
        return pygame.Rect(self.x, bottom_y, self.width, bottom_height)

def main():
    bird1 = Bird(50, BLUE)
    bird2 = Bird(100, RED)
    pipes = []
    running = True

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)

    while running:
        clock.tick(FPS)
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if bird1.alive and event.key == pygame.K_SPACE:
                    bird1.jump()
                if bird2.alive and event.key == pygame.K_w:
                    bird2.jump()

            if event.type == SPAWNPIPE:
                pipes.append(Pipe())

        # Move e desenha pássaros
        if bird1.alive:
            bird1.move()
            bird1.draw()
        if bird2.alive:
            bird2.move()
            bird2.draw()

        # Move e desenha tubos
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Colisão com bird1
            if bird1.alive and (bird1.get_rect().colliderect(pipe.get_top_rect()) or bird1.get_rect().colliderect(pipe.get_bottom_rect())):
                bird1.alive = False
            # Colisão com bird2
            if bird2.alive and (bird2.get_rect().colliderect(pipe.get_top_rect()) or bird2.get_rect().colliderect(pipe.get_bottom_rect())):
                bird2.alive = False

            # Atualiza score para bird1
            if bird1.alive and (pipe.x + pipe.width < bird1.x) and (bird1 not in pipe.passed):
                pipe.passed.append(bird1)
                bird1.score += 1

            # Atualiza score para bird2
            if bird2.alive and (pipe.x + pipe.width < bird2.x) and (bird2 not in pipe.passed):
                pipe.passed.append(bird2)
                bird2.score += 1

        # Remove tubos fora da tela
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Checa se pássaros bateram no chão
        if bird1.alive and bird1.y > HEIGHT - bird1.height:
            bird1.alive = False
        if bird2.alive and bird2.y > HEIGHT - bird2.height:
            bird2.alive = False

        # Desenha pontuação
        score1_text = font.render(f"Player 1 (Azul): {bird1.score}", True, BLUE)
        score2_text = font.render(f"Player 2 (Vermelho): {bird2.score}", True, RED)
        SCREEN.blit(score1_text, (10, 10))
        SCREEN.blit(score2_text, (10, 40))

        pygame.display.update()

        # Termina o jogo se os dois morreram
        if not bird1.alive and not bird2.alive:
            running = False

    # Tela final
    SCREEN.fill(WHITE)
    over_text = font.render("Game Over!", True, BLACK)
    SCREEN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 30))

    # Mostra o vencedor
    if bird1.score > bird2.score:
        winner_text = font.render("Player 1 Venceu!", True, BLUE)
    elif bird2.score > bird1.score:
        winner_text = font.render("Player 2 Venceu!", True, RED)
    else:
        winner_text = font.render("Empate!", True, BLACK)

    SCREEN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 + 10))
    pygame.display.update()
    pygame.time.wait(4000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

def load_records():
    try:
        with open("record.txt", "r") as f:
            lines = f.readlines()
            record1 = int(lines[0].strip())
            record2 = int(lines[1].strip())
            return record1, record2
    except:
        # Se não existir arquivo, inicia com 0
        return 0, 0

def save_records(record1, record2):
    with open("record.txt", "w") as f:
        f.write(f"{record1}\n{record2}\n")
