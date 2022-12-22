from secondary import load_image
from globals import MOVEMENT_TYPES


class Unit:
    health = 0
    attack_range = 0
    movement_range = 0
    movement_type = MOVEMENT_TYPES['grounded']
    name = ''
    image = ''

    def get_image(self):
        return load_image(self.image, colorkey='black')
