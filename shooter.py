import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Shooting Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load images
player_image = pygame.image.load('images/player.png').convert_alpha()
player2_image = pygame.image.load('images/player2.png').convert_alpha()
bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
enemy_image = pygame.image.load('images/enemy.png').convert_alpha()
enemy2_image = pygame.image.load('images/enemy2.png').convert_alpha()
bullet_enemy_image = pygame.image.load('images/bullet_enemy.png').convert_alpha()
powerup_image = pygame.image.load('images/health.png').convert_alpha()
ally_image = pygame.image.load('images/ally.png').convert_alpha()
boss_image = pygame.image.load('images/boss1.png').convert_alpha()

# Resize images
player_size = (50, 50)
player2_size = (60, 60)  # Adjust size if needed
bullet_size = (10, 20)
enemy_size = (50, 50)
powerup_size = (30, 30)
enemy2_size = (60, 60)
bullet_enemy_size = (10, 20)
ally_size = (50, 50)
boss_size = (100, 100)

player_image = pygame.transform.scale(player_image, player_size)
player2_image = pygame.transform.scale(player2_image, player2_size)
bullet_image = pygame.transform.scale(bullet_image, bullet_size)
enemy_image = pygame.transform.scale(enemy_image, enemy_size)
enemy2_image = pygame.transform.scale(enemy2_image, enemy2_size)
bullet_enemy_image = pygame.transform.scale(bullet_enemy_image, bullet_enemy_size)
powerup_image = pygame.transform.scale(powerup_image, powerup_size)
ally_image = pygame.transform.scale(ally_image, ally_size)
boss_image = pygame.transform.scale(boss_image, boss_size)

# Sound effects
pygame.mixer.music.load('audio/background_music.mp3')
pygame.mixer.music.play(-1)  # Loop the background music
shoot_sound = pygame.mixer.Sound('audio/shoot.wav')
explosion_sound = pygame.mixer.Sound('audio/explosion.wav')

# Player attributes
player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
player_speed = 7
player_health = 3
is_player2 = False

# Bullet attributes
bullets = []
bullet_speed = 7

# Enemy attributes
enemies = []
enemy_speed = 3
enemy_spawn_delay = 1000  # milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()

# Extra enemy attributes
enemy2s = []
enemy2_shoot_delays = []
enemy2_speed = 2
enemy2_spawn_delay = 2000  # milliseconds
last_enemy2_spawn_time = pygame.time.get_ticks()
enemy2_bullets = []
enemy2_bullet_speed = 5
enemy2_shoot_delay = 3000  # milliseconds

# Power-up attributes
powerups = []
powerup_spawn_delay = 5000  # milliseconds
last_powerup_spawn_time = pygame.time.get_ticks()

# Ally attributes
ally_rect = None
ally_shot_count = 0

# Boss attributes
boss_rect = None
boss_speed = 3
boss_bullets = []
boss_bullet_speed = 7
boss_shoot_delay = 2000  # milliseconds
last_boss_shoot_time = pygame.time.get_ticks()

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
playing = False
game_over = False
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def home_screen():
    screen.fill(BLACK)
    draw_text('Enhanced Shooting Game', font, WHITE, screen, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50)
    draw_text('Press ENTER to Play', font, WHITE, screen, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2)
    pygame.display.flip()

def end_screen(score):
    screen.fill(BLACK)
    draw_text('Game Over', font, RED, screen, SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 50)
    draw_text(f'Final Score: {score}', font, WHITE, screen, SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2)
    draw_text('Press ENTER to Restart', font, WHITE, screen, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50)
    pygame.display.flip()

while running:
    if not playing and not game_over:
        home_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    playing = True
                    player_health = 3
                    score = 0
                    enemies = []
                    enemy2s = []
                    enemy2_shoot_delays = []
                    bullets = []
                    powerups = []
                    ally_rect = None  # Reset ally rect
                    ally_shot_count = 0  # Reset ally shot count
                    boss_rect = None  # Reset boss rect
                    boss_bullets = []  # Reset boss bullets
                    is_player2 = False
                    player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    elif game_over:
        end_screen(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    playing = True
                    player_health = 3
                    score = 0
                    enemies = []
                    enemy2s = []
                    enemy2_shoot_delays = []
                    bullets = []
                    powerups = []
                    ally_rect = None  # Reset ally rect
                    ally_shot_count = 0  # Reset ally shot count
                    boss_rect = None  # Reset boss rect
                    boss_bullets = []  # Reset boss bullets
                    is_player2 = False
                    player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if is_player2:
                        # Player 2 shotgun-style shooting with spread at 40 degrees
                        spread_angle = 20  # Half of 40 degrees
                        number_of_bullets = 3
                        angle_step = spread_angle / (number_of_bullets - 1)
                        for i in range(number_of_bullets):
                            angle = (i - (number_of_bullets // 2)) * angle_step
                            radians = math.radians(angle)
                            bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                            bullet_velocity = [bullet_speed * math.sin(radians), -bullet_speed * math.cos(radians)]
                            bullets.append((bullet_rect, bullet_velocity))
                    else:
                        bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                        bullets.append((bullet_rect, [0, -bullet_speed]))
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        if is_player2:
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
                player_rect.x += player_speed
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.y -= player_speed
            if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
                player_rect.y += player_speed
        else:
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
                player_rect.x += player_speed

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_delay:
            enemy_rect = enemy_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - enemy_size[0]), 0))
            enemies.append(enemy_rect)
            last_enemy_spawn_time = current_time

        # Spawn extra enemies if score >= 20
        if score >= 20 and current_time - last_enemy2_spawn_time > enemy2_spawn_delay:
            enemy2_rect = enemy2_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - enemy2_size[0]), 0))
            enemy2s.append(enemy2_rect)
            enemy2_shoot_delays.append(current_time)  # Initialize last shoot time
            last_enemy2_spawn_time = current_time

        # Spawn ally if score >= 40
        if score >= 40 and ally_rect is None:
            ally_rect = ally_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - ally_size[0]), 0))

        # Spawn power-ups if score >= 60
        if score >= 60 and current_time - last_powerup_spawn_time > powerup_spawn_delay:
            powerup_rect = powerup_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - powerup_size[0]), 0))
            powerups.append(powerup_rect)
            last_powerup_spawn_time = current_time

        # Move and shoot enemies
        for enemy_rect in enemies:
            enemy_rect.y += enemy_speed
            if enemy_rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy_rect)
                score -= 10  # Penalty for missed enemy

        # Move and shoot extra enemies
        for i, enemy2_rect in enumerate(enemy2s):
            enemy2_rect.y += enemy2_speed
            if enemy2_rect.top > SCREEN_HEIGHT:
                enemy2s.pop(i)
                enemy2_shoot_delays.pop(i)
                score -= 20  # Penalty for missed extra enemy

            # Extra enemy shooting
            if current_time - enemy2_shoot_delays[i] > enemy2_shoot_delay:
                bullet_rect = bullet_enemy_image.get_rect(midbottom=enemy2_rect.midbottom)
                bullet_velocity = [0, enemy2_bullet_speed]
                enemy2_bullets.append((bullet_rect, bullet_velocity))
                enemy2_shoot_delays[i] = current_time

        # Move and shoot power-ups
        for powerup_rect in powerups:
            powerup_rect.y += enemy_speed
            if powerup_rect.top > SCREEN_HEIGHT:
                powerups.remove(powerup_rect)

        # Move and shoot bullets
        for bullet_rect, bullet_velocity in bullets[:]:
            bullet_rect.x += bullet_velocity[0]
            bullet_rect.y += bullet_velocity[1]
            if bullet_rect.bottom < 0:
                bullets.remove((bullet_rect, bullet_velocity))

        # Move and shoot enemy2 bullets
        for bullet_rect, bullet_velocity in enemy2_bullets[:]:
            bullet_rect.x += bullet_velocity[0]
            bullet_rect.y += bullet_velocity[1]
            if bullet_rect.top > SCREEN_HEIGHT or bullet_rect.left < 0 or bullet_rect.right > SCREEN_WIDTH:
                enemy2_bullets.remove((bullet_rect, bullet_velocity))

        # Move boss if it exists
        if boss_rect:
            boss_rect.y += boss_speed
            if boss_rect.top > SCREEN_HEIGHT:
                boss_rect = None  # Remove boss if it goes off screen

        # Boss shooting logic
        if boss_rect:
            current_time = pygame.time.get_ticks()
            if current_time - last_boss_shoot_time > boss_shoot_delay:
                spread_angle = 20
                number_of_bullets = 3
                angle_step = spread_angle / (number_of_bullets - 1)
                for i in range(number_of_bullets):
                    angle = (i - (number_of_bullets // 2)) * angle_step
                    radians = math.radians(angle)
                    boss_bullet_rect = bullet_enemy_image.get_rect(midbottom=boss_rect.midbottom)
                    boss_bullet_velocity = [boss_bullet_speed * math.sin(radians), -boss_bullet_speed * math.cos(radians)]
                    boss_bullets.append((boss_bullet_rect, boss_bullet_velocity))
                last_boss_shoot_time = current_time

        # Check for collisions
        for bullet_rect, _ in bullets[:]:
            if bullet_rect.colliderect(boss_rect):
                bullets.remove((bullet_rect, _))
                boss_rect = None
                score += 100  # Reward for defeating the boss

        for enemy_rect in enemies[:]:
            if enemy_rect.colliderect(player_rect):
                player_health -= 1
                enemies.remove(enemy_rect)
                if player_health <= 0:
                    game_over = True
                    playing = False

        for enemy2_rect in enemy2s[:]:
            if enemy2_rect.colliderect(player_rect):
                player_health -= 2
                enemy2s.remove(enemy2_rect)
                if player_health <= 0:
                    game_over = True
                    playing = False

        for powerup_rect in powerups[:]:
            if powerup_rect.colliderect(player_rect):
                player_health += 1
                powerups.remove(powerup_rect)

        for bullet_rect, _ in enemy2_bullets[:]:
            if bullet_rect.colliderect(player_rect):
                player_health -= 1
                enemy2_bullets.remove((bullet_rect, _))
                if player_health <= 0:
                    game_over = True
                    playing = False

        if ally_rect and player_rect.colliderect(ally_rect):
            ally_rect = None
            ally_shot_count += 3

        # Drawing
        screen.fill(BLACK)
        screen.blit(player_image, player_rect)
        for bullet_rect, _ in bullets:
            screen.blit(bullet_image, bullet_rect)
        for enemy_rect in enemies:
            screen.blit(enemy_image, enemy_rect)
        for enemy2_rect in enemy2s:
            screen.blit(enemy2_image, enemy2_rect)
        for powerup_rect in powerups:
            screen.blit(powerup_image, powerup_rect)
        for boss_bullet_rect, _ in boss_bullets:
            screen.blit(bullet_enemy_image, boss_bullet_rect)
        if boss_rect:
            screen.blit(boss_image, boss_rect)
        if ally_rect:
            screen.blit(ally_image, ally_rect)
        
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
        draw_text(f'Health: {player_health}', font, WHITE, screen, SCREEN_WIDTH - 150, 10)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
