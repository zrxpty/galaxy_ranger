import pygame
from settings import *

pygame.init()


def help():
    pygame.display.set_caption("Помощь")
    screen1 = pygame.display.set_mode((WIDTH, HEIGHT))
    screen1.fill((0, 0, 0))
    file_text = open('Помощь.txt', 'r')
    lines = file_text.readlines()
    dlina = len(lines)
    file_text.close()
    y = 40
    x = 15
    f = pygame.font.SysFont(None, 30)

    running = True
    while running:
        screen1.blit(bg_help, (0, 0))
        # отрисовка текста
        for i in range(dlina):
            ln = lines[i]
            dl = len(ln) - 1
            ln = ln[0:dl]
            text = f.render(ln, 1, [255, 255, 255])
            screen1.blit(text, (x, y))
            y += 25
            if i == dlina - 1:
                y = 30

        pygame.display.update()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
               running = False


