from cellClass import Cell
from globals import CELL_SIZE
from secondary import load_image

import pygame


class Field:
    def __init__(self):
        self.field = []

        xs = CELL_SIZE[0] // 2
        ys = CELL_SIZE[1] // 2

        for x in range(10):
            self.field.append([])
            for y in range(10):
                points = ((2 * xs, ys), (xs, 2 * ys), (0, ys), (xs, 0))
                pos = 100 + xs * (x + y), 350 + ys * (x - y)
                self.field[x].append(Cell(points, pos))

    def draw_field(self, surface):
        for row in self.field:
            for cell in row:
                cell.draw_cell(surface)

    def cell_clicked(self, pos):
        for row in self.field:
            for cell in row:
                if cell.is_clicked(pos):
                    cell.sprite = load_image('Безымянный.png', colorkey='black')
