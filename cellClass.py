import random

import pygame

from globals import CELL_SIZE, CELL_TYPES
from secondary import load_image


class Cell:
    """Класс клетки
        Хранит в себе всю информацию о ней."""

    content = None

    def __init__(self, points, pos, cell_type_id=None):
        self.points = points

        if cell_type_id is None:
            self.sprite = pygame.surface.Surface(CELL_SIZE)
            pygame.draw.polygon(self.sprite, 'white', points, 5)
        else:
            self.sprite = \
                load_image(f'''cell_images\\{CELL_TYPES[cell_type_id]
                }\\{CELL_TYPES[cell_type_id]}_{random.randint(1, 3)}.png''', colorkey='black')
        self.pos = pos

    def draw_cell(self, surface):

        """Изображает клетку на поле. Черный цвет - цвет фона (Предварительно)."""

        self.sprite.set_colorkey('black')
        surface.blit(self.sprite, (*self.pos, *CELL_SIZE))

    def is_clicked(self, pos):

        """Возвращает информацию о том, нажата ли клетка."""

        x, y = pos
        x = x - self.pos[0] - CELL_SIZE[0] // 2
        y = y - self.pos[1] - CELL_SIZE[1] // 2
        k = (CELL_SIZE[1] // 2) / (CELL_SIZE[0] // 2)
        if (k * x + (CELL_SIZE[1] // 2) >= y >= k * x - (CELL_SIZE[1] // 2)
                and -1 * k * x + (CELL_SIZE[1] // 2) >= y >= -1 * k * x - (CELL_SIZE[1] // 2)):
            return True
        else:
            return False
