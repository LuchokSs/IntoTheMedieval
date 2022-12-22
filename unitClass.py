from secondary import load_image


class Unit:
    health = 0
    damage = 0
    attack_range = 0
    movement_range = 0
    name = ''
    image = ''

    def get_image(self):
        return load_image(self.image, colorkey='black')
