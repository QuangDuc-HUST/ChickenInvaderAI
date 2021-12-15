import pygame
import os
import json
import numpy as np
from Model import GameModel


def online_play(game: 'GameModel'):
    White, Grey, Red = (255, 255, 255), (100, 100, 100), (255, 0, 0)
    unit = 50
    pygame.display.set_caption("CHICKEN INVADERS")
    pygame.init()
    pygame.font.init()
    all_step = dict()
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
        if finish and step == len(all_step.keys())-1:
            if len(space.eggs) > 0:
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
        data = json.loads(all_step[step])  # type here is a list of int
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

    def to_json(figure: 'np.ndarray', all_step: dict, step: int):
        all_step[step] = json.dumps(figure.tolist())

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
            
            if len(acting_possible_invaders) :
                new_egg_number = np.random.randint(1, min([4,1+ len(acting_possible_invaders)]))
                laying_invader = sorted(np.random.choice(
                    range(len(acting_possible_invaders)), new_egg_number, replace=False))
                for i in laying_invader:
                    acting_possible_invaders[i].lay()
            else:
                return
                for i in acting_possible_invaders:
                    i.lay()

    mode = 'play'
    i = 0
    step = 0
    run = True
    finish = False
    to_json(space.figure, all_step, i)
    FPS = 60
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        if mode == 'play':
            draw_screen(i)
        elif mode == 'play-back':
            draw_screen(step)
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
                    i += 1
                    print(f'Step {i}: Do ', end='')
                    environment_changes(space, i)
                    ship.move(n)
                    to_json(space.figure, all_step, i)
                    if space.check_collision():
                        finish = True
                    if space.check_winning():
                        print('Winning')
                        finish = True
                    space.show()
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if mode == 'play':
                        step = i
                        mode = 'play-back'
                    if event.key == pygame.K_LEFT:
                        if step >= 0:
                            step -= 1
                        if step == -1:
                            step = len(all_step.keys())-1
                    if event.key == pygame.K_RIGHT:
                        if step <= len(all_step.keys())-1:
                            step += 1
                        if step == len(all_step.keys()):
                            step = 0
    pygame.quit()

