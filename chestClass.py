import pygame
from globals import MODES


def chest_screen(main_screen):
    game = EndgameMenu()

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
                        if elem.name == "Back":
                            isOpened = True
                            return MODES["END_MENU"], isOpened
                else:
                    elem.image = game.render_selected(elem)

        game.all_sprites.draw(main_screen)
        pygame.display.flip()


class EndgameMenu:
    def __init__(self):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)
        self.all_sprites = pygame.sprite.Group()

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Back", 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 400, 350
        sprite.name = "Back"
        self.all_sprites.add(sprite)

    def render(self, elem):
        return self.main_font.render(elem.name, 1, (250, 30, 250))

    def render_selected(self, elem):
        return self.main_font.render(elem.name, 1, (250, 250, 30))
