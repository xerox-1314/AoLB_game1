import pygame
import os
import sys


class MainWindow:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
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

    def text_generation(self, text, size, color):
        font = pygame.font.Font('D:/Program Files/pycharmprograms/AoLB_game1/data/game_font.ttf', size)
        text = font.render(text, True, color)
        return text

    def add_button(self, text, size, color_text, color_rect, x, y):
        font = pygame.font.Font('D:/Program Files/pycharmprograms/AoLB_game1/data/game_font.ttf', size)
        text = font.render(text, True, color_text)
        pygame.draw.rect(self.screen, color_rect, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 0, 7)
        self.screen.blit(text, (x, y))
        return