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
boss2_image = pygame.image.load('images/boss2.png').convert_alpha()  # New boss image

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
boss2_size = (200, 200)  # New boss size

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
boss2_image = pygame.transform.scale(boss2_image, boss2_size)  # New boss image

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

# New boss (boss2) attributes
boss2_rect = None
boss2_health = 200
boss2_shoot_delay = 250  # milliseconds (rapid fire)
boss2_last_shoot_time = 0

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
                        bullet_rect = bullet_image.get_rect(midbottom=player_rect.midtop)
                        bullets.append((bullet_rect, [0, -bullet_speed]))
                    shoot_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        # Bound player to screen
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = 0
        if player_rect.top < 0:
            player_rect.top = 0
        if player_rect.bottom > SCREEN_HEIGHT:
            player_rect.bottom = 0

        # Auto-fire for third player mode
        if is_player3:
            auto_fire_counter += 1
            if auto_fire_counter >= auto_fire_rate:
                auto_fire_counter = 0
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

        # Update bullet positions
        for bullet in bullets[:]:
            bullet[0].x += bullet[1][0]
            bullet[0].y += bullet[1][1]
            if bullet[0].bottom < 0:
                bullets.remove(bullet)

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_delay:
            enemy_rect = enemy_image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH-enemy_size[0]), -enemy_size[1]))
            enemies.append(enemy_rect)
            last_enemy_spawn_time = current_time

        # Spawn new type of enemy (enemy2) that shoots
        if current_time - last_enemy2_spawn_time > enemy2_spawn_delay:
            enemy2_rect = enemy2_image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH-enemy2_size[0]), -enemy2_size[1]))
            enemies.append(enemy2_rect)
            enemy2_shoot_delays.append(current_time + random.randint(1000, 3000))  # Random delay before enemy2 shoots
            last_enemy2_spawn_time = current_time

        # Spawn power-ups
        if current_time - last_powerup_spawn_time > powerup_spawn_delay:
            powerup_rect = powerup_image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH-powerup_size[0]), -powerup_size[1]))
            powerups.append(powerup_rect)
            last_powerup_spawn_time = current_time

        # Move enemies and check for collisions
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.colliderect(player_rect):
                enemies.remove(enemy)
                player_health -= 1
                explosion_sound.play()
                if player_health <= 0:
                    game_over = True
                    playing = False
            elif enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # Move new type of enemy (enemy2), make them shoot, and check for collisions
        for i, enemy2 in enumerate(enemy2s[:]):
            enemy2.y += enemy2_speed
            if enemy2.colliderect(player_rect):
                enemy2s.remove(enemy2)
                enemy2_shoot_delays.pop(i)
                player_health -= 1
                explosion_sound.play()
                if player_health <= 0:
                    game_over = True
                    playing = False
            elif enemy2.y > SCREEN_HEIGHT:
                enemy2s.remove(enemy2)
                enemy2_shoot_delays.pop(i)
            else:
                # Make enemy2 shoot bullets
                if current_time >= enemy2_shoot_delays[i]:
                    bullet_rect = bullet_enemy_image.get_rect(midbottom=enemy2.midbottom)
                    enemy2_bullets.append((bullet_rect, [0, enemy2_bullet_speed]))
                    enemy2_shoot_delays[i] = current_time + enemy2_shoot_delay

        # Move enemy2 bullets and check for collisions
        for bullet in enemy2_bullets[:]:
            bullet[0].x += bullet[1][0]
            bullet[0].y += bullet[1][1]
            if bullet[0].top > SCREEN_HEIGHT:
                enemy2_bullets.remove(bullet)
            elif bullet[0].colliderect(player_rect):
                enemy2_bullets.remove(bullet)
                player_health -= 1
                explosion_sound.play()
                if player_health <= 0:
                    game_over = True
                    playing = False

        # Move power-ups and check for collisions
        for powerup in powerups[:]:
            powerup.y += 5
            if powerup.colliderect(player_rect):
                powerups.remove(powerup)
                player_health += 1  # Increment player health
            elif powerup.y > SCREEN_HEIGHT:
                powerups.remove(powerup)

        # Update and handle ally movement and shooting
        if ally_rect:
            ally_rect.y -= 7  # Ally moves upward
            if ally_rect.y < 0:
                ally_rect = None
            else:
                ally_shot_count += 1
                if ally_shot_count % 10 == 0:
                    bullet_rect = bullet_image.get_rect(midbottom=ally_rect.midtop)
                    bullets.append((bullet_rect, [0, -bullet_speed]))

        # Boss spawning
        if score > 0 and score % 5000 == 0 and not boss_rect:
            boss_rect = boss_image.get_rect(center=(SCREEN_WIDTH // 2, -boss_size[1] // 2))

        # Move and handle boss actions
        if boss_rect:
            boss_rect.y += 1  # Boss moves down slowly
            if boss_rect.top >= 0:
                boss_rect.top = 0
            current_time = pygame.time.get_ticks()
            if current_time - boss_last_shoot_time > boss_shoot_delay:
                bullet_rect = bullet_enemy_image.get_rect(midbottom=boss_rect.midbottom)
                enemy2_bullets.append((bullet_rect, [0, enemy2_bullet_speed]))
                boss_last_shoot_time = current_time

            for bullet in bullets:
                if boss_rect.colliderect(bullet[0]):
                    bullets.remove(bullet)
                    boss_health -= 1
                    if boss_health <= 0:
                        boss_rect = None
                        boss_health = 50
                        score += 1000  # Increase score for defeating the boss

        # New boss (boss2) spawning
        if score > 0 and score % 10000 == 0 and not boss2_rect:
            boss2_rect = boss2_image.get_rect(center=(SCREEN_WIDTH // 2, -boss2_size[1] // 2))

        # Move and handle new boss (boss2) actions
        if boss2_rect:
            boss2_rect.y += 1  # Boss2 moves down slowly
            if boss2_rect.top >= 0:
                boss2_rect.top = 0
            current_time = pygame.time.get_ticks()
            if current_time - boss2_last_shoot_time > boss2_shoot_delay:
                bullet_rect = bullet_enemy_image.get_rect(midbottom=boss2_rect.midbottom)
                enemy2_bullets.append((bullet_rect, [0, enemy2_bullet_speed]))
                boss2_last_shoot_time = current_time

            for bullet in bullets:
                if boss2_rect.colliderect(bullet[0]):
                    bullets.remove(bullet)
                    boss2_health -= 1
                    if boss2_health <= 0:
                        boss2_rect = None
                        boss2_health = 200
                        score += 2000  # Increase score for defeating boss2

        # Update score
        score += 1

        # Draw everything
        screen.fill(BLACK)
        if is_player2:
            screen.blit(player2_image, player_rect)
        elif is_player3:
            screen.blit(player3_image, player_rect)
        else:
            screen.blit(player_image, player_rect)

        for bullet in bullets:
            screen.blit(bullet_image, bullet[0])
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for enemy2 in enemy2s:
            screen.blit(enemy2_image, enemy2)
        for bullet in enemy2_bullets:
            screen.blit(bullet_enemy_image, bullet[0])
        for powerup in powerups:
            screen.blit(powerup_image, powerup)
        if ally_rect:
            screen.blit(ally_image, ally_rect)
        if boss_rect:
            screen.blit(boss_image, boss_rect)
        if boss2_rect:
            screen.blit(boss2_image, boss2_rect)

        # Draw player health
        draw_text(f'Health: {player_health}', font, WHITE, screen, 10, 10)
        # Draw score
        draw_text(f'Score: {score}', font, WHITE, screen, SCREEN_WIDTH - 150, 10)

        pygame.display.flip()
        clock.tick(60)  # Cap the frame rate

# Quit Pygame
pygame.quit()
