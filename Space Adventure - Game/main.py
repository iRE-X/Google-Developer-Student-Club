import pygame
import random
import math

pygame.init()

#Screen Settings
screen_width = 700
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#images
rocket = pygame.image.load('rocket.png')
enemy = pygame.image.load('ufo.png')
bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.rotate(bullet, 45)
backgroundimg = pygame.image.load('backgroundimg.jpg')
backgroundimg = pygame.transform.scale(backgroundimg,(screen_width,screen_height))


font = pygame.font.SysFont('arial', 30)
sensitivity = 25

def fire_bullet(x,y):
    screen.blit(bullet,(x,y))

def isCollision(enemyX,enemyY,x,y):
    distance = math.sqrt(math.pow(enemyX+20-x,2) + math.pow(enemyY+20-y,2))
    if distance <= sensitivity:
        return True
    else: return False

def textScreen(text,color,x,y):
    screenText = font.render(text,True,color)
    screen.blit(screenText,(x,y))

def welcome():
    greeting = True
    screen.fill((255, 255, 255))
    welcomeimg = pygame.image.load('Welcome.png')
    welcomeimg = pygame.transform.scale(welcomeimg, (screen_width, screen_height))
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    while greeting:
        screen.fill((255, 255, 255))
        screen.blit(welcomeimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    greeting = False
        pygame.display.update()
    game_loop()


def game_loop():
    fire_sound = pygame.mixer.Sound('fire.mp3')
    enemy_down = pygame.mixer.Sound('enemy_down.mp3')


    game_over = False
    game_quit = False
    score = 0

    # game object

    rocket_x = 280
    rocket_y = 400
    rocket_velocity = 0.5
    rocket_velocity_x = 0
    rocket_velocity_y = 0


    enemy_velocity = 0.4
    enemy_xlist = []
    enemy_ylist = []
    enemy_velocity_xlist = []
    number_of_enemy = 7

    for i in range(number_of_enemy):
        enemy_xlist.append(random.randint(50, screen_width - 50))
        enemy_ylist.append(random.randint(50, 100))
        enemy_velocity_xlist.append(enemy_velocity)

    bullet_x = 0
    bullet_y = 0
    bullet_velocity_y = -0.8
    fire = False
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)

    while not game_over:
        screen.fill((3, 252, 202))
        screen.blit(backgroundimg,(0,0))
        textScreen("Your Score : " + str(score), (255,255,255), 0, 0)
        screen.blit(rocket, (rocket_x, rocket_y))


        if game_quit:
            screen.fill((255,255,255))
            gameoverimage = pygame.image.load('gameoverimage.png')
            gameoverimage = pygame.transform.scale(gameoverimage,(screen_width,screen_height))
            screen.blit(gameoverimage,(0,0))
            textScreen("Your Score : "+str(score),(255,0,0),220,220)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        rocket_velocity_x = - rocket_velocity
                        rocket_velocity_y = 0
                    if event.key == pygame.K_RIGHT:
                        rocket_velocity_x = + rocket_velocity
                        rocket_velocity_y = 0
                    if event.key == pygame.K_UP:
                        rocket_velocity_y = - rocket_velocity
                        rocket_velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        rocket_velocity_y = + rocket_velocity
                        rocket_velocity_x = 0
                    if event.key == pygame.K_SPACE:
                        fire_sound.play()
                        fire = True
                        bullet_x = rocket_x + 20
                        bullet_y = rocket_y
                if event.type == pygame.KEYUP:
                    rocket_velocity_x = 0
                    rocket_velocity_y = 0


            #rocket movement
            rocket_x = rocket_x + rocket_velocity_x
            rocket_y = rocket_y + rocket_velocity_y
            if rocket_x >= screen_width - 64:
                rocket_x = screen_width - 64
            elif rocket_x <= 0:
                rocket_x = 0
            if rocket_y >= screen_height - 64:
                rocket_y = screen_height - 64
            elif rocket_y <= 0:
                rocket_y = 0

            for i in range(number_of_enemy):
                #enemy movement
                screen.blit(enemy, (enemy_xlist[i], enemy_ylist[i]))

                enemy_xlist[i] = enemy_xlist[i] + enemy_velocity_xlist[i]
                if enemy_xlist[i] >= screen_width - 64:
                    enemy_xlist[i] = screen_width - 64
                    enemy_velocity_xlist[i] = - enemy_velocity
                    enemy_ylist[i]  += 40
                elif enemy_xlist[i] <= 0:
                    enemy_xlist[i] = 0
                    enemy_velocity_xlist[i] = enemy_velocity
                    enemy_ylist[i] += 40

                # handeling the collision between bullet and enemy
                collision = isCollision(enemy_xlist[i], enemy_ylist[i], bullet_x, bullet_y)
                if collision:
                    enemy_down.play()
                    bullet_y = rocket_y
                    fire = False
                    enemy_ylist[i] = random.randint(50, screen_width - 50)
                    enemy_ylist[i] = random.randint(50, 150)
                    score = score + 1

            #bullet movement
            if fire:
                fire_bullet(bullet_x,bullet_y)
                bullet_y += bullet_velocity_y

            for i in range(number_of_enemy):
                game_quit = isCollision(enemy_xlist[i], enemy_ylist[i], rocket_x, rocket_y)
                if game_quit:
                    pygame.mixer.music.load('gameover.wav')
                    pygame.mixer.music.play()
                    break

        pygame.display.update()

welcome()
