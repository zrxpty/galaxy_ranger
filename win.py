import pygame
from settings import *
import sys


def win_game():
    pygame.init()
    pygame.display.set_caption("Dead")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    bg = pygame.image.load("you_win.png")
    run = True
    while run:
        screen.blit(bg, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                run = False
                import menu
                menu.main_menu()
                sys.exit()





