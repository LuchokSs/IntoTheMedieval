import pygame
from secondary import load_image
from globals import MODES


def start_screen(main_screen):
    game = Menu()

    while True:
        pos = pygame.mouse.get_pos()
        main_screen.fill((0, 100, 200))

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
    def __init__(self):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)
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
        return self.main_font.render(elem.name, 1, (250, 30, 250))

    def render_selected(self, elem):
        return self.main_font.render(elem.name, 1, (250, 250, 30))


class SecondPhase:
    def __init__(self, screen):
        self.screen = screen
        self.main_font = pygame.font.Font(None, 36)
        self.characters = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("data\\units\\IMG_0055.png"), (100, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 100
        sprite.name = "1"
        self.characters.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("data\\units\\IMG_0055.png"), (100, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 280
        sprite.name = "2"
        self.characters.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("data\\units\\IMG_0055.png"), (100, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 600, 460
        sprite.name = "3"
        self.characters.add(sprite)

        self.btn = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Start", 1, (0, 0, 0))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 900, 650
        self.btn.add(sprite)

    def show_win(self):
        while True:
            self.screen.fill((0, 100, 200))
            image1 = pygame.Surface([400, 170])
            image1.fill("green")
            self.screen.blit(image1, (590, 90))

            image2 = pygame.Surface([400, 170])
            image2.fill("green")
            self.screen.blit(image2, (590, 270))

            image3 = pygame.Surface([400, 170])
            image3.fill("green")
            self.screen.blit(image3, (590, 450))
            pos = pygame.mouse.get_pos()

            self.characters.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                for elem in self.characters:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.character_selection()
                for elem in self.btn:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        return 1
            self.btn.draw(self.screen)
            pygame.display.flip()

    def character_selection(self):
        s = pygame.Surface((1000, 700), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        image = pygame.Surface([400, 400])
        image.fill(pygame.Color("white"))
        s.blit(image, (300, 150))

        group = pygame.sprite.Group()
        btn_ok = pygame.sprite.Sprite()
        btn_ok.image = self.main_font.render("OK", 1, (0, 0, 0))
        btn_ok.rect = btn_ok.image.get_rect()
        btn_ok.rect.x, btn_ok.rect.y = 650, 520
        group.add(btn_ok)
        group.draw(s)

        self.screen.blit(s, (0, 0))

        while True:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    return -1
                for elem in group:
                    if elem.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        return

            group.draw(s)
            pygame.display.flip()
