import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Simples")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)

# Variáveis do jogo
FPS = 60
GRAVITY = 0.3       # gravidade reduzida para queda mais lenta
JUMP_STRENGTH = -6 # pulo mais forte
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Classe do pássaro
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Classe dos tubos
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.width = PIPE_WIDTH
        self.passed = False

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Tubo de cima
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, self.width, self.height))
        # Tubo de baixo
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
    bird = Bird()
    pipes = []
    score = 0

    # Timer para criar tubos
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1500)

    running = True
    while running:
        clock.tick(FPS)
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Pulo detectado!")  # CONFIRMAÇÃO NO TERMINAL
                    bird.jump()
            if event.type == SPAWNPIPE:
                pipes.append(Pipe())

        bird.move()
        bird.draw()

        # Movimenta e desenha os tubos
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Verifica colisão
            if bird.get_rect().colliderect(pipe.get_top_rect()) or bird.get_rect().colliderect(pipe.get_bottom_rect()):
                running = False

            # Atualiza score quando passa o tubo
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1

        # Remove tubos que saíram da tela
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Verifica se pássaro bateu no chão ou no teto
        if bird.y > HEIGHT - bird.height or bird.y < 0:
            running = False

        # Desenha score
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.update()

    # Tela de Game Over
    SCREEN.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Score final: {score}", True, BLACK)
    SCREEN.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 30))
    SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 10))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
