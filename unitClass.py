from secondary import load_image
from globals import MOVEMENT_TYPES, HOUSE_DAMAGED_EVENT
import pygame


class Unit:
    health = 0
    attack_range = 0
    movement_range = 0
    movement_type = MOVEMENT_TYPES['grounded']
    name = ''
    image = ''
    turns_left = {'move': True, 'spell': True}

    def get_image(self):
        return load_image(self.image, colorkey='black')


class Warrior(Unit):
    def show_spellrange(self, field, pos):
        field[pos[0] + 1][pos[1]].marked = True
        field[pos[0]][pos[1] + 1].marked = True
        field[pos[0] - 1][pos[1]].marked = True
        field[pos[0]][pos[1] - 1].marked = True

    def cast_spell(self, field, pos, unit):
        event = HOUSE_DAMAGED_EVENT
        event.pos = []
        if pos.crds[0] == unit.crds[0]:
            x, y = pos.crds
            for dx in range(-1, 2, 1):
                if field[x + dx][y].content is not None:
                    field[x + dx][y].content.health -= 1
                if field[x + dx][y].cell_type_id == 2:
                    event.pos.append([x + dx, y])
        elif pos.crds[1] == unit.crds[1]:
            x, y = pos.crds
            for dy in range(-1, 2, 1):
                if field[x][y + dy].content is not None:
                    field[x][y + dy].content.health -= 1
                if field[x][y + dy].cell_type_id == 2:
                    event.pos.append([x, y + dy])
        pygame.event.post(event)

    def cell_under_attack(self, pos, field, cell):
        if pos.crds[0] == cell.crds[0]:
            x, y = pos.crds
            for dx in range(-1, 2, 1):
                field[x + dx][y].clicked = True
        elif pos.crds[1] == cell.crds[1]:
            x, y = pos.crds
            for dy in range(-1, 2, 1):
                field[x][y + dy].clicked = True
