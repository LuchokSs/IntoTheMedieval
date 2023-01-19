import pygame
from secondary import load_image
from globals import MODES, IMAGE_UNITS, squad, available_units, FIELD_SIZE, DESCRIPTION_UNITS


def start_screen(main_screen):
    "ф-ия запуска стартового окна"
    game = Menu()

    while True:
        pos = pygame.mouse.get_pos()
        main_screen.blit(pygame.transform.scale(load_image(".\\data\\interface_images\\background.png"), FIELD_SIZE),
                         (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MODES["EXIT"]
            for elem in game.all_sprites:
                if elem.rect.collidepoint(pos):
                    elem.image = game.render(elem)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if elem.name == "Play":
                            menu = SecondPhase(main_screen)
                            res = menu.show_win()
                            if res == 1:
                                return MODES['FIELD']
                            else:
                                return MODES["EXIT"]
                        elif elem.name == "Quit":
                            return MODES["EXIT"]
                else:
                    elem.image = game.render_selected(elem)

        game.all_sprites.draw(main_screen)
        pygame.display.flip()


class Menu:
    "класс стартового окна"
    def __init__(self):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 70)
        self.all_sprites = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Play", 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 425, 250
        sprite.name = "Play"
        self.all_sprites.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Quit", 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 425, 350
        sprite.name = "Quit"
        self.all_sprites.add(sprite)

    def render(self, elem):
        "ф-ия подсвечивает выделенную кнопку"
        return self.main_font.render(elem.name, 1, (250, 30, 250))

    def render_selected(self, elem):
        "ф-ия возвращает кнопку в нейтральное положение"
        return self.main_font.render(elem.name, 1, (250, 250, 30))


class SecondPhase:
    "Класс второго этапа меню. Выбор отряда"
    def __init__(self, screen):
        self.screen = screen
        self.main_font = pygame.font.Font(None, 36)

    def show_win(self):
        "ф-ия запуска второго этапа меню"
        characters = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        im = load_image(IMAGE_UNITS[squad[0]])
        im.set_colorkey((0, 0, 0))
        im.set_alpha()
        sprite.image = pygame.transform.scale(im, (150, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 100
        sprite.name = "1"
        characters.add(sprite)

        sprite = pygame.sprite.Sprite()
        im = load_image(IMAGE_UNITS[squad[1]])
        im.set_colorkey((0, 0, 0))
        im.set_alpha()
        sprite.image = pygame.transform.scale(im, (150, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 280
        sprite.name = "2"
        characters.add(sprite)

        sprite = pygame.sprite.Sprite()
        im = load_image(IMAGE_UNITS[squad[2]])
        im.set_colorkey((0, 0, 0))
        im.set_alpha()
        sprite.image = pygame.transform.scale(im, (150, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 460
        sprite.name = "3"
        characters.add(sprite)

        btn = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Start", 1, (0, 0, 0))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 900, 650
        btn.add(sprite)

        while True:
            self.screen.fill((135, 181, 122))

            self.screen.blit(pygame.transform.scale(load_image(".\\data\\interface_images\\background.png"),
                                                    (530, 530)), (30, 90))

            font = pygame.font.Font(None, 30)
            image1 = pygame.Surface([400, 170])
            image1.fill((189, 198, 164))
            self.screen.blit(image1, (590, 90))
            text = DESCRIPTION_UNITS[squad[0]]
            text_coord = 90
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                text_coord += 20
                self.screen.blit(string_rendered, (740, text_coord))

            image2 = pygame.Surface([400, 170])
            image2.fill((189, 198, 164))
            self.screen.blit(image2, (590, 270))
            text = DESCRIPTION_UNITS[squad[1]]
            text_coord = 270
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                text_coord += 20
                self.screen.blit(string_rendered, (740, text_coord))

            image3 = pygame.Surface([400, 170])
            image3.fill((189, 198, 164))
            self.screen.blit(image3, (590, 450))
            text = DESCRIPTION_UNITS[squad[2]]
            text_coord = 450
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                text_coord += 20
                self.screen.blit(string_rendered, (740, text_coord))
            pos = pygame.mouse.get_pos()

            characters.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                for elem in characters:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.character_selection(elem)
                        im = load_image(IMAGE_UNITS[squad[int(elem.name) - 1]])
                        im.set_colorkey((0, 0, 0))
                        im.set_alpha()
                        elem.image = pygame.transform.scale(im, (150, 150))
                for elem in btn:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        return 1
            btn.draw(self.screen)
            characters.draw(self.screen)
            pygame.display.flip()

    def character_selection(self, spr):
        "ф-ия выбора юнита в отряд"
        global squad
        s = pygame.Surface(FIELD_SIZE)
        s.blit(pygame.transform.scale(load_image(".\\data\\interface_images\\background.png"), FIELD_SIZE),
               (0, 0))
        pygame.draw.rect(s, (255, 255, 255), (300, 150, 400, 400), 0)

        group = pygame.sprite.Group()
        btn_ok = pygame.sprite.Sprite()
        btn_ok.image = self.main_font.render("OK", 1, (0, 0, 0))
        btn_ok.rect = btn_ok.image.get_rect()
        btn_ok.rect.x, btn_ok.rect.y = 650, 525
        group.add(btn_ok)
        group.draw(s)

        arrows = pygame.sprite.Group()
        btn_right = pygame.sprite.Sprite()
        btn_right.image = pygame.image.load("data\\interface_images\\arrow_right.png")
        btn_right.rect = btn_right.image.get_rect()
        btn_right.rect.x, btn_right.rect.y = 650, 330
        btn_right.name = "+"
        arrows.add(btn_right)

        btn_left = pygame.sprite.Sprite()
        btn_left.image = pygame.image.load("data\\interface_images\\arrow_left.png")
        btn_left.rect = btn_left.image.get_rect()
        btn_left.rect.x, btn_left.rect.y = 310, 330
        btn_left.name = "-"
        arrows.add(btn_left)
        arrows.draw(s)

        character = pygame.sprite.Group()
        im2 = pygame.sprite.Sprite()
        im = load_image(IMAGE_UNITS[squad[int(spr.name) - 1]])
        im.set_colorkey((0, 0, 0))
        im.set_alpha()
        im2.image = pygame.transform.scale(im, (300, 300))
        im2.rect = im2.image.get_rect()
        im2.rect.x, im2.rect.y = 340, 170
        character.add(im2)

        self.screen.blit(s, (0, 0))

        while True:
            im = load_image(IMAGE_UNITS[squad[int(spr.name) - 1]])
            im.set_colorkey((0, 0, 0))
            im.set_alpha()
            im2.image = pygame.transform.scale(im, (300, 300))
            character.draw(s)

            font = pygame.font.Font(None, 30)
            text = DESCRIPTION_UNITS[squad[int(spr.name) - 1]]
            text_coord = 740
            for line in text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                text_coord += 20
                s.blit(string_rendered, (170, text_coord))

            self.screen.blit(s, (0, 0))

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    return -1
                for el in arrows:
                    if el.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        a = squad[int(spr.name) - 1]
                        fl = False
                        if el.name == "+":
                            for key in available_units:
                                if fl:
                                    squad[int(spr.name) - 1] = key
                                    fl = False
                                if key == a:
                                    fl = True
                            if a == squad[int(spr.name) - 1]:
                                squad[int(spr.name) - 1] = list(IMAGE_UNITS.keys())[0]
                        if el.name == "-":
                            sp = available_units
                            for key in sp[::-1]:
                                if fl:
                                    squad[int(spr.name) - 1] = key
                                    fl = False
                                if key == a:
                                    fl = True
                            if a == squad[int(spr.name) - 1]:
                                squad[int(spr.name) - 1] = list(IMAGE_UNITS.keys())[-1]
                for elem in group:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        return

            self.screen.blit(s, (0, 0))
            pygame.display.flip()
