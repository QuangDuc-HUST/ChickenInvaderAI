import pygame
import os
import copy
import pickle
import numpy as np
from Model import GameModel

def online_play(game: 'GameModel'):
    Grey, Red = (100, 100, 100), (255, 0, 0)
    unit = 60
    pygame.display.set_caption("CHICKEN INVADERS")
    pygame.init()
    pygame.font.init()
    space = game.getSpace()
    ship = space.spaceship
    size = (space.width, space.height)
    screen_width, screen_height = unit*size[0],  unit*(size[1]+1)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # __LOAD IMAGE__
    background = pygame.transform.scale(pygame.image.load(os.path.join(
        "assets", "background-black.png")), (screen_width, screen_height))
    img_ship = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "pixel_ship_yellow.png")), (unit, unit))
    img_chicken = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "chicken.png")), (unit, unit))
    img_egg = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "egg.png")), (unit//2, unit//2))
    img_laser = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "pixel_laser_red.png")), (unit, unit))

    # __DRAW OBJECT FUNCTIONS__
    def draw_ship(x, y):
        screen.blit(img_ship, (x*unit, y*unit))

    def draw_egg(x, y):
        screen.blit(img_egg, ((x+0.25)*unit, (y+0.25)*unit))

    def draw_laser(x, y):
        screen.blit(img_laser, (x*unit, y*unit))

    def draw_chicken(x, y):
        screen.blit(img_chicken, (x*unit, y*unit))

    def draw_screen(step: int):
        '''
        Draw objects on screen by data from saved states
        '''
        screen.blit(background, (0, 0))
        step_label = pygame.font.SysFont("arial", 12).render(
            f"Step: {step} --- Mode: " + mode, 1, (255, 255, 255))
        screen.blit(step_label, (10, screen_height -
                    step_label.get_height()-unit/2))
        if mode == 'play-back':
            label = pygame.font.SysFont("arial", 12).render(
                f"Press SPACE to return 'play' mode.", 1, (255, 255, 255))
        elif mode == 'play':
            label = pygame.font.SysFont("arial", 12).render(
                f"Press A, D, S, W to control|| Press left, right arrow to 'play-back", 1, (255, 255, 255))
        if finish and step == len(game._states)-1:
            if len(space.invaders) > 0:
                lose_label = pygame.font.SysFont(
                    "arial", 40).render(f"LOSE", 1, Red)
                screen.blit(lose_label, (screen_width/2 - lose_label.get_width() /
                            2, screen_height/2 - lose_label.get_height()/2))
            else:
                win_label = pygame.font.SysFont(
                    "arial", 40).render(f"WIN", 1, Red)
                screen.blit(win_label, (screen_width/2 - win_label.get_width() /
                            2, screen_height/2 - win_label.get_height()/2))
        screen.blit(label, (10, screen_height-label.get_height()-10))
        data = game._states[step]  # type here is a list of int
        # print(step, data)
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == 1:
                    draw_chicken(x, y)
                if data[y][x] == 2:
                    draw_ship(x, y)
                if data[y][x] == 4:
                    draw_egg(x, y)
                if data[y][x] == 5:
                    draw_chicken(x, y)
                    draw_egg(x, y)
                if data[y][x] == 6:
                    draw_ship(x, y)
                    draw_egg(x, y)
                if data[y][x] == 7:
                    draw_laser(x, y)
                if data[y][x] == 9:
                    draw_ship(x, y)
                    draw_egg(x, y)
                if data[y][x] == 11:
                    draw_egg(x, y)
                    draw_laser(x, y)
        for i in range(1, size[0]):
            pygame.draw.line(screen, Grey, (i * unit, 0),
                             (i*unit, screen_height-unit))
        for i in range(1, size[1]+1):
            pygame.draw.line(screen, Grey, (0, i * unit),
                             (screen_width, i * unit))
        pygame.display.update()

    def environment_changes(space, step: int):
        """
        Action of all objects in space (excluding Agent)\\
        Actions of bullets, eggs, invaders\\ 
        Return None"""
        for egg in space.eggs.copy():
            egg.drop()
        for bullet in space.bullets.copy():
            bullet.move()

        # invader actions
        acting_possible_invaders = []
        for invader in space.invaders:
            x, y = invader.get_position()
            if space.figure[x + 1, y] != 1:
                acting_possible_invaders.append(invader)

        if step % 3 == 1:

            if len(acting_possible_invaders):
                new_egg_number = np.random.randint(
                    1, min([4, 1 + len(acting_possible_invaders)]))
                laying_invader = sorted(np.random.choice(
                    range(len(acting_possible_invaders)), new_egg_number, replace=False))
                for i in laying_invader:
                    acting_possible_invaders[i].lay()
            else:
                return
                for i in acting_possible_invaders:
                    i.lay()

    mode = 'play'
    current_step = 0
    playback_step = 0
    run = True
    finish = False
    game._states.append(copy.deepcopy(space.figure))
    FPS = 60
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        if mode == 'play':
            draw_screen(current_step)
        elif mode == 'play-back':
            draw_screen(playback_step)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:

                if mode == 'play-back' and event.key == pygame.K_SPACE:
                    mode = 'play'
                    continue
                elif mode == 'play' and event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s] and not finish:
                    n = None
                    if event.key == pygame.K_a:
                        n = 'a'
                    elif event.key == pygame.K_d:
                        n = 'd'
                    elif event.key == pygame.K_w:
                        n = 'w'
                    else:
                        n = 'remain'
                    current_step += 1
                    print(f'Step {current_step}: ' + n)
                    environment_changes(space, current_step)
                    ship.move(n)
                    game._states.append(copy.deepcopy(space.figure))
                    if space.check_collision():
                        finish = True
                    if space.check_winning():
                        print('Winning')
                        finish = True
                    space.show()
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if mode == 'play':
                        playback_step = current_step
                        mode = 'play-back'
                    if event.key == pygame.K_LEFT:
                        if playback_step >= 0:
                            playback_step -= 1
                        if playback_step == -1:
                            playback_step = len(game._states)-1
                    if event.key == pygame.K_RIGHT:
                        if playback_step <= len(game._states)-1:
                            playback_step += 1
                        if playback_step == len(game._states):
                            playback_step = 0
    pygame.quit()


def visualize_play(filename):

    with open(os.path.join('data', f'{filename}.pickle'), 'rb') as f:
        list_data = pickle.load(f)
    
    print('Hello')

    # __COLOR__
    White, Grey = (255, 255, 255), (100, 100, 100)
    # Black, Red, Blue, Yellow = (0, 0, 0), (255, 0, 0), (0, 0, 255), (250, 200, 0)

    # __SET UP__
    unit = 60
    size = (7, 10)
    screen_width = unit*size[0]
    screen_height = unit*size[1]
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("CHICKEN INVADERS")

    # __LOAD IMAGE__
    background = pygame.transform.scale(pygame.image.load(os.path.join(
        "assets", "background-black.png")), (screen_width, screen_height))
    img_ship = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "pixel_ship_yellow.png")), (unit, unit))
    img_chicken = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "chicken.png")), (unit, unit))
    img_egg = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "egg.png")), (unit, unit))
    img_laser = pygame.transform.scale(pygame.image.load(
        os.path.join("assets", "pixel_laser_red.png")), (unit, unit))

    # __DRAW OBJECT FUNCTIONS__


    def draw_ship(x, y):
        screen.blit(img_ship, (x*unit, y*unit))


    def draw_egg(x, y):
        pygame.draw.circle(screen, White, ((x+0.5) * unit, (y+0.5)*unit), unit//6)


    def draw_laser(x, y):
        screen.blit(img_laser, (x*unit, y*unit))


    def draw_chicken(x, y):
        screen.blit(img_chicken, (x*unit, y*unit))


    # __DRAW SCREEN FUNCTION__
    def draw_screen(step: str, list_data):
        screen.blit(background, (0, 0))
        step_label = pygame.font.SysFont("arial", 20).render(
            f"Step: {step}", 1, (255, 255, 255))
        screen.blit(step_label, (0, screen_height-step_label.get_height()))
        if int(step) >= 0:
            data = list_data[int(step)]  # type here is a list of int
            for y in range(len(data)):
                for x in range(len(data[y])):
                    if data[y][x] == 1:
                        draw_chicken(x, y)
                    if data[y][x] == 2:
                        draw_ship(x, y)
                    if data[y][x] == 4:
                        draw_egg(x, y)
                    if data[y][x] == 5:
                        draw_chicken(x, y)
                        draw_egg(x, y)
                    if data[y][x] == 7:
                        draw_laser(x, y)
                    if data[y][x] == 9:
                        draw_ship(x, y)
                        draw_egg(x, y)
                    if data[y][x] == 11:
                        draw_egg(x, y)
                        draw_laser(x, y)
        for i in range(1, size[0]):
            pygame.draw.line(screen, Grey, (i * unit, 0),
                            (i * unit, screen_height-unit))
        for i in range(1, size[1]):
            pygame.draw.line(screen, Grey, (0, i * unit), (screen_width, i * unit))

    ## Get input file
    


    pygame.display.update()
    pygame.init()
    pygame.font.init()
    step = 0
    run = True
    FPS = 30
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        draw_screen(str(step), list_data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Press LEFT_ARROW to see previous step
                if event.key == pygame.K_LEFT:
                    if step > 0:
                        step -= 1
                # Press RIGHT_ARROW to see next step
                if event.key == pygame.K_RIGHT:
                    if step < len(list_data)-1:
                        step += 1
    pygame.quit()


# if __name__ == '__main__':
#     game = GameModel()
#     game.initialize(height=9, width=7, num=14)
#     online_play(game)

#     # visualize_play('Test')
