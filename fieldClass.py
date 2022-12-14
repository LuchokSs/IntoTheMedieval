import random

from cellClass import Cell
from globals import CELL_SIZE
from secondary import load_image

import pygame


def field_mode(main_screen, *args, **kwargs):
    """Функция с игровым цЫклом поля."""

    board = Field()

    running = True

    while running:
        pygame.display.flip()

        main_screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.cell_clicked(event.pos)

        board.draw_field(main_screen)


class Field:
    """Класс поля."""

    patterns_name = ["HILLS_PATTERNS"]  # WIP , "LAKE_PATTERNS", "FOREST_PATTERNS", "CITY_PATTERNS"
    patterns_num = 1

    def __init__(self):
        self.field = \
            open(f'''.\\data\\field_patterns\\{self.patterns_name[random.randint(0, len(self.patterns_name) - 1)]}/{
        random.randint(1, self.patterns_num)}.txt''',
                 'r').readlines()
        self.field = list(map(str.split, self.field))

        xs = CELL_SIZE[0] // 2
        ys = CELL_SIZE[1] // 2

        for row in range(len(self.field)):
            for cell in range(len(self.field[row])):
                points = ((2 * xs, ys), (xs, 2 * ys), (0, ys), (xs, 0))
                pos = 100 + xs * (row + cell), 350 + ys * (row - cell)
                self.field[row][cell] = Cell(points, pos, int(self.field[row][cell]))

    def draw_field(self, surface):

        """Изображает поле на указанном хосте."""

        for row in self.field:
            for cell in row:
                cell.draw_cell(surface)

    def cell_clicked(self, pos):

        """Обработка событий нажатия кнопки. Получает на вход координаты в виде tuple"""

        for row in self.field:
            for cell in row:
                if cell.is_clicked(pos):
                    cell.sprite = load_image('Безымянный.png', colorkey='black')
                    # Р.S. На данный момент в качестве спрайта по умолчанию берется Безымянный.png
