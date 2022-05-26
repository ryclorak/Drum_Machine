# from freecodecamp tutorial: https://www.youtube.com/watch?v=F3J3PZj0zi0
from math import floor
import pygame
from pygame import mixer

pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0) # active
purple = (128, 0, 128) # rim around beat boxes
blue = (0, 255, 255) # for active beat

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drummasheen')
label_font = pygame.font.Font('FiraSans-Medium.ttf', 32)
medium_font = pygame.font.Font('FiraSans-Medium.ttf', 24)

fps = 60
timer = pygame.time.Clock()
num_instruments = 6
num_beats = 8
boxes = []
# this fills a list full of -1, to show whether a box was clicked:
clicked =  [[-1 for _ in range(num_beats)] for _ in range(num_instruments)]
active_list = [1 for _ in range(num_instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0 # 1, 2, 3, 4... doesn't really start from 0 irl but the loop has to start at column 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
beat_name = ''
typing = False

file = open('saved_beats.txt', 'r') # will be csv style
for line in file:
    saved_beats.append(line)

# load in sounds
clap = mixer.Sound('sounds\clap.WAV')
crash = mixer.Sound('sounds\crash.WAV')
hi_hat = mixer.Sound('sounds\hi hat.WAV')
snare = mixer.Sound('sounds\snare.WAV')
floor_tom = mixer.Sound('sounds\\floor tom.WAV')
bass = mixer.Sound('sounds\\bass.WAV')
pygame.mixer.set_num_channels(num_instruments * 3) 
# default is 8 channels, but some WAV files take more loops to finish (worse at higher BPM)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0: clap.play()
            if i == 1: crash.play()
            if i == 2: hi_hat.play()
            if i == 3: snare.play()
            if i == 4: floor_tom.play()
            if i == 5: bass.play()


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5) 
    # 0,0 is top left corner, 200 is width, 5 is how wide edges are
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    # HEIGHT-200 prevents crisscross
    boxes = []
    colors = [gray, white, gray] # idk why this and no black

    # TODO: make this programmatically set, vary heights by num_instruments
    clap_text       = label_font.render('Clap', True, colors[actives[0]]) # True for anti-alias
    screen.blit(clap_text,      (30, 30)) # blit displays on screen, (X,Y) location
    crash      = label_font.render('Crash', True, colors[actives[1]])
    screen.blit(crash,     (30, 130))
    hi_hat_text     = label_font.render('Hi Hat', True, colors[actives[2]])
    screen.blit(hi_hat_text,    (30, 230))
    snare_text      = label_font.render('Snare', True, colors[actives[3]])
    screen.blit(snare_text,     (30, 330))
    floor_tom_text  = label_font.render('Floor Tom', True, colors[actives[4]])
    screen.blit(floor_tom_text, (30, 430))
    bass_text       = label_font.render('Bass Drum', True, colors[actives[5]])
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
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
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

        
        active = pygame.draw.rect(screen, blue, \
            [beat * ((WIDTH-200)//num_beats) + 200, 0, \
            ((WIDTH-200)//num_beats), num_instruments*100], 5, 5)

    return boxes

# TODO: maybe pause playing while menu is open
def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: What do you wanna call this banger?', True, white)
    save_button_text = label_font.render('Save Beat', True, white)
    exit_text = label_font.render('Close', True, white)
    save_button = pygame.draw.rect(screen, gray, [WIDTH//2 - 200, HEIGHT*0.75, 400, 100], 0, 5)
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH-200, HEIGHT-100, 180, 90], 0, 5)
    screen.blit(menu_text, (400, 40))
    screen.blit(save_button_text, (WIDTH//2 - 70, HEIGHT*0.75 + 30))
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))
    if typing: 
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, save_button, entry_rect


def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH-200, HEIGHT-100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-70))
    return exit_btn


# GAME LOOP
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)

    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT-150, 200, 100], 0, 5) # 5 for rounded
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT-130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT-90))

    # bpm stuff
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT-150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT-130))
    bpm_num_text = label_font.render(f'{bpm}', True, white) # can also do f'BPM:{bpm}'
    screen.blit(bpm_num_text, (370, HEIGHT-100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT-150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT-100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (520, HEIGHT-140))
    screen.blit(sub_text, (520, HEIGHT-90))

    # beats stuff
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT-150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (618, HEIGHT-130))
    beats_text2 = label_font.render(f'{num_beats}', True, white)
    screen.blit(beats_text2, (680, HEIGHT-100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT-150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT-100, 48, 48], 0, 5)
    add_text = medium_font.render('+1', True, white)
    sub_text = medium_font.render('-1', True, white)
    screen.blit(add_text, (820, HEIGHT-140))
    screen.blit(sub_text, (820, HEIGHT-90))

    # instrument rects
    instrument_rects = []
    for i in range(num_instruments):
        rect = pygame.rect.Rect((0, i*100), (200, 100))
        instrument_rects.append(rect)

    # save and load stuff
    save_menu_button = pygame.draw.rect(screen, gray, [900, HEIGHT-150, 200, 48], 0, 5)
    load_menu_button = pygame.draw.rect(screen, gray, [900, HEIGHT-100, 200, 48], 0, 5)
    save_menu_text = label_font.render('Save Beat', True, white)
    load_menu_text = label_font.render('Load Beat', True, white)
    screen.blit(save_menu_text, (920, HEIGHT-140))
    screen.blit(load_menu_text, (920, HEIGHT-90))

    # clear board
    clear_button = pygame.draw.rect(screen, gray, [1150, HEIGHT-150, 200, 100], 0, 5)
    clear_button_text = label_font.render('Clear Board', True, white)
    screen.blit(clear_button_text, (1160, HEIGHT-120))

    if save_menu:
        exit_button, save_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    # check mouse input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                # scalable, check whether mouse click collides with box
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                num_beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                num_beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(num_beats)] for _ in range(num_instruments)]
            elif save_menu_button.collidepoint(event.pos):
                save_menu = True
            elif load_menu_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            if entry_rectangle. collidepoint(event.pos):
                #TODO: typing=false when clicking outside of entry_rectangle
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            elif save_button.collidepoint(event.pos):
                file = open('saved_beats.txt', 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {num_beats}, bpm: {bpm}, selected: {clicked}')
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

    beat_length = 3600 // bpm # clicks per minute - fps*60

    if playing:
        if active_length < beat_length:
            active_length += 1
        else: # beat as long as its supposed to be
            active_length = 0
            if active_beat < num_beats-1:
                active_beat += 1
                beat_changed = True
            else: # not at the end of loop or went too far
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit() # just in case
