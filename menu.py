import pygame
from pygame.color import THECOLORS
from settings import *
import sys


def main_menu():
    pygame.init()
    pygame.display.set_caption("Галактический рейнджер")
    screen = pygame.display.set_mode([1000, 1000])
    background = pygame.Surface(screen.get_size())
    top = [300, 500, 700]
    left = 100
    width = 200
    height = 80
    menu_text = ["Играть", "Помощь", "Выход"]

    font = pygame.font.Font(None, 60)
    font2 = pygame.font.SysFont(None, 50)

    running = True
    while running:
        background.blit(bg_menu, (0, 0))

        (x, y) = pygame.mouse.get_pos()
        for i in range(len(top)):

            if x > left and x < left + width and y > top[i] and y < top[i] + height:
                 break
        #отрисовка надписей
        for i in range(len(menu_text)):
            text3 = font.render(menu_text[i], 1, THECOLORS["white"])
            background.blit(text3, [left+53, top[i]+20])
        text3 = font2.render("Галактический рейнджер", 1, THECOLORS["white"])
        background.blit(text3, [35, 75])
        screen.blit(background, (0, 0))

        pygame.display.flip()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    # выбор надписи
                    if x>left and x<left+width and y>top[i] and y<top[i]+height:
                        break
                if i == 2:
                    pygame.quit()
                    sys.exit()
                if i == 0:
                    import choice_game
                    choice_game.choice_mode()
                    sys.exit()
                if i == 1:
                    import help
                    help.help()
    pygame.quit()

main_menu()
