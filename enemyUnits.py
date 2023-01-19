import random


def move_content(self, cell1, cell2):
    cell1.content, cell2.content = cell2.content, cell1.content


class EnemyWarrior:
    movement_range = 3
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
                move_content(pos, pos1)
                self.target = (pos1[0] - pos[0], pos1[1] - pos[1])
                break
        else:
            while True:
                dx, dy = random.randint(-3, 3), random.randint(-3, 1)
                if field[pos[0] + dx][pos[1] + dy].cell_type_id == 0 and dx != dy != 0:
                    move_content(pos, field[pos[0] + dx][pos[1] + dy])
                    break
