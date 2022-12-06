import pygame

from fieldClass import Field
from globals import FPS, FIELD_SIZE


if __name__ == '__main__':
    pygame.init()
    field = pygame.display.set_mode(FIELD_SIZE)

    board = Field()

    running = True

    while running:
        pygame.display.flip()

        field.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.cell_clicked(event.pos)

        board.draw_field(field)
