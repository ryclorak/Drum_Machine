# from freecodecamp tutorial: https://www.youtube.com/watch?v=F3J3PZj0zi0
import pygame
from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0) # active
purple = (128, 0, 128) # rim around beat boxes

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drummasheen')
label_font = pygame.font.Font('FiraSans-Medium.ttf', 32)

fps = 60
timer = pygame.time.Clock()
num_instruments = 6
num_beats = 8
boxes = []
clicked =  [[-1 for _ in range(num_beats)] for _ in range(num_instruments)]
# this fills a list full of -1, to show whether a box was clicked


def draw_grid(clicks):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5) 
    # 0,0 is top left corner, 200 is width, 5 is how wide edges are
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    # HEIGHT-200 prevents crisscross
    boxes = []
    colors = [gray, white, gray] # idk why this and no black

    # TODO: make this programmatically set, vary heights by num_instruments
    clap_text       = label_font.render('Clap', True, white) # True for anti-alias
    screen.blit(clap_text,      (30, 30)) # blit displays on screen, (X,Y) location
    hi_hat_text     = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text,    (30, 130))
    crash_text      = label_font.render('Crash', True, white)
    screen.blit(crash_text,     (30, 230))
    snare_text      = label_font.render('Snare', True, white)
    screen.blit(snare_text,     (30, 330))
    floor_tom_text  = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30, 430))
    bass_text       = label_font.render('Bass Drum', True, white)
    screen.blit(bass_text,      (30, 530))

    for i in range(num_instruments):
        # draw lines separating instrument names
        # args: screen, color, start pos (tuple), end pos (tuple), line thickness (default 1)
        pygame.draw.line(screen, gray, (0, i*100), (195, i*100), 3)

    for i in range(num_beats):
        for j in range(num_instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            # start at beat (at 200), calc available space on screen, update based on num_instr/beats
            rect = pygame.draw.rect(screen, color, \
                [i * ((WIDTH - 200) // num_beats) + 205, \
                (j * 100) + 5, \
                ((WIDTH - 200) // num_beats) - 10, \
                ((HEIGHT - 200) // num_instruments)], \
                0, 3)
            pygame.draw.rect(screen, purple, \
                [i * ((WIDTH - 200) // num_beats) + 200, \
                (j * 100), \
                ((WIDTH - 200) // num_beats), \
                ((HEIGHT - 200) // num_instruments)], \
                5, 5)
            # 5 is for rounded rectangle, 5 is thickness of lines; this is the outline rectangle:
            pygame.draw.rect(screen, black, \
                [i * ((WIDTH - 200) // num_beats) + 200, \
                (j * 100), \
                ((WIDTH - 200) // num_beats), \
                ((HEIGHT - 200) // num_instruments)], \
                2, 5)
            # return each beat, plus its coordinates, will use for collision detection
            boxes.append((rect, (i, j)))
    return boxes


# GAME LOOP
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked)

    # check keyboard/mouse input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                # scalable, check whether mouse click collides with box
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

    pygame.display.flip()

pygame.quit() # just in case
