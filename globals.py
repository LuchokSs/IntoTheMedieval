import pygame


FPS = 30
CELL_SIZE = (80, 50)
FIELD_SIZE = (1000, 700)

MODES = {'START_MENU': 0,   # Словарь хранит соответствие названия состояния игры и численного кода состояния.
         'FIELD': 1,        # НЕ МЕНЯТЬ БЕЗ ПРЕДУПРЕЖДЕНИЯ
         'END_MENU': 2,
         'EXIT': 3,
         'CHEST': 4}

CELL_TYPES = ['FIELD', 'FOREST', 'HOUSE', 'HILL', 'WATER']

MOVEMENT_TYPES = {'grounded': 0,
                  'flying': 1,
                  'floating': 2}


"""EVENTS"""

EXIT_MENU_EVENT = pygame.event.Event(pygame.USEREVENT + 1)
MOVING_UNIT_EVENT = pygame.event.Event(pygame.USEREVENT + 2)
SPELLCAST_UNIT_EVENT = pygame.event.Event(pygame.USEREVENT + 3)
HOUSE_DAMAGED_EVENT = pygame.event.Event(pygame.USEREVENT + 4)


UNITS = {'warrior': ".\\data\\units\\warrior\\unit.json",
         'shield': '.\\data\\units\\shield\\unit.json',
         'archer': '.\\data\\units\\archer\\unit.json'}

squad = ['warrior', 'archer', 'warrior']