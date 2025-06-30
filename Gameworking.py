import pygame
import random
import math
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Comeback2.0")

icon = pygame.image.load('arcade.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background.png')
mixer.music.load("background.wav")
mixer.music.play(-1)


playerImg = pygame.image.load("project.png")
playerX = 270
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemy = 10

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load("Bhoot.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load("Bull.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "Ready"

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
over_font = pygame.font.Font("freesansbold.ttf", 64)
button_font = pygame.font.Font("freesansbold.ttf", 24)  

game_over = False
paused = False

def showscore(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

def draw_buttons():
    pygame.draw.ellipse(screen, (0, 255, 0), (550, 10, 100, 40))  
    pause_text = button_font.render("Pause", True, (0, 0, 0))
    screen.blit(pause_text, (550 + 25, 18))  

    pygame.draw.ellipse(screen, (255, 0, 0), (670, 10, 100, 40))  
    restart_text = button_font.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, (670 + 15, 18)) 

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def reset_game():
    global score, bullet_state, bulletX, bulletY, playerX, playerX_change, enemyX, enemyY
    global game_over, paused
    score = 0
    bullet_state = "Ready"
    bulletX = 0
    bulletY = 480
    playerX = 370
    playerX_change = 0
    enemyX = [random.randint(0, 736) for _ in range(no_of_enemy)]
    enemyY = [random.randint(50, 150) for _ in range(no_of_enemy)]
    game_over = False
    paused = False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
        
            if 550 <= mouseX <= 650 and 10 <= mouseY <= 50:
                paused = not paused
            
            if 670 <= mouseX <= 770 and 10 <= mouseY <= 50:
                reset_game()

       
        if event.type == pygame.KEYDOWN:
            if not paused and not game_over:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.3
                if event.key == pygame.K_SPACE and bullet_state == "Ready":
                    bullet_sound = mixer.Sound("explosion.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            # Restart with space bar
            if event.key == pygame.K_SPACE and game_over:
                reset_game()

        if event.type == pygame.KEYUP and not paused:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if paused:
        pause_text = over_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (250, 250))
        draw_buttons()
        pygame.display.update()
        continue

    if game_over:
        game_over_text()
        draw_buttons()
        pygame.display.update()
        continue

    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(no_of_enemy):
        if enemyY[i] > 200:
            for j in range(no_of_enemy):
                enemyY[j] = 2000
            game_over = True
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showscore(textX, textY)



    draw_buttons()

    pygame.display.update()
