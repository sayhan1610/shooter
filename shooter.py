import pygame
import random

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
player_image = pygame.image.load('player.png').convert_alpha()
bullet_image = pygame.image.load('bullet.png').convert_alpha()
enemy_image = pygame.image.load('enemy.png').convert_alpha()
powerup_image = pygame.image.load('health.png').convert_alpha()

# Resize images
player_size = (50, 50)
bullet_size = (10, 20)
enemy_size = (50, 50)
powerup_size = (30, 30)

player_image = pygame.transform.scale(player_image, player_size)
bullet_image = pygame.transform.scale(bullet_image, bullet_size)
enemy_image = pygame.transform.scale(enemy_image, enemy_size)
powerup_image = pygame.transform.scale(powerup_image, powerup_size)

# Sound effects
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Loop the background music
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

# Player attributes
player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
player_speed = 5
player_health = 3

# Bullet attributes
bullets = []
bullet_speed = 7

# Enemy attributes
enemies = []
enemy_speed = 3
enemy_spawn_delay = 1000  # milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()

# Power-up attributes
powerups = []
powerup_spawn_delay = 5000  # milliseconds
last_powerup_spawn_time = pygame.time.get_ticks()

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
                    bullets = []
                    powerups = []
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
                    bullets = []
                    powerups = []
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                    bullets.append(bullet_rect)
                    shoot_sound.play()
        
        keys = pygame.key.get_pressed()
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
        
        # Spawn power-ups
        if current_time - last_powerup_spawn_time > powerup_spawn_delay:
            powerup_rect = powerup_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - powerup_size[0]), 0))
            powerups.append(powerup_rect)
            last_powerup_spawn_time = current_time

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)
        
        # Move enemies
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_health -= 1
                if player_health == 0:
                    game_over = True
                    playing = False

        # Move power-ups
        for powerup in powerups[:]:
            powerup.y += enemy_speed
            if powerup.top > SCREEN_HEIGHT:
                powerups.remove(powerup)
        
        # Check for collisions
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    explosion_sound.play()
                    break

        for powerup in powerups[:]:
            for bullet in bullets[:]:
                if powerup.colliderect(bullet):
                    powerups.remove(powerup)
                    bullets.remove(bullet)
                    player_health += 2
                    break

        # Draw everything
        screen.fill(BLACK)
        screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for powerup in powerups:
            screen.blit(powerup_image, powerup)
        
        # Draw score and health
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
        draw_text(f'Health: {player_health}', font, WHITE, screen, 10, 50)
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
