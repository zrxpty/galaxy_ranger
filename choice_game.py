import pygame
from settings import *
import sys
pygame.init()


def choice_mode():
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Галактический рейнджер")
    choice_text = ['Сюжетная игра', 'Бесконечная игра']
    top = [200, 600, 1000]
    left = 40
    width = 480
    height = 90
    f3 = pygame.font.SysFont(None, 50)

    running = True
    while running:
        screen.blit(bg_choice, (0,0))
        (x, y) = pygame.mouse.get_pos()
        
        text4 = f3.render(choice_text[0], 1, (255, 255, 255))
        text5 = f3.render(choice_text[1], 1, (255, 255, 255))
        screen.blit(text4, (left, top[0]))
        screen.blit(text5, (left, top[1]))
        pygame.display.update()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # выбор режима
                for i in range(len(top)):
                    if x > left and x < left + width and y > top[i] and y < top[i] + height:
                        break
                if i == 0:
                    import start_game
                    start_game.start_level()
                    running = False
                    sys.exit()
                    
                if i == 1:
                    import bes_game
                    bes_game.bes_game()
                    sys.exit()
                    
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
