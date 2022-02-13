import pygame
import time
import random
import sys
from settings import *


def bes_game():
    pygame.font.init()

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Галактический рейнджер")

    # дроны
    RED_SPACE_SHIP = pygame.image.load('dron.png')
    GREEN_SPACE_SHIP = pygame.image.load('dron1.png')
    VIOLET_SPACE_SHIP = pygame.image.load("dron2.png")

    # Корабль игрока
    YELLOW_SPACE_SHIP = pygame.image.load("hero.png")

    # Лазеры
    GREEN_LASER = pygame.image.load('pixel_laser_green.png')
    BLUE_LASER = pygame.image.load("pixel_laser_blue.png")
    RED_LASER = pygame.image.load("pixel_laser_red.png")
    VIOLET_LASER = pygame.image.load("pixel_laser_yellow.png")

    class Laser:
        """
        Класс наследуемый в другие классы
        """
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.mask = pygame.mask.from_surface(self.img)

        # отрисовка лазера
        def draw(self, window):
            window.blit(self.img, (self.x, self.y))

        #движение лазера
        def move(self, vel):
            self.y += vel

        # сопрекосновение с экраном
        def off_screen(self, height):
            return not (self.y <= height and self.y >= 0)
        # сопрекосновение с обьектами такие как дроны или враги
        def collision(self, obj):
            return collide(self, obj)

    class Ship:
        """Класс наследуемый в другие как класс игкорка и дрона"""
        COOLDOWN = 20

        def __init__(self, x, y, health=100):
            self.x = x
            self.y = y
            self.health = health
            self.ship_img = None
            self.laser_img = None
            self.lasers = []
            self.cool_down_counter = 0

        # отрисовка героя
        def draw(self, window):
            window.blit(self.ship_img, (self.x, self.y))
            for laser in self.lasers:
                laser.draw(window)

        # выстрел
        def move_lasers(self, vel, obj):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                elif laser.collision(obj):
                    obj.health -= 10
                    self.lasers.remove(laser)

        # перезарядка, то есть он не может выпустить несколько пуль подряд
        def cooldown(self):
            if self.cool_down_counter >= self.COOLDOWN:
                self.cool_down_counter = 0
            elif self.cool_down_counter > 0:
                self.cool_down_counter += 1

        # выстрел
        def shoot(self):
            if self.cool_down_counter == 0:
                laser = Laser(self.x, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1

        # принимает ширину корабля
        def get_width(self):
            return self.ship_img.get_width()

        # принимает высоту корабля
        def get_height(self):
            return self.ship_img.get_height()

    class Player(Ship):
        """Принимает некоторые функции из класса Ship"""
        def __init__(self, x, y, health=100):
            super().__init__(x, y, health)
            self.ship_img = YELLOW_SPACE_SHIP
            self.laser_img = RED_LASER
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health

        # движение лазера и его сопрекосновение с обьектом
        def move_lasers(self, vel, objs):
            self.cooldown()
            for laser in self.lasers:
                laser.move(vel)
                if laser.off_screen(HEIGHT):
                    self.lasers.remove(laser)
                else:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)

        # управление кораблем игрока
        def move_hero(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0:  # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
                player.x += player_vel
            if keys[pygame.K_w] and player.y - player_vel > 0:  # up
                player.y -= player_vel
            if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
                player.y += player_vel
            if keys[pygame.K_SPACE]:
                player.shoot()
            if keys[pygame.K_ESCAPE]:
                import menu
                menu.main_menu()
                run = False
                sys.exit()

        # анимация полета корабля
        def animation(self):
            player.y -= 3

            if player.y <= -150:
                sys.exit()

        # отрисовка жизней корабля
        def draw(self, window):
            super().draw(window)
            self.healthbar(window)

        # создание панельки жизней игрока
        def healthbar(self, window):
            pygame.draw.rect(window, (255, 0, 0),
                             (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                                   self.ship_img.get_width() * (self.health / self.max_health), 10))

    class Enemy(Ship):
        COLOR_MAP = {
            "red": (RED_SPACE_SHIP, GREEN_LASER),
            "green": (GREEN_SPACE_SHIP, BLUE_LASER),
            "violet": (VIOLET_SPACE_SHIP, VIOLET_LASER)
        }
        # создание модельки дронов
        def __init__(self, x, y, color, health=100):
            super().__init__(x, y, health)
            self.ship_img, self.laser_img = self.COLOR_MAP[color]
            self.mask = pygame.mask.from_surface(self.ship_img)
        # движение дронов
        def move(self, vel):
            self.y += vel
        # выстре дронов
        def shoot(self):
            if self.cool_down_counter == 0:
                laser = Laser(self.x - 20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1
    # сопрекосновение с игкроком
    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 7
    laser_vel = 10

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    while run:
        clock.tick(FPS)
        WIN.blit(bg_advent, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        #  отрисовка жизней и количество пройденных волн
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # отрисовка дронов
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

        # проигрыш
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        # проигрыш
        if lost:
            run = False
            import dead
            dead.dead_game()

        # генерация новой волны и увелечение дронов
        if len(enemies) == 0:
            level += 1
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "green", "violet"]))
                enemies.append(enemy)
        # выход из игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
                run = False


        # сопрекосноввение с обьектами переберая дронов
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            # выстрел дронов
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()
            # сопрекосновение игрока и дрона
            if collide(enemy, player):
                player.health -= 5
                enemies.remove(enemy)
            # сопрекосновение дрона с нижней части экрана
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        # движение игрока и движение лазера и сопрекосновение с дронами
        player.move_lasers(-laser_vel, enemies)
        player.move_hero()



    pygame.quit()


