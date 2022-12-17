class Unit:
    def __init__(self, hp, damage, range_of_attack, range_of_feet, image):
        self.hp = hp
        self.damage = damage
        self.range_of_attack = range_of_attack
        self.range_of_feet = range_of_feet
        self.image = image

    def change_hp(self, damage_given):
        self.hp -= damage_given

    def give_damage(self):
        return self.damage

    def take_range_of_attack(self):
        return self.range_of_attack

    def take_range_of_feet(self):
        return self.range_of_feet
