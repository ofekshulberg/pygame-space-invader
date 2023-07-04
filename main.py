import pygame
from pygame import mixer
import random
import math

pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Load and play background music
mixer.music.load('Steven Universe.wav')
mixer.music.play(-1)

# Load player image and set initial position
player_img = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0

# Initialize lists for enemies' images, positions, and movements
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

# Create enemy instances with random positions and movements
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemy_x.append(random.randint(10, 735))
    enemy_y.append(random.randint(10, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(10)

# Load bullet image and set initial position and movement
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 8
bullet_state = "ready"

# Initialize score value and set font for rendering text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 5
text_y = 5

# Set font for rendering game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function to display the score on the screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))

# Function to display "GAME OVER" text on the screen
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

# Function to draw the player's spaceship on the screen
def player(x, y):
    screen.blit(player_img, (x, y))

# Function to draw an enemy on the screen
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

# Function to fire a bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

# Function to check collision between enemy and bullet
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:

    # Fill the screen with a green color and draw the background image
    screen.fill((0, 220, 100))
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bullet sound.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Update player position
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy logic
    for i in range(num_of_enemies):

        # Game over condition
        if enemy_y[i] > 420:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        # Update enemy positions
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Check for collision between enemy and bullet
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            impact_sound = mixer.Sound('impact.wav')
            impact_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(20, 735)
            enemy_y[i] = random.randint(20, 150)

        # Draw enemy on the screen
        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet logic
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Draw player and score on the screen
    player(player_x, player_y)
    show_score(text_x, text_y)

    # Update the display
    pygame.display.update()