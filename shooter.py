import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Shooting Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load images
player_image = pygame.Surface((50, 30))
player_image.fill(WHITE)
bullet_image = pygame.Surface((5, 10))
bullet_image.fill(RED)
enemy_image = pygame.Surface((50, 30))
enemy_image.fill(GREEN)

# Player attributes
player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
player_speed = 5

# Bullet attributes
bullets = []
bullet_speed = 7

# Enemy attributes
enemies = []
enemy_speed = 3
enemy_spawn_delay = 1000  # milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                bullets.append(bullet_rect)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += player_speed
    
    # Spawn enemies
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_delay:
        enemy_rect = enemy_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - 50), 0))
        enemies.append(enemy_rect)
        last_enemy_spawn_time = current_time

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
    
    # Check for collisions
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    # Draw everything
    screen.fill(BLACK)
    screen.blit(player_image, player_rect)
    for bullet in bullets:
        screen.blit(bullet_image, bullet)
    for enemy in enemies:
        screen.blit(enemy_image, enemy)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
