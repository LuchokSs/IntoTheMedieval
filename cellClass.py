import random

import pygame

from PIL import Image, ImageDraw

from globals import CELL_SIZE, CELL_TYPES
from secondary import load_image, pil_image_to_surface


class Cell:

    """Класс клетки
        Хранит в себе всю информацию о ней."""

    content = None
    clicked = False
    marked = False
    tick = 0
    animation_direction = True

    def __init__(self, points, pos, cell_type_id=None, indexes=(0, 0)):
        self.points = points
        self.crds = indexes

        self.cell_type_id = cell_type_id

        if cell_type_id is None:
            self.sprite = pygame.surface.Surface(CELL_SIZE)
            pygame.draw.polygon(self.sprite, 'white', points, 5)
        else:
            self.sprite = \
                load_image(f'''data\\cell_images\\{CELL_TYPES[cell_type_id]
                }\\{CELL_TYPES[cell_type_id]}_{random.randint(1, 3)}.png''', colorkey='black')
        self.pos = pos

    def draw_cell(self, surface):

        """Изображает клетку на поле. Черный цвет - цвет фона (Предварительно)."""
        image = self.sprite.copy()

        if self.marked:
            pygame.draw.polygon(image, (150, 150, 30),
                                ((0, CELL_SIZE[1] // 2), (CELL_SIZE[0] // 2, 0),
                                 (CELL_SIZE[0], CELL_SIZE[1] // 2), (CELL_SIZE[0] // 2, CELL_SIZE[1])), 5)

        if self.clicked:
            image = pil_image_to_surface(image, direction=False)
            data = image.load()
            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    data[x, y] = tuple(map(
                        lambda el: (el + int(20 * self.tick)) if (el + 20 * self.tick) < 255 else 255, data[x, y]))
            color = data[0, 0]
            image = pil_image_to_surface(image)
            image.set_colorkey(color)
            self.tick = (self.tick + 0.08) if self.animation_direction else (self.tick - 0.05)
            if self.tick > 5 and self.animation_direction or self.tick < 0.5 and not self.animation_direction:
                self.animation_direction = not self.animation_direction
        else:
            image.set_colorkey('black')

        if self.content is not None:
            unit_image = self.content.get_image()
            image.blit(unit_image, unit_image.get_rect())

        surface.blit(image, (*self.pos, *CELL_SIZE))

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
