# from freecodecamp tutorial: https://www.youtube.com/watch?v=F3J3PZj0zi0
import pygame
from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (127, 127, 127)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drummasheen')
label_font = pygame.font.Font('FiraSans-Medium.ttf', 32)

fps = 60
timer = pygame.time.Clock()

run = True
while run:
    timer.tick(fps)
    screen.fill(black)

    # check keyboard/mouse input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
