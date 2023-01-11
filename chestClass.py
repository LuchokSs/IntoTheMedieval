import pygame
import random
from globals import MODES, UNITS
from secondary import load_image


def chest_screen(main_screen):
    game = ChestMenu(main_screen)

    while True:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MODES["EXIT"]
            for elem in game.all_sprites:
                if elem.rect.collidepoint(pos):
                    elem.image = game.render(elem)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if elem.name == "Back":
                            isOpened = True
                            return MODES["END_MENU"], isOpened
                else:
                    elem.image = game.render_selected(elem)

        game.all_sprites.draw(main_screen)
        pygame.display.flip()


class ChestMenu:
    def __init__(self, main_screen):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)
        self.all_sprites = pygame.sprite.Group()
        main_screen.fill((0, 100, 200))

        font_of_game_over = pygame.font.Font(None, 60)
        text = font_of_game_over.render("CONGRATULATIONS", 10, (250, 250, 30))
        main_screen.blit(text, (290, 100))
        pygame.display.update()

        with open('data\\units\\available_units.txt', "r+") as units_file:
            data = units_file.read()
            while True:
                units = []
                for key in UNITS.keys():
                    units.append(key)
                unit = units[random.randint(0, len(UNITS.keys()) - 1)]
                if unit not in data.split():
                    name_of_unit = unit
                    units_file.write(f' {unit}')
                    break
            sprite = pygame.image.load(f'data\\units\\{name_of_unit}\\image.png')
            sprite = pygame.transform.scale(sprite, (320, 200))
            sprite.set_colorkey((0, 0, 0))
            main_screen.blit(sprite, (340, 225))
            pygame.display.update()

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Back", 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 450, 550
        sprite.name = "Back"
        self.all_sprites.add(sprite)

    def render(self, elem):
        return self.main_font.render(elem.name, 1, (250, 30, 250))

    def render_selected(self, elem):
        return self.main_font.render(elem.name, 1, (250, 250, 30))
