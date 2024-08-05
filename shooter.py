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
boss_size = (100, 100)  # Boss size

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
boss_health = 10
boss_shoot_delay = 500  # milliseconds
boss_last_shoot_time = 0

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

        # Spawn boss if score reaches 100
        if score >= 100 and boss_rect is None:
            boss_rect = boss_image.get_rect(center=(SCREEN_WIDTH // 2, -boss_size[1]))

        # Spawn ally if score >= 40 and no boss is present
        if score >= 40 and ally_rect is None and boss_rect is None:
            ally_rect = ally_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - ally_size[0]), 0))

        # Update ally position
        if ally_rect:
            ally_rect.y += enemy_speed
            if ally_rect.top > SCREEN_HEIGHT:
                ally_rect = None  # Remove ally if it goes off screen

        # Enemy2 shooting logic
        for i, enemy2 in enumerate(enemy2s[:]):
            if current_time - enemy2_shoot_delays[i] > enemy2_shoot_delay:  # Reduced shooting rate
                enemy2_bullet_rect = bullet_enemy_image.get_rect(midtop=enemy2.midbottom)
                enemy2_bullets.append(enemy2_bullet_rect)
                enemy2_shoot_delays[i] = current_time  # Update the last shoot time for this enemy2

        # Spawn power-ups
        if current_time - last_powerup_spawn_time > powerup_spawn_delay:
            powerup_rect = powerup_image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - powerup_size[0]), 0))
            powerups.append(powerup_rect)
            last_powerup_spawn_time = current_time

        # Move bullets
        for bullet, velocity in bullets[:]:
            bullet.x += velocity[0]
            bullet.y += velocity[1]
            if bullet.bottom < 0 or bullet.left < 0 or bullet.right > SCREEN_WIDTH:
                bullets.remove((bullet, velocity))
        
        # Move enemy bullets
        for enemy_bullet in enemy2_bullets[:]:
            enemy_bullet.y += enemy2_bullet_speed
            if enemy_bullet.top > SCREEN_HEIGHT:
                enemy2_bullets.remove(enemy_bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_health -= 1
                if player_health == 0:
                    game_over = True
                    playing = False

        # Move extra enemies
        for enemy2 in enemy2s[:]:
            enemy2.y += enemy2_speed
            if enemy2.top > SCREEN_HEIGHT:
                enemy2s.remove(enemy2)  # Don't reduce player health if enemy2 escapes

        # Move power-ups
        for powerup in powerups[:]:
            powerup.y += enemy_speed
            if powerup.top > SCREEN_HEIGHT:
                powerups.remove(powerup)

        # Move ally
        if ally_rect:
            ally_rect.y += enemy_speed
            if ally_rect.top > SCREEN_HEIGHT:
                ally_rect = None  # Remove ally if it goes off screen

        # Move boss and make it shoot
        if boss_rect:
            boss_rect.y += enemy_speed
            if boss_rect.top > SCREEN_HEIGHT // 4:
                # Boss shoots in all directions
                if current_time - boss_last_shoot_time > boss_shoot_delay:
                    boss_last_shoot_time = current_time
                    # Shoot in 8 directions
                    for angle in range(0, 360, 45):
                        radians = math.radians(angle)
                        bullet_rect = bullet_image.get_rect(midbottom=boss_rect.center)
                        bullet_velocity = [bullet_speed * math.cos(radians), bullet_speed * math.sin(radians)]
                        bullets.append((bullet_rect, bullet_velocity))

        # Check for collisions
        for enemy in enemies[:]:
            for bullet, _ in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove((bullet, _))
                    score += 1
                    explosion_sound.play()
                    break

        for enemy2 in enemy2s[:]:
            for bullet, _ in bullets[:]:
                if enemy2.colliderect(bullet):
                    enemy2s.remove(enemy2)
                    bullets.remove((bullet, _))
                    score += 2  # Double the points
                    explosion_sound.play()
                    break

        for powerup in powerups[:]:
            for bullet, _ in bullets[:]:
                if powerup.colliderect(bullet):
                    powerups.remove(powerup)
                    bullets.remove((bullet, _))
                    player_health += 2
                    break

        if boss_rect:
            for bullet, _ in bullets[:]:
                if boss_rect.colliderect(bullet):
                    boss_health -= 1
                    bullets.remove((bullet, _))
                    if boss_health <= 0:
                        boss_rect = None
                        score += 100  # Add points for defeating the boss
                    break

        for enemy_bullet in enemy2_bullets[:]:
            if enemy_bullet.colliderect(player_rect):
                enemy2_bullets.remove(enemy_bullet)
                player_health -= 1
                if player_health == 0:
                    game_over = True
                    playing = False

        # Check for ally collisions
        if ally_rect:
            for bullet, _ in bullets[:]:
                if ally_rect.colliderect(bullet):
                    bullets.remove((bullet, _))
                    ally_shot_count += 1
                    if ally_shot_count >= 3:
                        ally_rect = None
                        player_health -= 1
                        ally_shot_count = 0
                    break

        # Transform player based on health
        if player_health >= 10 and not is_player2:
            is_player2 = True
            player_rect = player2_image.get_rect(center=player_rect.center)
        elif player_health < 10 and is_player2:
            is_player2 = False
            player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

        # Draw everything
        screen.fill(BLACK)
        screen.blit(player2_image if is_player2 else player_image, player_rect)
        for bullet, _ in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for enemy2 in enemy2s:
            screen.blit(enemy2_image, enemy2)
        for enemy_bullet in enemy2_bullets:
            screen.blit(bullet_enemy_image, enemy_bullet)
        for powerup in powerups:
            screen.blit(powerup_image, powerup)
        if ally_rect:
            screen.blit(ally_image, ally_rect)
        if boss_rect:
            screen.blit(boss_image, boss_rect)
        
        # Draw score and health
        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
        draw_text(f'Health: {player_health}', font, WHITE, screen, 10, 50)
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
