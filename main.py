import pygame

from fieldClass import field_mode
from globals import FPS, FIELD_SIZE, MODES
from menuClass import start_screen


if __name__ == '__main__':
    pygame.init()
    main_screen = pygame.display.set_mode(FIELD_SIZE)

    running = True

    mode = MODES['START_MENU']
    # В зависимости от Mod'а игры запускается определенная функция.

    while running:
        if mode == MODES['START_MENU']:
            mode = start_screen(main_screen)
        if mode == MODES['FIELD']:
            mode = field_mode(main_screen)
        if mode == MODES['EXIT']:
            running = False
