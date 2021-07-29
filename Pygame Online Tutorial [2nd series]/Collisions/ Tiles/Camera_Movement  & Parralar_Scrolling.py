import pygame, sys  # import pygame and sys

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame

pygame.display.set_caption('Pygame Window')  # set the window name

WINDOW_SIZE = (600, 400)  # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen

display = pygame.Surface((300, 200))

player_image = pygame.image.load('player.png').convert()
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
true_scroll = [0, 0]

dirt_image = pygame.image.load('dirt.png')


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


gam_map = load_map('map')

background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [130, 90, 100, 400]],
                      [0.5, [300, 80, 120, 400]]]


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while True:  # game loop
    display.fill((146, 244, 255))
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect((0, 120, 300, 80)))
    for background_object in background_objects:
        obj_rect = pygame.Rect((background_object[1][0] - scroll[0] * background_object[0],
                                background_object[1][1] - scroll[0] * background_object[0], background_object[1][2],
                                background_object[1][3]))
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)

        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    y = 0
    for row in gam_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * 16 - scroll[0], y * 16 - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps
