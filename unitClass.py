import json


class Unit:
    def __init__(self, name_of_json_file):
        with open(name_of_json_file, "r") as read_file:
            data = json.load(read_file)
            self.hp = data[0]
            self.damage = data[1]
            self.range_of_attack = data[2]
            self.range_of_feet = data[3]
            self.image = data[4]
            read_file.close()

    def change_hp(self, damage_given):
        self.hp -= damage_given

    def give_damage(self):
        return self.damage

    def take_range_of_attack(self):
        return self.range_of_attack

    def take_range_of_feet(self):
        return self.range_of_feet
