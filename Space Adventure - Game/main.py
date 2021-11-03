import pygame
import random

pygame.init()

screen_width = 600
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
game_over = False

# game object
rocket = pygame.image.load('rocket.png')
rocket_x = 270
rocket_y = 415
rocket_velocity = 5
rocket_velocity_x = 0
rocket_velocity_y = 0
enemy = pygame.image.load('ufo.png')
enemy_x = random.randint(50, screen_width - 50)
enemy_y = random.randint(50, screen_height - 50)
enemy_velocity = 5
enemy_velocity_x = enemy_velocity
enemy_velocity_y = 0

while not game_over:
    screen.fill((3, 252, 202))
    screen.blit(rocket, (rocket_x, rocket_y))
    screen.blit(enemy, (enemy_x, enemy_y))

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

        enemy_x = enemy_x + enemy_velocity_x

        if enemy_x >= screen_width - 64:
            enemy_x = screen_width - 64


        rocket_x = rocket_x + rocket_velocity_x
        rocket_y = rocket_y + rocket_velocity_y

    pygame.display.update()
