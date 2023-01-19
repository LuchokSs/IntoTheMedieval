import random
from secondary import load_image


def move_content(field, cell1, cell2):
    cell1 = field[cell1[0]][cell1[1]]
    cell2 = field[cell2[0]][cell2[1]]
    cell1.content, cell2.content = cell2.content, cell1.content


class EnemyWarrior:
    movement_range = 3
    image = '.\\data\\units\\warrior\\image_test.png'
    target = None
    name = 'e'
    health = 3

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
                move_content(field, pos, pos1)
                self.target = (pos1[0] - pos[0], pos1[1] - pos[1])
                break
        else:
            while True:
                dx, dy = random.randint(-3, 3), random.randint(-3, 1)
                try:
                    if (field[pos[0] + dx][pos[1] + dy].cell_type_id == 0 and dx != dy != 0
                            and pos[0] + dx > 0 and pos[1] + dy > 0):
                        move_content(field, pos, [pos[0] + dx, pos[1] + dy])
                        break
                except IndexError:
                    continue


    def get_image(self):
        return load_image(self.image, colorkey='black')