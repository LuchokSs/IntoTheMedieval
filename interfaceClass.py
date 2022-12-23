import pygame
from secondary import load_image, pil_image_to_surface
from globals import EXIT_MENU_EVENT


class Interface:

    images = {}
    interface_sprites = pygame.sprite.Group()

    def __init__(self, surface, player_health):
        self.surface = surface
        self.images["interface_image"] = pygame.sprite.Sprite(self.interface_sprites)
        self.images["interface_image"].image = load_image('data\\interface_images\\interface.png', colorkey='black')
        self.images["interface_image"].rect = pygame.rect.Rect(0, 426, 1000, 274)

        self.images["exit_button"] = pygame.sprite.Sprite(self.interface_sprites)
        self.images["exit_button"].image = load_image('data\\interface_images\\exit_button.png', colorkey='black')
        self.images["exit_button"].rect = pygame.rect.Rect(10, 10, 45, 45)

        self.player_healthBar_status = player_health
        self.images['player_healthBar'] = pygame.sprite.Sprite(self.interface_sprites)
        self.images['player_healthBar'].image = \
            load_image(f'data\\interface_images\\player_healthBar{5 - self.player_healthBar_status}.png',
                       colorkey='black')
        self.images['player_healthBar'].rect = pygame.rect.Rect(860, 10, 140, 32)

    def update(self):
        self.interface_sprites.draw(self.surface)

    def interface_clicked(self, pos):
        if self.images['exit_button'].rect.collidepoint(pos):
            pygame.event.post(EXIT_MENU_EVENT)
