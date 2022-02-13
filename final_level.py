import pygame
import sys
from settings import *


def final():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Галактический рейнджер')

    # define game variables
    tile_size = 50
    game_over = 0

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            self.interval_jump = 1
            for num in range(1, 11):
                img_right = pygame.image.load(f'hero/hero_{num}.png')
                img_right = pygame.transform.scale(img_right, (40, 80))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True

        def update(self, game_over):
            dx = 0
            dy = 0
            walk_cooldown = 5

            if game_over == 0:
                # get keypresses
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                    self.vel_y = -17
                    self.jumped = True
                if keys[pygame.K_SPACE] == False:
                    self.jumped = False
                if keys[pygame.K_a]:
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                if keys[pygame.K_d]:
                    dx += 5
                    self.counter += 1
                    self.direction = 1
                if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]
                if keys[pygame.K_ESCAPE]:
                    import menu
                    game_over = -1

                # handle animation
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                # add gravity
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y
                self.in_air = True
                # check for collision
                for tile in world.tile_list:
                    # check for collision in x direction
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    # check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        # check if below the ground i.e. jumping
                        self.in_air = False
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        # check if above the ground i.e. falling
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0

                if pygame.sprite.spritecollide(self, ship_group, False):
                    game_over = 1

                # update player coordinates
                self.rect.x += dx
                self.rect.y += dy

            elif game_over == -1:
                self.image = self.dead_image
                if self.rect.y > -100:
                    self.rect.y -= 5

            # draw player onto screen
            screen.blit(self.image, self.rect)

            return game_over

    class World():
        def __init__(self, data):
            self.tile_list = []

            # load images
            dirt_img = pygame.image.load('dirt1.png')
            grass_img = pygame.image.load('grass1.png')

            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2:
                        img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 5:
                        ship = Ship(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        ship_group.add(ship)

                    col_count += 1
                row_count += 1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])

    class Ship(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('hero.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - 70
            self.move_direction = 1
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter = 5
            self.rect.y -= self.move_counter
            if self.rect.y == -150:
                import ship_adventure
                ship_adventure.adventure()

    player = Player(100, HEIGHT - 130)
    ship_group = pygame.sprite.Group()

    world = World(level)

    run = True
    while run:

        start_win(screen, bg_day)

        world.draw()

        if game_over == 1:
            run = False

        ship_group.draw(screen)
        game_over = player.update(game_over)

        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if key[pygame.K_ESCAPE]:
                import menu
                menu.main_menu()
                run = False
                sys.exit()

        pygame.display.update()

    run = True
    while run:
        start_win(screen, bg_day)

        world.draw()

        ship_group.draw(screen)
        ship_group.update()

        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if key[pygame.K_ESCAPE]:
                import menu
                menu.main_menu()
                run = False
                sys.exit()

        pygame.display.update()


final()
