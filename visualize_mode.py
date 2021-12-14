import pygame
import os
import pickle

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
    step_label = pygame.font.SysFont("comicsans", 20).render(
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
                         (i * unit, screen_height))
    for i in range(1, size[1]):
        pygame.draw.line(screen, Grey, (0, i * unit), (screen_width, i * unit))
    pygame.display.update()

# __DISPLAY FUNCTION__


def display(list_data):
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


# __LOAD DATA__

if __name__ == '__main__':

    file_name = 'Test1'
    with open(f'data\{file_name}.pickle', 'rb') as f:
        list_data = pickle.load(f)

    print(list_data)
    display(list_data)
