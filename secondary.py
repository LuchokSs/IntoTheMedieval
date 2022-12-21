import os

import sys

import pygame

import json_tricks as json

from PIL import Image

from globals import UNITS


def load_image(name: str, colorkey=None) -> pygame.surface:
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def pil_image_to_surface(image, direction=True):

    """PIL >> SURFACE if direction else SURFACE >> PIL"""

    if not direction:
        str_format = 'RGBA'
        raw_str = pygame.image.tostring(image, str_format, False)
        return Image.frombytes(str_format, image.get_size(), raw_str)

    return pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert()


def new_unit(name_of_unit, health, damage, range_of_attack, movement_range, image):
    with open(f"data/{name_of_unit}.json", "w") as write_file:
        data = [health, damage, range_of_attack, movement_range, image]
        json.dump(data, write_file)
        UNITS[name_of_unit] = f"{name_of_unit}.json"
        write_file.close()