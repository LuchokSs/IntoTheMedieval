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

    def __init__(self, points, pos, cell_type_id=None):
        self.points = points

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
        image = self.sprite

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
            surface.blit(image, (*self.pos, *CELL_SIZE))
            self.tick = (self.tick + 0.08) if self.animation_direction else (self.tick - 0.05)
            if self.tick > 5 and self.animation_direction or self.tick < 0.5 and not self.animation_direction:
                self.animation_direction = not self.animation_direction
            return
        image.set_colorkey('black')
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

    def move_unit(self, cell_of_unit, cell_of_movement):

        """Перемещает песронажа класса Unit в указанную клетку, возвращает tuple новой позиции."""

        cell_of_unit.content, cell_of_movement.content = cell_of_movement.content, cell_of_unit.content

    def show_movement_range(self, pos, range_of_movement, movement_type=0, visited=[]):

        """Подсвечивает все возможные для перемещения клетки."""

        print(pos)
        x, y = pos
        if range_of_movement == 0:
            self.field[[x][y]].marked = True
        else:
            if self.field[[x + 1][y]].cell_type_id == movement_type == 0 and [x + 1][y] not in visited:
                self.field[[x + 1][y]].marked = True
                visited.append([x + 1][y])
                show_movement_range((x + 1, y), range_of_movement - 1, movement_type, visited)
            if self.field[[x - 1][y]].cell_type_id == movement_type == 0 and [x - 1][y] not in visited:
                self.field[[x - 1][y]].marked = True
                visited.append([x - 1][y])
                show_movement_range((x - 1, y), range_of_movement - 1, movement_type, visited)
            if self.field[[x][y + 1]].cell_type_id == movement_type == 0 and [x][y + 1] not in visited:
                self.field[[x][y + 1]].marked = True
                visited.append([x][y + 1])
                show_movement_range((x, y + 1), range_of_movement - 1, movement_type, visited)
            if self.field[[x][y - 1]].cell_type_id == movement_type == 0 and [x][y - 1] not in visited:
                self.field[[x][y - 1]].marked = True
                visited.append([x][y - 1])
                show_movement_range((x, y - 1), range_of_movement - 1, movement_type, visited)
            if movement_type == 1:
                if [x + 1][y] not in visited:
                    self.field[[x + 1][y]].marked = True
                    visited.append([x + 1][y])
                    show_movement_range((x + 1, y), range_of_movement - 1, movement_type, visited)
                if [x - 1][y] not in visited:
                    self.field[[x - 1][y]].marked = True
                    visited.append([x - 1][y])
                    show_movement_range((x - 1, y), range_of_movement - 1, movement_type, visited)
                if [x][y + 1] not in visited:
                    self.field[[x][y + 1]].marked = True
                    visited.append([x][y + 1])
                    show_movement_range((x, y + 1), range_of_movement - 1, movement_type, visited)
                if [x][y - 1] not in visited:
                    self.field[[x][y + 1]].marked = True
                    visited.append([x][y + 1])
                    show_movement_range((x, y + 1), range_of_movement - 1, movement_type, visited)