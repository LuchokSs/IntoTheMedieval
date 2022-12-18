import random

from cellClass import Cell
from globals import CELL_SIZE, EXIT_MENU_EVENT
from secondary import load_image
from interfaceClass import Interface

import pygame


LAST_CLICKED = None


def field_mode(main_screen, *args, **kwargs):
    """Функция с игровым цЫклом поля."""

    running = True

    board = Field(main_screen, running)

    while running:
        pygame.display.flip()

        main_screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 3
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.clicked(event.pos)
            if event == EXIT_MENU_EVENT:
                return 0

        board.draw_field()


class Field:
    """Класс поля."""

    patterns_name = ["HILLS_PATTERNS"]  # WIP , "LAKE_PATTERNS", "FOREST_PATTERNS", "CITY_PATTERNS"
    patterns_num = 4

    def __init__(self, surface, running):
        self.surface = surface
        self.running = running

        self.interface = Interface(self.surface)
        self.interface.update()

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

    def draw_field(self):

        """Изображает поле на указанном хосте."""

        for row in self.field:
            for cell in row:
                cell.draw_cell(self.surface)

        self.interface.update()

    def clicked(self, pos):

        """Обработка событий нажатия кнопки. Получает на вход координаты в виде tuple."""

        for row in self.field:
            for cell in row:
                if cell.is_clicked(pos):
                    global LAST_CLICKED
                    if LAST_CLICKED is not None:
                        LAST_CLICKED.clicked = False
                    cell.clicked = True
                    LAST_CLICKED = cell

        self.interface.interface_clicked(pos)

    def set_unit(self, pos, unit_name):

        """Загрузка юнита из json файла, расположенного по пути, указанному в глобальном словаре,
           в соответствии с именем юнита на указанную точку."""
