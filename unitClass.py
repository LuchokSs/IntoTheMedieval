import random

from secondary import load_image, good_cell
from globals import MOVEMENT_TYPES, HOUSE_DAMAGED_EVENT
from fieldClass import Field
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


class Enemy:
    health = 3
    attack_range = 0
    movement_range = 2
    movement_type = MOVEMENT_TYPES['grounded']
    turns_left = {'move': True, 'spell': True}

    def get_image(self):
        return load_image(self.image, colorkey='black')


class EnemyWarrior(Enemy):
    image = '.\\data\\units\\warrior\\unit.json'
    target = None

    def move(self, field, curr_cell):
        cells = []
        pos = curr_cell.crds
        for row in field:
            for cell in row:
                if cell.content is not EnemyWarrior and cell.content is not None:
                    cells.append(cell)
        for cell in cells:
            pos1 = cell.crds
            if ((pos[0] - pos1[1]) ** 2 + (pos[1] - pos1[0]) ** 2) ** 0.5 <= self.movement_range:
                Field.move_content(1, pos, pos1)
                self.target = (pos1[0] - pos[0], pos1[1] - pos[1])
                break
        else:
            while True:
                dx, dy = random.randint(-3, 3), random.randint(-3, 1)
                if field[pos[0] + dx][pos[1] + dy].cell_type_id == 0 and dx != dy != 0:
                    Field.move_content(1, pos, field[pos[0] + dx][pos[1] + dy])
                    break

    def attack(self, field, pos):
        target_pos = (pos[0] + self.target[0], pos[1] + self.target[1])
        target_cell = field[target_pos[0]][target_pos[1]]
        if target_cell.cell_type_id == 2:
            event = HOUSE_DAMAGED_EVENT
            event.pos = target_cell.crds
            pygame.event.post(event)
        if target_cell.content is Unit:
            target_cell.content.health -= 2


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


class Archer(Unit):
    def show_spellrange(self, field, pos):
        num = 0
        while pos[0] + num < 10:
            if good_cell(field[pos[0] + num][pos[1]]):
                field[pos[0] + num][pos[1]].marked = True
            else:
                break
            num += 1
        num = 0
        while pos[0] - num > 0:
            if good_cell(field[pos[0] - num][pos[1]]):
                field[pos[0] - num][pos[1]].marked = True
            else:
                break
            num += 1
        num = 0
        while pos[1] + num < 10:
            if good_cell(field[pos[0]][pos[1] + num]):
                field[pos[0]][pos[1] + num].marked = True
            else:
                break
            num += 1
        num = 0
        while pos[1] - num > 0:
            if good_cell(field[pos[0]][pos[1] - num]):
                field[pos[0]][pos[1] - num].marked = True
            else:
                break
            num += 1

    def cast_spell(self, field, pos, unit):
        event = HOUSE_DAMAGED_EVENT
        event.pos = []
        if pos.crds[1] == unit.crds[1]:
            x, y = unit.crds
            num = 1
            while x + num < 10:
                if field[x + num][y].content is not None:
                    field[x + num][y].content.health -= 2
                    if x + num + 1 < 10:
                        if good_cell(field[x + num + 1][y]):
                            Field.move_content(1, field[x + num][y], field[x + num + 1][y])
                        break
                if field[x + num][y].cell_type_id == 2:
                    event.pos.append([x + num, y])
                    break
                num += 1
            num = 1
            while x - num > 0:
                if field[x - num][y].content is not None:
                    field[x - num][y].content.health -= 2
                    if x - num - 1 > -10:
                        if good_cell(field[x - num - 1][y]):
                            Field.move_content(1, field[x - num][y], field[x - num - 1][y])
                        break
                if field[x - num][y].cell_type_id == 2:
                    event.pos.append([x - num, y])
                    break
                num += 1
        elif pos.crds[0] == unit.crds[0]:
            x, y = unit.crds
            num = 1
            while y + num < 10:
                if field[x][y + num].content is not None:
                    field[x][y + num].content.health -= 2
                    if y + num + 1 < 10:
                        if good_cell(field[x][y + num + 1]):
                            Field.move_content(1, field[x][y + num], field[x][y + num + 1])
                        break
                if field[x][y + num].cell_type_id == 2:
                    event.pos.append([x, y + num])
                    break
                num += 1
            num = 1
            while y - num > 0:
                if field[x][y - num].content is not None:
                    field[x][y - num].content.health -= 2
                    if y - num - 1 > -10:
                        if good_cell(field[x][y - num - 1]):
                            Field.move_content(1, field[x][y - num], field[x][y - num - 1])
                        break
                if field[x][y - num].cell_type_id == 2:
                    event.pos.append([x, y - num])
                    break
                num += 1
        pygame.event.post(event)

    def cell_under_attack(self, pos, field, cell):
        if pos.crds[0] == cell.crds[0] and pos.crds[1] > cell.crds[1]:
            x, y = cell.crds
            num = 0
            while y + num < 9:
                num += 1
                if good_cell(field[x][y + num]):
                    field[x][y + num].clicked = True
                else:
                    break
        elif pos.crds[0] == cell.crds[0] and pos.crds[1] < cell.crds[1]:
            x, y = cell.crds
            num = 0
            while y - num > 0:
                num += 1
                field[x][y - num].clicked = True
                if good_cell(field[x][y - num]):
                    field[x][y - num].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] > cell.crds[0]:
            x, y = cell.crds
            num = 0
            while x + num < 9:
                num += 1
                if good_cell(field[x + num][y]):
                    field[x + num][y].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] < cell.crds[0]:
            x, y = cell.crds
            num = 0
            while x - num > 0:
                num += 1
                field[x - num][y].clicked = True
                if good_cell(field[x - num][y]):
                    field[x - num][y].clicked = True
                else:
                    break


class Shield(Unit):
    def show_spellrange(self, field, pos):
        if good_cell(field[pos[0] + 1][pos[1]]):
            field[pos[0] + 1][pos[1]].marked = True
        if good_cell(field[pos[0]][pos[1] + 1]):
            field[pos[0]][pos[1] + 1].marked = True
        if good_cell(field[pos[0] - 1][pos[1]]):
            field[pos[0] - 1][pos[1]].marked = True
        if good_cell(field[pos[0]][pos[1] - 1]):
            field[pos[0]][pos[1] - 1].marked = True

    def cast_spell(self, field, pos, unit):
        if pos.crds[1] == unit.crds[1]:
            x, y = unit.crds
            num = 1
            if field[x + num][y].content is not None and x + num + 1 < 10:
                if good_cell(field[x + num + 1][y]):
                    Field.move_content(1, field[x + num][y], field[x + num + 1][y])
                else:
                    field[x + num][y].content.health -= 1
            elif field[x - num][y].content is not None and x - num - 1 >= 0:
                if good_cell(field[x - num - 1][y]):
                    Field.move_content(1, field[x - num][y], field[x - num - 1][y])
                else:
                    field[x - num][y].content.health -= 1
        elif pos.crds[0] == unit.crds[0]:
            x, y = unit.crds
            num = 1
            if field[x][y + num].content is not None and y + num + 1 < 10:
                if good_cell(field[x][y + num + 1]):
                    Field.move_content(1, field[x][y + num], field[x][y + num + 1])
                else:
                    field[x][y + num].content.health -= 1
            elif field[x][y - num].content is not None and y - num - 1 >= 0:
                if good_cell(field[x][y - num - 1]):
                    Field.move_content(1, field[x][y - num], field[x][y - num - 1])
                else:
                    field[x][y - num].content.health -= 1

    def cell_under_attack(self, pos, field, cell):
        if pos.crds[0] == cell.crds[0] and pos.crds[1] > cell.crds[1]:
            x, y = cell.crds
            for num in range(2):
                if good_cell(field[x][y + num]):
                    field[x][y + num].clicked = True
                else:
                    break
        elif pos.crds[0] == cell.crds[0] and pos.crds[1] < cell.crds[1]:
            x, y = cell.crds
            for num in range(2):
                field[x][y - num].clicked = True
                if good_cell(field[x][y - num]):
                    field[x][y - num].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] > cell.crds[0]:
            x, y = cell.crds
            for num in range(2):
                if good_cell(field[x + num][y]):
                    field[x + num][y].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] < cell.crds[0]:
            x, y = cell.crds
            for num in range(2):
                field[x - num][y].clicked = True
                if good_cell(field[x - num][y]):
                    field[x - num][y].clicked = True
                else:
                    break


class Hiller(Unit):
    def show_spellrange(self, field, pos):
        for num in range(3):
            if good_cell(field[pos[0] + num][pos[1]]):
                field[pos[0] + num][pos[1]].marked = True
            else:
                break
        for num in range(3):
            if good_cell(field[pos[0]][pos[1] + num]):
                field[pos[0]][pos[1] + num].marked = True
            else:
                break
        for num in range(3):
            if good_cell(field[pos[0] - num][pos[1]]):
                field[pos[0] - num][pos[1]].marked = True
            else:
                break
        for num in range(3):
            if good_cell(field[pos[0]][pos[1] - num]):
                field[pos[0]][pos[1] - num].marked = True
            else:
                break

    def cast_spell(self, field, pos, unit):
        if pos.crds[0] == unit.crds[0]:
            x, y = unit.crds
            for num in range(3):
                if field[x + num][y].content is not None:
                    field[x + num][y].content.health += 2
            for num in range(3):
                if field[x - num][y].content is not None:
                    field[x - num][y].content.health += 2
        elif pos.crds[1] == unit.crds[1]:
            x, y = unit.crds
            for num in range(3):
                if field[x][y + num].content is not None:
                    field[x][y + num].content.health += 2
            for num in range(3):
                if field[x][y - num].content is not None:
                    field[x][y - num].content.health += 2

    def cell_under_attack(self, pos, field, cell):
        if pos.crds[0] == cell.crds[0] and pos.crds[1] > cell.crds[1]:
            x, y = cell.crds
            for num in range(3):
                if good_cell(field[x][y + num]):
                    field[x][y + num].clicked = True
                else:
                    break
        elif pos.crds[0] == cell.crds[0] and pos.crds[1] < cell.crds[1]:
            x, y = cell.crds
            for num in range(3):
                field[x][y - num].clicked = True
                if good_cell(field[x][y - num]):
                    field[x][y - num].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] > cell.crds[0]:
            x, y = cell.crds
            for num in range(3):
                if good_cell(field[x + num][y]):
                    field[x + num][y].clicked = True
                else:
                    break
        elif pos.crds[1] == cell.crds[1] and pos.crds[0] < cell.crds[0]:
            x, y = cell.crds
            for num in range(3):
                field[x - num][y].clicked = True
                if good_cell(field[x - num][y]):
                    field[x - num][y].clicked = True
                else:
                    break


class Tower(Unit):
    def mark_range(self, field, range, curr_cell):
        if range == 0:
            return
        if curr_cell[0] < 0 or curr_cell[1] < 0 or curr_cell[0] > 9 or curr_cell[1] > 9:
            return
        field[curr_cell[0]][curr_cell[1]].marked = True
        self.mark_range(field, range - 1, [curr_cell[0] - 1, curr_cell[1]])
        self.mark_range(field, range - 1, [curr_cell[0], curr_cell[1] - 1])
        self.mark_range(field, range - 1, [curr_cell[0] + 1, curr_cell[1]])
        self.mark_range(field, range - 1, [curr_cell[0], curr_cell[1] + 1])

    def show_spellrange(self, field, pos):
        x, y = pos
        self.mark_range(field, 6, (x, y))

    def cast_spell(self, field, pos, unit):
        x, y = unit.crds
        if field[x][y].marked:
            field[x][y].content.health -= 1

    def cell_under_attack(self, pos, field, cell):
        x, y = pos.crds
        if field[x][y].marked:
            field[x][y].clicked = True


class Wizard(Unit):
    def show_spellrange(self, field, pos):
        for i in range(10):
            for j in range(10):
                if field[i][j].content:
                    field[i][j].marked = True

    def cast_spell(self, field, pos, unit):
        x, y = pos.crds
        i, j = unit.crds
        if field[x][y].marked:
            Field.move_content(1, field[x][y], field[i][j])

    def cell_under_attack(self, pos, field, cell):
        x, y = pos.crds
        i, j = cell.crds
        if field[x][y].marked:
            field[x][y].clicked = True
        field[i][j].clicked = True
