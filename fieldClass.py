import random

from cellClass import Cell
from globals import squad, UNITS, CELL_SIZE, EXIT_MENU_EVENT, MOVING_UNIT_EVENT, SPELLCAST_UNIT_EVENT, CELL_TYPES
from globals import HOUSE_DAMAGED_EVENT
import json_tricks as json
from interfaceClass import Interface
from secondary import load_image
from unitClass import EnemyWarrior

import pygame


LAST_CLICKED = None


def field_mode(main_screen, *args, **kwargs):
    """Функция с игровым цЫклом поля."""

    running = True
    moving_phase = False
    attacking_phase = False

    STAGE = 0  # 0 - ход бота. 1 - ход игрока.

    board = Field(main_screen, running)

    unit_num = 0

    while unit_num < 3:
        pygame.display.flip()

        main_screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if board.set_unit(pygame.mouse.get_pos(), squad[unit_num], marked=True):
                    unit_num += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.interface.interface_clicked(event.pos)
            if event == EXIT_MENU_EVENT:
                return 0

        main_screen.blit(board.main_font.render('Установите персонажей на позиции', 1, (150, 150, 30)), (220, 10))

        board.draw_field()

    board.clear_marks()

    while running:
        pygame.display.flip()

        if STAGE == 0:
            board.attack_enemies()
            board.summon_enemies()
            if len(board.enemy_list) == 0:
                board.generate_enemy(3)
            board.prepare_enemies()

            STAGE = 1

        if STAGE == 1:
            main_screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 3
                if event == HOUSE_DAMAGED_EVENT:
                    for pos in event.pos:
                        cell = board.field[pos[0]][pos[1]]
                        if not cell.destroyed:
                            cell.sprite = load_image(f'''data\\cell_images\\HOUSE\\HOUSE_BURNING.png''', colorkey='black')
                            cell.destroyed = True
                            board.player_health -= 1
                            if board.player_health == 0:
                                return 2
                if event == MOVING_UNIT_EVENT:
                    if not LAST_CLICKED.content.turns_left['move']:
                        pass
                    board.mark_range(LAST_CLICKED.content.movement_range, LAST_CLICKED.crds, first=True)
                    moving_phase = True
                if event == SPELLCAST_UNIT_EVENT:
                    if not LAST_CLICKED.content.turns_left['attack']:
                        pass
                    LAST_CLICKED.content.show_spellrange(board.field, LAST_CLICKED.crds)
                    attacking_phase = True
                if event.type == pygame.MOUSEMOTION and attacking_phase:
                    board.cell_under_attack(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and attacking_phase:
                    if board.use_spell(LAST_CLICKED, event.pos):
                        attacking_phase = False
                        LAST_CLICKED.content.turns_left['attack'] = False
                        board.clear_marks()
                elif event.type == pygame.MOUSEBUTTONDOWN and moving_phase:
                    if board.move_unit(LAST_CLICKED, event.pos):
                        moving_phase = False
                        LAST_CLICKED.content.turns_left['move'] = False
                        board.clear_marks()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.clicked(event.pos)
                if event == EXIT_MENU_EVENT:
                    return 0

        board.draw_field()


class Field:
    """Класс поля."""

    patterns_name = ["HILLS_PATTERNS"]  # WIP , "LAKE_PATTERNS", "FOREST_PATTERNS", "CITY_PATTERNS"
    patterns_num = 3
    player_health = 4

    enemy_list = []

    def __init__(self, surface, running):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)

        self.surface = surface
        self.running = running

        self.interface = Interface(self.surface, self.player_health)
        self.interface.update()

        self.field = \
            open(f'''.\\data\\field_patterns\\{self.patterns_name[random.randint(0, len(self.patterns_name) - 1)]}/{
        random.randint(1, self.patterns_num)}.txt''',
                 'r').readlines()
        marked_list = self.field[10:]
        self.starting_pos = marked_list
        self.field = list(map(str.split, self.field[:10]))

        xs = CELL_SIZE[0] // 2
        ys = CELL_SIZE[1] // 2

        for row in range(len(self.field)):
            for cell in range(len(self.field[row])):
                points = ((2 * xs, ys), (xs, 2 * ys), (0, ys), (xs, 0))
                pos = 100 + xs * (row + cell), 350 + ys * (row - cell)
                self.field[row][cell] = Cell(points, pos, int(self.field[row][cell]), (row, cell))

        for i in marked_list:
            pos = i.split()
            self.mark_cell(self.field[int(pos[0])][int(pos[1])], True)

    def draw_field(self):

        """Изображает поле на хосте."""

        self.interface.player_healthBar_status = self.player_health
        for row in self.field:
            for cell in row:
                cell.draw_cell(self.surface)

        if LAST_CLICKED is None or LAST_CLICKED.content is None:
            self.interface.hide_unit_interface()
        self.interface.update()

    def find_clicked_cell(self, pos):
        for row in self.field:
            for cell in row:
                if cell.is_clicked(pos):
                    return cell
        return None

    def mark_cell(self, cell, condition):
        cell.marked = condition

    def clicked(self, pos):

        """Обработка событий нажатия. Получает на вход координаты в виде tuple."""

        cell = self.find_clicked_cell(pos)
        if cell is not None:
            global LAST_CLICKED
            if LAST_CLICKED is not None:
                LAST_CLICKED.clicked = False
                LAST_CLICKED.tick = 0
            cell.clicked = True
            cell.tick = 0
            LAST_CLICKED = cell

            if cell.content is not None:
                self.interface.show_unit_interface(cell.content)

        if LAST_CLICKED is not None and LAST_CLICKED.content is not None:
            self.interface.unit_management(pos, LAST_CLICKED)

        self.interface.interface_clicked(pos)

    def set_unit(self, pos, unit_name, marked=False):

        """Загрузка юнита из json файла, расположенного по пути, указанному в глобальном словаре,
                  в соответствии с именем юнита на указанную точку."""

        cell = self.find_clicked_cell(pos)
        if cell is None:
            return False

        if (marked and cell.marked and cell.content is None) or not marked:
            with open(UNITS[unit_name], "r") as file:
                cell.content = json.load(file)
                return True
        return False

    def generate_enemy(self, num):
        cnt = 0
        while cnt < num:
            cell = random.randint(6, 8), random.randint(1, 8)
            self.field[cell[0]][cell[1]].enemy_summon_mark = (True
                                                              if self.field[cell[0]][cell[1]].cell_type_id == 0
                                                              and not self.field[cell[0]][cell[1]].enemy_summon_mark
                                                              else False)
            cnt += 1 if self.field[cell[0]][cell[1]].enemy_summon_mark else 0

    def summon_enemies(self):
        for row in self.field:
            for cell in row:
                if cell.enemy_summon_mark:
                    cell.enemy_summon_mark = False
                    cell.content = EnemyWarrior()
                    self.enemy_list.append(cell.content)

    def prepare_enemies(self):
        for unit in self.enemy_list:
            unit.move()

    def attack_enemies(self):
        for row in self.field:
            for cell in row:
                if cell.content is EnemyWarrior:
                    cell.content.attack(self.field, cell)

    def move_unit(self, unit, pos):
        cell = self.find_clicked_cell(pos)
        if cell is None:
            return False
        if cell.marked:
            self.move_content(unit, cell)
            global LAST_CLICKED
            LAST_CLICKED.clicked = False
            LAST_CLICKED.tick = 0
        return True

    def use_spell(self, unit, pos):
        cell = self.find_clicked_cell(pos)
        if cell is None:
            return False
        if cell.marked:
            unit.content.cast_spell(self.field, cell, unit)
            global LAST_CLICKED
            LAST_CLICKED.clicked = False
            LAST_CLICKED.tick = 0
        return True

    def clear_marks(self, clicked=True, marked=True, tick=True, enemy_summon_mark=False):
        for row in self.field:
            for cell in row:
                cell.marked = False if marked else cell.marked
                cell.clicked = False if clicked else cell.clicked
                cell.tick = 0 if tick else cell.tick
                cell.enemy_summon_mark = False if enemy_summon_mark else cell.enemy_summon_mark

    def mark_range(self, range, curr_cell, movement_type=0, first=False):
        if range == 0:
            return
        try:
            if self.field[curr_cell[0]][curr_cell[1]].marked:
                return
            if curr_cell[0] < 0 or curr_cell[1] < 0:
                return
        except IndexError:
            return
        if first:
            self.field[curr_cell[0]][curr_cell[1]].marked = True
        if movement_type == 0:
            if self.field[curr_cell[0]][curr_cell[1]].cell_type_id != 0:
                return
            else:
                self.field[curr_cell[0]][curr_cell[1]].marked = True
                self.mark_range(range - 1, [curr_cell[0] - 1, curr_cell[1]], movement_type)
                self.mark_range(range - 1, [curr_cell[0], curr_cell[1] - 1], movement_type)
                self.mark_range(range - 1, [curr_cell[0] + 1, curr_cell[1]], movement_type)
                self.mark_range(range - 1, [curr_cell[0], curr_cell[1] + 1], movement_type)
        if movement_type == 1:
            self.field[curr_cell[0]][curr_cell[1]].marked = True
            self.mark_range(range - 1, [curr_cell[0] - 1, curr_cell[1]], movement_type)
            self.mark_range(range - 1, [curr_cell[0], curr_cell[1] - 1], movement_type)
            self.mark_range(range - 1, [curr_cell[0] + 1, curr_cell[1]], movement_type)
            self.mark_range(range - 1, [curr_cell[0], curr_cell[1] + 1], movement_type)

    def move_content(self, cell1, cell2):
        cell1.content, cell2.content = cell2.content, cell1.content

    def cell_under_attack(self, pos):
        pos = self.find_clicked_cell(pos)
        if pos is None or not pos.marked:
            return
        if pos.clicked:
            self.clear_marks(marked=False, tick=False)
        else:
            self.clear_marks(marked=False)
        LAST_CLICKED.content.cell_under_attack(pos, self.field, LAST_CLICKED)
