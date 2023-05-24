import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Space Invader Background.jpg')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy1-ship.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5  # Adjust this value to change the bullet speed
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Power-up
power_upImg = pygame.image.load('power-up.png')
power_upX = random.randint(0, 736)
power_upY = -50
power_upY_change = 0.5  # speed of the powerup falls
power_up_state = "ready"
power_up_duration = 3  # Power-up duration in seconds
power_up_start_time = None

# Enhanced Firepower
enhanced_firepower = False
enhanced_firepower_bullet_speed = 30  # Bullet speed during enhanced firepower

# Original Bullet Speed
original_bullet_speed = 2.5

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def spawn_power_up():
    global power_up_state, power_upX, power_upY, power_up_start_time
    power_upX = random.randint(0, 736)
    power_upY = -50
    power_up_state = "ready"
    power_up_start_time = None


def show_power_up(x, y):
    screen.blit(power_upImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = .5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Power-up Movement
    if power_up_state == "ready":
        power_upY += power_upY_change
        if power_upY >= 600:
            spawn_power_up()

    # Power-up Collision
    power_up_collision = isCollision(power_upX, power_upY, playerX, playerY)
    if power_up_collision:
        enhanced_firepower = True
        power_up_state = "consumed"
        power_up_start_time = pygame.time.get_ticks()

    # Enhanced Firepower Effect
    if enhanced_firepower:
        if power_up_start_time is not None:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - power_up_start_time) / 1000  # Convert to seconds
            remaining_time = power_up_duration - elapsed_time

            if elapsed_time <= power_up_duration:
                # Implement the logic for enhanced firepower here
                # Adjust bullet speed
                bulletY_change = enhanced_firepower_bullet_speed

                # Display remaining time
                timer_font = pygame.font.Font('freesansbold.ttf', 24)
                timer_text = timer_font.render("Power-up Time: " + str(int(remaining_time)), True, (255, 255, 255))
                screen.blit(timer_text, (10, 40))
            else:
                enhanced_firepower = False
                power_up_start_time = None  # Reset power-up start time
                bulletY_change = original_bullet_speed # Reset bullet speed

    # Draw Power-up
    if power_up_state == "ready":
        show_power_up(power_upX, power_upY)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
