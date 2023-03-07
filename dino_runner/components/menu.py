import pygame

from dino_runner.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH


class Menu:
    hals_screen_heigth = SCREEN_HEIGHT // 2
    hals_screen_width = SCREEN_WIDTH // 2    

    def __init__(self, message, screen):
        screen.fill((255, 255, 255))
        self.font = pygame.font.Font(FONT_STYLE, 30)
        self.text = self.font.render(message, True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.hals_screen_heigth, self.hals_screen_width)

    def update(self):
        pass

    def draw(self):
        pass