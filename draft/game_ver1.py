from pygame.constants import K_LEFT, K_RIGHT
from main import *
import pygame, os

White, Grey, Red = (255, 255, 255), (100, 100, 100), (255, 0, 0)
all_step = dict()
unit = 60
size = (7, 9)
screen_width, screen_height = unit*size[0],  unit*(size[1]+1)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CHICKEN INVADERS")
pygame.init()
pygame.font.init()
# __LOAD IMAGE__
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (screen_width, screen_height))
img_ship = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")), (unit, unit))
img_chicken = pygame.transform.scale(pygame.image.load(os.path.join("assets", "chicken.png")), (unit, unit))
img_egg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "egg.png")), (unit//2, unit//2))
img_laser = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_laser_red.png")), (unit, unit))
# __DRAW OBJECT FUNCTIONS__
def draw_ship(x, y):
    screen.blit(img_ship, (x*unit, y*unit))
def draw_egg(x, y):
    screen.blit(img_egg, ((x+0.25)*unit, (y+0.25)*unit))
def draw_laser(x, y):
    screen.blit(img_laser, (x*unit, y*unit))
def draw_chicken(x, y):
    screen.blit(img_chicken, (x*unit, y*unit))


def draw_screen(step:int):
    screen.blit(background, (0, 0))
    step_label = pygame.font.SysFont("comicsans", 20).render(
        f"Step: {step} --- Mode: " + mode, 1, (255, 255, 255))
    screen.blit(step_label, (10, screen_height-step_label.get_height()-unit/2))
    if mode == 'play-back':
        label = pygame.font.SysFont("comicsans", 20).render(f"Press SPACE to return 'play' mode." , 1, (255, 255, 255))
    elif mode == 'play':
        label = pygame.font.SysFont("comicsans", 20).render(f"Press A, D, W to control || Press left, right arrow to 'play-back" , 1, (255, 255, 255))
    if finish and step == len(all_step.keys())-1:
        if len(space.eggs) > 0:
            lose_label = pygame.font.SysFont("comicsans", 40).render(f"LOSE" , 1, Red)
            screen.blit(lose_label, (screen_width/2 - lose_label.get_width()/2, screen_height/2 - lose_label.get_height()/2))
        else:
            win_label = pygame.font.SysFont("comicsans", 40).render(f"WIN" , 1, Red)
            screen.blit(win_label, (screen_width/2 - win_label.get_width()/2, screen_height/2 - win_label.get_height()/2))
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
        pygame.draw.line(screen, Grey, (i * unit, 0), (i*unit, screen_height-unit))
    for i in range(1, size[1]+1):
        pygame.draw.line(screen, Grey, (0, i * unit), (screen_width, i * unit))
    pygame.display.update()


space, ship = environment_initialize(9, 7, 14)
print(space.figure)
print('-+-+'*20)
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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if mode == 'play':
        #         step = i
        #         mode = 'play-back'
        #     if event.button == 1:
        #         if step > 0:
        #             step -= 1
        #         if step == 0:
        #             step = len(all_step.keys())-1
        #     if event.button == 3:
        #         if step < len(all_step.keys())-1:
        #             step += 1
        #         if step == len(all_step.keys())-1:
        #             step = 0
        if event.type == pygame.KEYDOWN:
            if mode == 'play-back' and event.key == pygame.K_SPACE:
                    mode = 'play'
                    continue
            elif mode == 'play' and event.key in [pygame.K_a, pygame.K_d, pygame.K_w] and not finish:
                n = None
                if event.key == pygame.K_a:
                    n = 'a'
                elif event.key == pygame.K_d:
                    n = 'd'
                elif event.key == pygame.K_w:
                    n = 'w'
                i += 1
                print(f'Step {i}: Do ', end='')
                environment_changes(space=space, step=i)
                ship.move(n)
                to_json(space.figure, all_step, i)
                if check_collision(space=space):
                    finish = True
                if check_winning(space=space):
                    print('Winning')
                    finish = True
                space.show()
            elif event.key in [K_LEFT, K_RIGHT]:
                if mode == 'play':
                    step = i
                    mode = 'play-back'
                if event.key == K_LEFT:
                    if step >= 0:
                        step -= 1
                    if step == -1:
                        step = len(all_step.keys())-1
                if event.key == K_RIGHT:
                    if step <= len(all_step.keys())-1:
                        step += 1
                    if step == len(all_step.keys()):
                        step = 0
pygame.quit()


