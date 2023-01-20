import pygame

from fieldClass import field_mode
from globals import FPS, FIELD_SIZE, MODES, available_units
from menuClass import start_screen
from endgameClass import end_screen
from chestClass import chest_screen


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Into The Medieval")
    icon = pygame.image.load(".\\data\\interface_images\\icon.png")
    pygame.display.set_icon(icon)

    pygame.mixer.music.load(".\\data\\music\\aknightarrivesincancoonvillage.mp3")
    pygame.mixer.music.play(-1)

    main_screen = pygame.display.set_mode(FIELD_SIZE)

    running = True
    isOpened = False

    mode = MODES['START_MENU']
    # В зависимости от Mod'а игры запускается определенная функция.
    while running:
        if mode == MODES['START_MENU']:
            mode = start_screen(main_screen)
        if mode == MODES['FIELD']:
            mode = field_mode(main_screen)
            isOpened = False
        if mode == MODES['END_MENU']:
            mode = end_screen(main_screen, isOpened)
        if mode == MODES['CHEST']:
            mode, isOpened = chest_screen(main_screen)
        if mode == MODES['EXIT']:
            running = False
