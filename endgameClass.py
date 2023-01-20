import pygame
from secondary import load_image
from globals import MODES, FIELD_SIZE


def end_screen(main_screen, isOpened):
    game = EndgameMenu(isOpened, main_screen)

    while True:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return MODES["EXIT"]
            for elem in game.all_sprites:
                if elem.rect.collidepoint(pos):
                    elem.image = game.render(elem)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if elem.name == "Open Chest":
                            return MODES['CHEST']
                        elif elem.name == "Main Menu":
                            return MODES["START_MENU"]
                        elif elem.name == "New Game":
                            return MODES["FIELD"]
                else:
                    elem.image = game.render_selected(elem)

        game.all_sprites.draw(main_screen)
        pygame.display.flip()


class EndgameMenu:
    def __init__(self, isOpened, main_screen):
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)
        self.all_sprites = pygame.sprite.Group()
        main_screen.blit(pygame.transform.scale(load_image(".\\data\\interface_images\\background.png"), FIELD_SIZE),
                         (0, 0))

        sprite = pygame.sprite.Sprite()
        if isOpened:
            name = "New Game"
        else:
            name = "Open Chest"
        sprite.image = self.main_font.render(name, 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 400, 300
        sprite.name = name
        self.all_sprites.add(sprite)

        sprite = pygame.sprite.Sprite()
        sprite.image = self.main_font.render("Main Menu", 1, (250, 250, 30))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x, sprite.rect.y = 400, 400
        sprite.name = "Main Menu"
        self.all_sprites.add(sprite)

        font_of_game_over = pygame.font.Font(None, 100)
        text = font_of_game_over.render("GAME OVER", 10, (100, 20, 20))
        main_screen.blit(text, (290, 100))
        pygame.display.update()

    def render(self, elem):
        return self.main_font.render(elem.name, 1, (250, 30, 250))

    def render_selected(self, elem):
        return self.main_font.render(elem.name, 1, (250, 250, 30))
