import pygame
import random
import math

pygame.init()

screen_width = 700
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Adventure")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont('arial',30)

#images
rocket = pygame.image.load('rocket.png')
enemy = pygame.image.load('ufo.png')
bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.rotate(bullet,45)
backgrounimg = pygame.image.load('backgroundimg.jpg')
backgrounimg = pygame.transform.scale(backgrounimg,(screen_width,screen_height))

def fire_bullet(bulletx,bullety):
    screen.blit(bullet,(bulletx,bullety))

def hit(enemyX,enemyY,x,y):
    distance = math.sqrt((math.pow(enemyX-x,2)) + (math.pow(enemyY-y,2)))
    if distance <= 25:
        return True
    else: return False

def textScreen(text,color,x,y):
    dialogue = font.render(text,True,color)
    screen.blit(dialogue,(x,y))


def welcome():
    v = False
    wcimg = pygame.image.load('Welcome.png')
    wcimg = pygame.transform.scale(wcimg,(screen_width,screen_height))
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    while not v:
        screen.fill((255,255,255))
        screen.blit(wcimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    v = True

        pygame.display.update()
    game_loop()

def game_loop():
    bullet_sound = pygame.mixer.Sound('fire.mp3')
    enemy_down = pygame.mixer.Sound('enemy_down.mp3')

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)
    game_over = False
    game_quit = False
    # game object
    rocket_x = 270
    rocket_y = 415
    rocket_velocity = 0.5
    rocket_velocity_x = 0
    rocket_velocity_y = 0
    score = 0

    enemy_xlist = []
    enemy_ylist = []
    enemy_velocity_xlist = []
    number_of_enemy = 5
    enemy_velocity = 0.3

    for i in range(number_of_enemy):
        enemy_xlist.append(random.randint(50, screen_width - 50))
        enemy_ylist.append(random.randint(50, 100))
        enemy_velocity_xlist.append(enemy_velocity)

    bullet_x = 0
    bullet_y = 0
    bullet_velocity_y = 0.7
    Fire = False

    while not game_over:
        screen.fill((255,255,255))
        screen.blit(backgrounimg,(0,0))
        screen.blit(rocket, (rocket_x, rocket_y))
        textScreen("Your Score : " + str(score), (255,255,255), 0, 0)

        if game_quit:
            gameoverimg = pygame.image.load('gameoverimage.png')
            gameoverimg = pygame.transform.scale(gameoverimg,(screen_width,screen_height))
            screen.blit(gameoverimg,(0,0))
            textScreen("Your Score : " + str(score), (255, 0, 0), 240, 240)
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
                    if event.key == pygame.K_RIGHT:
                        rocket_velocity_x = + rocket_velocity
                    if event.key == pygame.K_UP:
                        rocket_velocity_y = - rocket_velocity
                    if event.key == pygame.K_DOWN:
                        rocket_velocity_y = + rocket_velocity
                    if event.key == pygame.K_SPACE:
                        bullet_sound.play()
                        Fire = True
                        bullet_x = rocket_x + 20
                        bullet_y = rocket_y

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        rocket_velocity_x = 0
                        rocket_velocity_y = 0


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
                screen.blit(enemy, (enemy_xlist[i], enemy_ylist[i]))
                enemy_xlist[i] = enemy_xlist[i] + enemy_velocity_xlist[i]

                if enemy_xlist[i] >= screen_width - 64:
                    enemy_xlist[i] = screen_width - 64
                    enemy_ylist[i] = enemy_ylist[i] + 40
                    enemy_velocity_xlist[i] = - enemy_velocity

                elif enemy_xlist[i] <= 0:
                    enemy_xlist[i] = 0
                    enemy_ylist[i] = enemy_ylist[i] + 40
                    enemy_velocity_xlist[i] = + enemy_velocity

                isHit = hit(enemy_xlist[i],enemy_ylist[i],bullet_x,bullet_y)
                if isHit:
                    score += 1
                    enemy_down.play()
                    bullet_y = rocket_x + 20
                    enemy_xlist[i] = random.randint(50, screen_width - 50)
                    enemy_ylist[i] = random.randint(50, 100)
                    Fire = False



            if Fire:
                fire_bullet(bullet_x,bullet_y)
                bullet_y -= bullet_velocity_y

            for i in range(number_of_enemy):
                r_hit = hit(enemy_xlist[i],enemy_ylist[i],rocket_x,rocket_y)
                if r_hit:
                    game_quit = True
                    pygame.mixer.music.load('gameover.wav')
                    pygame.mixer.music.play()
                    break

        pygame.display.update()

welcome()
