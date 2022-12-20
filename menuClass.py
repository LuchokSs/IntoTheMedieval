import pygame
import sys
from globals import FIELD_SIZE, MODES


class Menu:
    def __init__(self, screen, buttons):
        self.window = screen
        self.buttons = buttons
        pygame.font.init()
        self.main_font = pygame.font.Font(None, 48)
        self.screen = pygame.Surface(FIELD_SIZE)

    def render(self, window, num_btn):
        for btn in self.buttons:
            if num_btn == btn[5]:
                window.blit(self.main_font.render(btn[2], 1, btn[4]), (btn[0], btn[1]))
            else:
                window.blit(self.main_font.render(btn[2], 1, btn[3]), (btn[0], btn[1]))

    def menu(self):
        done = True
        num = 0
        while done:
            self.window.fill((0, 100, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if num > 0:
                            num -= 1
                    if event.key == pygame.K_DOWN:
                        if num < len(self.buttons):
                            num += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if num == 0:
                        done = False
                    if num == 1:
                        sys.exit()

            mp = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn[0] < mp[0] < btn[0] + 155 and btn[1] < mp[1] < btn[1] + 50:
                    num = btn[5]
            self.render(self.screen, num)

            self.window.blit(self.screen, (0, 0))
            pygame.display.flip()


def start_screen(main_screen):
    buttons = [(450, 300, "Play", (250, 250, 30), (250, 30, 250), 0),
               (450, 350, "Quit", (250, 250, 30), (250, 30, 250), 1)]
    game = Menu(main_screen, buttons)
    game.menu()
    return MODES['FIELD']