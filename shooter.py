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
player3_image = pygame.image.load('images/player3.png').convert_alpha()  # New player image for third mode
bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
enemy_image = pygame.image.load('images/enemy.png').convert_alpha()
enemy2_image = pygame.image.load('images/enemy2.png').convert_alpha()
bullet_enemy_image = pygame.image.load('images/bullet_enemy.png').convert_alpha()
powerup_image = pygame.image.load('images/health.png').convert_alpha()
ally_image = pygame.image.load('images/ally.png').convert_alpha()
boss_image = pygame.image.load('images/boss1.png').convert_alpha()
boss2_image = pygame.image.load('images/boss2.png').convert_alpha()  # Load the second boss image

# Resize images
player_size = (50, 50)
player2_size = (60, 60)  # Adjust size if needed
player3_size = (70, 70)  # New size for third player mode
bullet_size = (10, 20)
enemy_size = (50, 50)
powerup_size = (30, 30)
enemy2_size = (60, 60)
bullet_enemy_size = (10, 20)
ally_size = (50, 50)
boss_size = (100, 100)  # Boss size
boss2_size = (150, 150)  # Second boss size

player_image = pygame.transform.scale(player_image, player_size)
player2_image = pygame.transform.scale(player2_image, player2_size)
player3_image = pygame.transform.scale(player3_image, player3_size)  # New player image
bullet_image = pygame.transform.scale(bullet_image, bullet_size)
enemy_image = pygame.transform.scale(enemy_image, enemy_size)
enemy2_image = pygame.transform.scale(enemy2_image, enemy2_size)
bullet_enemy_image = pygame.transform.scale(bullet_enemy_image, bullet_enemy_size)
powerup_image = pygame.transform.scale(powerup_image, powerup_size)
ally_image = pygame.transform.scale(ally_image, ally_size)
boss_image = pygame.transform.scale(boss_image, boss_size)
boss2_image = pygame.transform.scale(boss2_image, boss2_size)  # Resize the second boss image

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
is_player3 = False  # New variable for third mode

# Bullet attributes
bullets = []
bullet_speed = 7
auto_fire_rate = 5  # Bullet firing rate for third mode (in frames)
auto_fire_counter = 0  # Counter for auto fire

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
boss_health = 50
boss_shoot_delay = 500  # milliseconds
boss_last_shoot_time = 0

# Second Boss attributes
boss2_rect = None
boss2_health = 100
boss2_shoot_delay = 300  # milliseconds
boss2_last_shoot_time = 0
boss2_speed = 1  # Slower movement speed for the second boss

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
                    is_player3 = False  # Reset third player mode
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
                    is_player3 = False  # Reset third player mode
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
                    elif is_player3:
                        # Player 3 spread fire in all directions
                        spread_angle = 360  # Full circle
                        number_of_bullets = 8
                        angle_step = spread_angle / number_of_bullets
                        for i in range(number_of_bullets):
                            angle = i * angle_step
                            radians = math.radians(angle)
                            bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                            bullet_velocity = [bullet_speed * math.cos(radians), bullet_speed * math.sin(radians)]
                            bullets.append((bullet_rect, bullet_velocity))
                    else:
                        # Regular shooting for Player 1
                        bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                        bullets.append((bullet_rect, [0, -bullet_speed]))
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT]:
            player_rect.move_ip(player_speed, 0)
        if keys[pygame.K_UP]:
            player_rect.move_ip(0, -player_speed)
        if keys[pygame.K_DOWN]:
            player_rect.move_ip(0, player_speed)

        # Keep player within screen bounds
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > SCREEN_HEIGHT:
            player_rect.bottom = SCREEN_HEIGHT

        # Update auto fire counter and fire bullets for third player mode
        if is_player3:
            auto_fire_counter += 1
            if auto_fire_counter >= auto_fire_rate:
                auto_fire_counter = 0
                # Auto fire logic (similar to manual fire)
                spread_angle = 360  # Full circle
                number_of_bullets = 8
                angle_step = spread_angle / number_of_bullets
                for i in range(number_of_bullets):
                    angle = i * angle_step
                    radians = math.radians(angle)
                    bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                    bullet_velocity = [bullet_speed * math.cos(radians), bullet_speed * math.sin(radians)]
                    bullets.append((bullet_rect, bullet_velocity))
                shoot_sound.play()

        # Update bullets
        for bullet in bullets[:]:
            bullet[0].move_ip(bullet[1])
            if bullet[0].bottom < 0 or bullet[0].top > SCREEN_HEIGHT or bullet[0].left < 0 or bullet[0].right > SCREEN_WIDTH:
                bullets.remove(bullet)

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_delay:
            enemy_rect = enemy_image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), 0))
            enemies.append(enemy_rect)
            last_enemy_spawn_time = current_time

        # Spawn extra enemies
        if current_time - last_enemy2_spawn_time > enemy2_spawn_delay:
            enemy2_rect = enemy2_image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), 0))
            enemies.append(enemy2_rect)
            enemy2_shoot_delays.append(current_time + enemy2_shoot_delay)  # Initialize the shoot delay for the enemy
            last_enemy2_spawn_time = current_time

        # Update enemies
        for enemy in enemies[:]:
            enemy.move_ip(0, enemy_speed)
            if enemy.top > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # Enemy shooting
        for i, enemy2_rect in enumerate(enemy2s):
            if current_time > enemy2_shoot_delays[i]:
                enemy2_bullet_rect = bullet_enemy_image.get_rect(midtop=enemy2_rect.midbottom)
                enemy2_bullets.append((enemy2_bullet_rect, [0, enemy2_bullet_speed]))
                enemy2_shoot_delays[i] = current_time + enemy2_shoot_delay  # Reset shoot delay

        # Update enemy bullets
        for bullet in enemy2_bullets[:]:
            bullet[0].move_ip(bullet[1])
            if bullet[0].top > SCREEN_HEIGHT:
                enemy2_bullets.remove(bullet)

        # Spawn power-ups
        if current_time - last_powerup_spawn_time > powerup_spawn_delay:
            powerup_rect = powerup_image.get_rect(midbottom=(random.randint(0, SCREEN_WIDTH), 0))
            powerups.append(powerup_rect)
            last_powerup_spawn_time = current_time

        # Update power-ups
        for powerup in powerups[:]:
            powerup.move_ip(0, enemy_speed)
            if powerup.top > SCREEN_HEIGHT:
                powerups.remove(powerup)

        # Spawn ally at 5,000 points
        if score >= 5000 and ally_rect is None:
            ally_rect = ally_image.get_rect(center=(SCREEN_WIDTH // 2, 100))

        # Spawn first boss at 2,000 points
        if score >= 2000 and boss_rect is None:
            boss_rect = boss_image.get_rect(midbottom=(SCREEN_WIDTH // 2, 0))
            boss_health = 50  # Reset boss health

        # Spawn second boss at 10,000 points
        if score >= 10000 and boss2_rect is None:
            boss2_rect = boss2_image.get_rect(midbottom=(SCREEN_WIDTH // 2, 0))
            boss2_health = 100  # Reset second boss health

        # Update ally position and shooting
        if ally_rect:
            ally_rect.move_ip(0, 1)  # Move ally downwards slowly
            if ally_rect.bottom > SCREEN_HEIGHT:
                ally_rect.bottom = SCREEN_HEIGHT  # Keep ally within bounds

            ally_shot_count += 1
            if ally_shot_count >= 30:  # Ally shoots every 30 frames
                ally_bullet_rect = bullet_image.get_rect(midbottom=ally_rect.midtop)
                bullets.append((ally_bullet_rect, [0, -bullet_speed]))
                ally_shot_count = 0

        # Update boss position and shooting
        if boss_rect:
            boss_rect.move_ip(0, 1)  # Move boss downwards slowly
            if boss_rect.bottom > SCREEN_HEIGHT // 2:
                boss_rect.bottom = SCREEN_HEIGHT // 2  # Keep boss within bounds

            if current_time - boss_last_shoot_time > boss_shoot_delay:
                boss_bullet_rect = bullet_enemy_image.get_rect(midtop=boss_rect.midbottom)
                enemy2_bullets.append((boss_bullet_rect, [0, enemy2_bullet_speed]))
                boss_last_shoot_time = current_time

        # Update second boss position and shooting
        if boss2_rect:
            boss2_rect.move_ip(boss2_speed, 0)  # Move second boss horizontally
            if boss2_rect.left < 0 or boss2_rect.right > SCREEN_WIDTH:
                boss2_speed = -boss2_speed  # Reverse direction if hitting screen bounds

            if current_time - boss2_last_shoot_time > boss2_shoot_delay:
                for angle in range(0, 360, 45):  # Shoot in 8 directions (every 45 degrees)
                    radians = math.radians(angle)
                    boss2_bullet_rect = bullet_enemy_image.get_rect(midtop=boss2_rect.midbottom)
                    bullet_velocity = [enemy2_bullet_speed * math.cos(radians), enemy2_bullet_speed * math.sin(radians)]
                    enemy2_bullets.append((boss2_bullet_rect, bullet_velocity))
                boss2_last_shoot_time = current_time

        # Check collisions
        for bullet in bullets[:]:
            if player_rect.colliderect(bullet[0]):
                player_health -= 1
                bullets.remove(bullet)
                explosion_sound.play()
                if player_health <= 0:
                    playing = False
                    game_over = True

        for enemy in enemies[:]:
            if player_rect.colliderect(enemy):
                player_health -= 1
                enemies.remove(enemy)
                explosion_sound.play()
                if player_health <= 0:
                    playing = False
                    game_over = True

        for powerup in powerups[:]:
            if player_rect.colliderect(powerup):
                player_health += 1
                powerups.remove(powerup)

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet[0].colliderect(enemy):
                    score += 100
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    explosion_sound.play()
                    break

        for bullet in bullets[:]:
            if boss_rect and bullet[0].colliderect(boss_rect):
                boss_health -= 1
                bullets.remove(bullet)
                explosion_sound.play()
                if boss_health <= 0:
                    boss_rect = None
                    score += 1000

        for bullet in bullets[:]:
            if boss2_rect and bullet[0].colliderect(boss2_rect):
                boss2_health -= 1
                bullets.remove(bullet)
                explosion_sound.play()
                if boss2_health <= 0:
                    boss2_rect = None
                    score += 2000

        # Draw everything
        screen.fill(BLACK)
        screen.blit(player_image, player_rect)

        for bullet in bullets:
            screen.blit(bullet_image, bullet[0])

        for enemy in enemies:
            screen.blit(enemy_image, enemy)

        for powerup in powerups:
            screen.blit(powerup_image, powerup)

        if ally_rect:
            screen.blit(ally_image, ally_rect)

        if boss_rect:
            screen.blit(boss_image, boss_rect)

        if boss2_rect:
            screen.blit(boss2_image, boss2_rect)

        draw_text(f'Score: {score}', font, WHITE, screen, 10, 10)
        draw_text(f'Health: {player_health}', font, WHITE, screen, 10, 40)

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
