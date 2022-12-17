import json_tricks as json


class Unit:
    def __init__(self, name_of_json_file):
        with open(name_of_json_file, "r") as read_file:
            data = json.load(read_file)
            self.hp = data[0]
            self.damage = data[1]
            self.range_of_attack = data[2]
            self.range_of_movement = data[3]
            self.image = data[4]
            read_file.close()