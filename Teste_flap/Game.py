import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Luta com Cenário")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Cores para blocos do cenário
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
BULLET_SPEED = 10
SUPER_BULLET_SPEED = 15

class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.color = color
        self.velocity_y = 0
        self.on_ground = False
        self.controls = controls
        self.health = 100
        self.bullets = []

    def move(self, keys):
        # Guardar posição anterior para verificar colisões
        old_x = self.rect.x
        
        if keys[self.controls['left']]:
            self.rect.x -= PLAYER_SPEED
            if self.check_collision_horizontal(blocks):
                self.rect.x = old_x
                
        if keys[self.controls['right']]:
            self.rect.x += PLAYER_SPEED
            if self.check_collision_horizontal(blocks):
                self.rect.x = old_x

        # Limitar o player dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if keys[self.controls['jump']] and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        # Aplicar gravidade
        self.velocity_y += GRAVITY
        
        # Aplicar movimento vertical
        self.rect.y += self.velocity_y
        
        # Verificar colisões verticais
        self.check_collision_vertical(blocks)
        
        # Verificar se tocou o chão da tela
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def check_collision_horizontal(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block['rect']):
                return True
        return False

    def check_collision_vertical(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block['rect']):
                # Se está caindo (velocidade positiva)
                if self.velocity_y > 0:
                    # Colidir por cima - pousar na plataforma
                    self.rect.bottom = block['rect'].top
                    self.velocity_y = 0
                    self.on_ground = True
                    return
                
                # Se está subindo (velocidade negativa)  
                elif self.velocity_y < 0:
                    # Colidir por baixo - bater a cabeça
                    self.rect.top = block['rect'].bottom
                    self.velocity_y = 0
                    return
        
        # Se chegou aqui, não está em contato com nenhum bloco
        if self.velocity_y >= 0 and self.rect.bottom < HEIGHT:
            self.on_ground = False

    def shoot(self):
        direction = 1 if self.color == BLUE else -1
        bullet = pygame.Rect(self.rect.centerx, self.rect.centery, 10, 5)
        self.bullets.append({'rect': bullet, 'direction': direction, 'speed': BULLET_SPEED, 'damage': 10, 'color': BLACK})

    def super_shoot(self):
        direction = 1 if self.color == BLUE else -1
        bullet = pygame.Rect(self.rect.centerx, self.rect.centery, 50, 25)
        self.bullets.append({'rect': bullet, 'direction': direction, 'speed': SUPER_BULLET_SPEED, 'damage': 45, 'color': RED})

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        for b in self.bullets:
            pygame.draw.rect(SCREEN, b['color'], b['rect'])

    def update_bullets(self, other_player):
        new_bullets = []
        for b in self.bullets:
            b['rect'].x += b['speed'] * b['direction']
            
            # Verificar colisão com o outro jogador
            if b['rect'].colliderect(other_player.rect):
                other_player.health -= b['damage']
                continue  # Remove a bala após acertar
            
            # Verificar colisão com blocos do cenário
            hit_block = False
            for block in blocks:
                if b['rect'].colliderect(block['rect']):
                    hit_block = True
                    break
            
            # Manter bala apenas se não saiu da tela e não acertou nada
            if not hit_block and 0 <= b['rect'].x <= WIDTH:
                new_bullets.append(b)
                
        self.bullets = new_bullets

def main():
    player1_controls = {
        'left': pygame.K_a,
        'right': pygame.K_d,
        'jump': pygame.K_w,
        'shoot': pygame.K_s,
        'super_shoot': pygame.K_q
    }
    player2_controls = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'jump': pygame.K_UP,
        'shoot': pygame.K_DOWN,
        'super_shoot': pygame.K_RSHIFT
    }

    player1 = Player(50, HEIGHT - 100, BLUE, player1_controls)
    player2 = Player(WIDTH - 90, HEIGHT - 100, RED, player2_controls)

    shot_cooldown = 200
    super_shot_cooldown = 1500
    last_shot_time_p1 = 0
    last_shot_time_p2 = 0
    last_super_shot_time_p1 = 0
    last_super_shot_time_p2 = 0

    global blocks
    blocks = [
        {'rect': pygame.Rect(0, HEIGHT - 40, WIDTH, 40), 'color': BROWN},   # chão
        {'rect': pygame.Rect(150, HEIGHT - 120, 150, 20), 'color': GREEN}, # plataforma
        {'rect': pygame.Rect(350, HEIGHT - 180, 200, 20), 'color': GRAY},  # plataforma
        {'rect': pygame.Rect(600, HEIGHT - 240, 150, 20), 'color': DARK_GRAY}, # plataforma
        {'rect': pygame.Rect(100, HEIGHT - 300, 100, 20), 'color': GREEN}, # plataforma alta esquerda
        {'rect': pygame.Rect(450, HEIGHT - 350, 120, 20), 'color': GRAY},  # plataforma mais alta centro
        {'rect': pygame.Rect(800, HEIGHT - 200, 100, 20), 'color': DARK_GRAY}, # plataforma direita
    ]

    running = True
    while running:
        clock.tick(FPS)
        SCREEN.fill(WHITE)

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == player1_controls['shoot']:
                    if current_time - last_shot_time_p1 > shot_cooldown:
                        player1.shoot()  # Removido o parâmetro 'keys'
                        last_shot_time_p1 = current_time
                if event.key == player1_controls['super_shoot']:
                    if current_time - last_super_shot_time_p1 > super_shot_cooldown:
                        player1.super_shoot()  # Removido o parâmetro 'keys'
                        last_super_shot_time_p1 = current_time

                if event.key == player2_controls['shoot']:
                    if current_time - last_shot_time_p2 > shot_cooldown:
                        player2.shoot()  # Removido o parâmetro 'keys'
                        last_shot_time_p2 = current_time
                if event.key == player2_controls['super_shoot']:
                    if current_time - last_super_shot_time_p2 > super_shot_cooldown:
                        player2.super_shoot()  # Removido o parâmetro 'keys'
                        last_super_shot_time_p2 = current_time

        keys = pygame.key.get_pressed()
        player1.move(keys)
        player2.move(keys)

        player1.apply_gravity()
        player2.apply_gravity()

        player1.update_bullets(player2)
        player2.update_bullets(player1)

        # Desenhar cenário primeiro (fundo)
        for block in blocks:
            pygame.draw.rect(SCREEN, block['color'], block['rect'])

        # Desenhar jogadores por cima
        player1.draw()
        player2.draw()

        # Interface
        health_text_p1 = font.render(f"Vida P1: {player1.health}", True, BLUE)
        health_text_p2 = font.render(f"Vida P2: {player2.health}", True, RED)
        SCREEN.blit(health_text_p1, (10, 10))
        SCREEN.blit(health_text_p2, (WIDTH - health_text_p2.get_width() - 10, 10))

        # Mostrar cooldowns
        p1_shot_cd = max(0, shot_cooldown - (current_time - last_shot_time_p1))
        p1_super_cd = max(0, super_shot_cooldown - (current_time - last_super_shot_time_p1))
        p2_shot_cd = max(0, shot_cooldown - (current_time - last_shot_time_p2))
        p2_super_cd = max(0, super_shot_cooldown - (current_time - last_super_shot_time_p2))
        
        cd_text_p1 = font.render(f"Tiro: {p1_shot_cd//10}/20 | Super: {p1_super_cd//100}/15", True, BLUE)
        cd_text_p2 = font.render(f"Tiro: {p2_shot_cd//10}/20 | Super: {p2_super_cd//100}/15", True, RED)
        SCREEN.blit(cd_text_p1, (10, 50))
        SCREEN.blit(cd_text_p2, (WIDTH - cd_text_p2.get_width() - 10, 50))

        # Mostrar controles
        controls_text = font.render("P1: WASD + Q(super) + S(tiro) + E(escudo) | P2: Setas + Shift(super) + Down(tiro) + Ctrl(escudo)", True, BLACK)
        SCREEN.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT - 30))

        if player1.health <= 0 or player2.health <= 0:
            running = False

        pygame.display.update()

    # Tela de resultado
    SCREEN.fill(WHITE)
    if player1.health <= 0 and player2.health <= 0:
        result_text = font.render("Empate!", True, BLACK)
    elif player1.health <= 0:
        result_text = font.render("Jogador 2 (Vermelho) venceu!", True, RED)
    else:
        result_text = font.render("Jogador 1 (Azul) venceu!", True, BLUE)

    SCREEN.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 20))
    
    restart_text = font.render("Pressione qualquer tecla para sair", True, BLACK)
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    
    pygame.display.update()
    
    # Aguardar input para fechar
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()