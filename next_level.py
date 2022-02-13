import pygame
import sys
from settings import *


import pygame
from settings import *
import sys
pygame.init()


def start_level_1():
    clock = pygame.time.Clock()
    fps = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Галактический рейнджер')


    tile_size = 50
    game_over = 0
    font = pygame.font.SysFont(None, 30)
    # draw text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    class Player(pygame.sprite.Sprite):
        """Class player"""
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
            """Управление персонажем сопрекосновение с полом, стенами и врагами"""
            dx = 0
            dy = 0
            walk_cooldown = 7

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

                # анимация игрока
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

                # гравитация
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                self.in_air = True
                # проверка на касания
                for tile in world.tile_list:
                    # касание с полом
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    # косание с землей
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        # прыжок проверка на пустоту
                        self.in_air = False
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0

                        # падение
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0

                # прикосновение с врагами
                if pygame.sprite.spritecollide(self, enemy_group, False):
                    game_over = -1

                # прикосновение с лавой
                if pygame.sprite.spritecollide(self, lava_group, False) or pygame.sprite.spritecollide(self, lavafull_group, False):
                    game_over = -1
                # прикосновение с летающим врагом
                if pygame.sprite.spritecollide(self, fly_enemy, False):
                    game_over = -1
                # прикосновение с шипом
                if pygame.sprite.spritecollide(self, spike_group, False):
                    game_over = -1

                # передвижение
                self.rect.x += dx
                self.rect.y += dy

            # отрисовка игрока
            screen.blit(self.image, self.rect)

            return game_over

    class World():
        """Класс мир здесь идет чтение матрицы и ее отрисовка по значениям"""
        def __init__(self, data):
            self.tile_list = []

            # load images
            dirt_img = pygame.image.load('dirt.png')
            grass_img = pygame.image.load('grass.png')
            coin = pygame.image.load('glass.png')
            lava = pygame.image.load("lava.png")
            coin = pygame.transform.scale(coin, (40, 40))
            score_block = 0

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
                    if tile == 3:
                        enemy = Enemy(col_count * tile_size, row_count * tile_size + 5)
                        enemy_group.add(enemy)
                    if tile == 4:
                        lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lava_group.add(lava)
                    if tile == 5:
                        exit = Exit(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        exit_group.add(exit)
                    if tile == "y":
                        spike = Spike(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        spike_group.add(spike)
                    if tile == 8:
                        money = Money(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        money_group.add(money)
                        score_block += 1
                        print(score_block)
                    if tile == 'x':
                        img = pygame.transform.scale(coin, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 'e':
                        fly = FlyEnemy(col_count * tile_size, row_count * tile_size + 5)
                        enemy_group.add(fly)
                    if tile == 6:
                        pokerMad = PokerMad(col_count * tile_size, row_count * tile_size + 5)
                        enemy_group.add(pokerMad)
                    if tile == 44:
                        lava = LavaFull(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                        lavafull_group.add(lava)
                    if tile == 444:
                        pokerMadUP = PokerMadUP(col_count * tile_size, row_count * tile_size + 5)
                        enemy_group.add(pokerMadUP)

                    col_count += 1
                row_count += 1
        # отрисовка мира
        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])

    class Enemy(pygame.sprite.Sprite):
        """Класс врага"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('blob.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.move_direction = 2
            self.move_counter = 0

        # передвижение врага
        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1

            if abs(self.move_counter) > 25:
                self.move_direction *= -1
                self.move_counter *= -1

    class Lava(pygame.sprite.Sprite):
        """Создание блока лавы"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('lava.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class LavaFull(pygame.sprite.Sprite):
        """Создание блока лавы"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('lava.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y-25

    class Exit(pygame.sprite.Sprite):
        """Создание блока выхода"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('exit.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size+20))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y-45

    class Money(pygame.sprite.Sprite):
        """Создание блока монет"""
        def __init__(self, x, y):
            super().__init__()

            self.sprites = []
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_1.png'), (40, 40)))
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_2.png'), (40, 40)))
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_3.png'), (40, 40)))
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_4.png'), (40, 40)))
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_5.png'), (40, 40)))
            self.sprites.append(pygame.transform.scale(pygame.image.load('money/money_6.png'), (40, 40)))
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.topleft = [x+5, y-20]
        # анимация монеты
        def update(self):
            self.current_sprite += 0.4
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

    class FlyEnemy(pygame.sprite.Sprite):
        """Создание класса летающего врага"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('fly-enemy/fly1.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - 10
            self.move_direction = 3
            self.move_counter = 0
            self.image = pygame.transform.flip(self.image, True, False)
        # передвижение врага
        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 1

            if abs(self.move_counter) > 125:
                self.move_direction *= -1
                self.move_counter *= -1
                self.image = pygame.transform.flip(self.image, True, False)

    class Spike(pygame.sprite.Sprite):
        """Класс шипов"""
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('spike.png')
            self.image = pygame.transform.scale(img, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.x = x+5
            self.rect.y = y-15

    class PokerMad(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('pokerMad.png')
            self.rect = self.image.get_rect()
            self.rect.x = x-250
            self.rect.y = y
            self.move_direction = 3
            self.move_counter = 0

        def update(self):
            self.rect.x += self.move_direction
            self.move_counter += 2
            if abs(self.move_counter) > 100:
                self.move_direction *= -1
                self.move_counter *= -1
    class PokerMadUP(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('pokerMadUP.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y-150
            self.move_direction = 10
            self.move_counter = 0

        def update(self):
            self.rect.y -= self.move_direction
            self.move_counter += 2
            if abs(self.move_counter) > 50:
                self.move_direction *= -1
                self.move_counter *= -1

    # создание экзапляров классов
    player = Player(100, HEIGHT - 130)
    money_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    lava_group = pygame.sprite.Group()
    lavafull_group = pygame.sprite.Group()
    spike_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    money_group = pygame.sprite.Group()
    world = World(level_2)
    fly_enemy = pygame.sprite.Group()
    score_money = Money(tile_size // 2, tile_size // 2)
    money_group.add(score_money)
    poker_group = pygame.sprite.Group()

    score = 0

    run = True
    while run:

        start_win(screen, bg_level)

        world.draw()

        if game_over == 0:
            # сбор монет и добавление в счет их
            if pygame.sprite.spritecollide(player, money_group, True):
                score += 1
            draw_text(f"X {score}", font, (255, 255, 255), tile_size+20, 15)
            # при наберание определеннного кол-ва монет появляется дверь
            if score >= 15:
                exit_group.draw(screen)
                if pygame.sprite.spritecollide(player, exit_group, False):
                    game_over = 1
            # иницилизация классов
            enemy_group.update()
            fly_enemy.update()
            money_group.update()
            poker_group.update()
        # проверка на смерть
        if game_over == -1:
            run = False
            import dead
            dead.dead_game()
            sys.exit()
        # проверка на касание двери
        if game_over == 1:
            import final_level
            final_level.final()
            sys.exit()
        # иницилизация обьектов

        enemy_group.draw(screen)
        lava_group.draw(screen)
        lavafull_group.draw(screen)
        money_group.draw(screen)
        game_over = player.update(game_over)
        fly_enemy.draw(screen)
        spike_group.draw(screen)
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

    pygame.quit()

