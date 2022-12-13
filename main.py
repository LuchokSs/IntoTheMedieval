import pygame

from fieldClass import field_mode
from globals import FPS, FIELD_SIZE, MODES


if __name__ == '__main__':
    pygame.init()
    main_screen = pygame.display.set_mode(FIELD_SIZE)

    running = True

    mode = MODES['FIELD']

    while running:
        if mode == MODES['START_MENU']:
            pass
        if mode == MODES['FIELD']:
            running = field_mode(main_screen)
