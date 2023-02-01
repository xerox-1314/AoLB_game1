import pygame
import os
import sys


class MainWindow:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def load_image(self, name, directory=None, colorkey=None):
        if directory is not None:
            fullname = os.path.join('data', directory, name)
        else:
            fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
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
        text = font.render(text, False, color)
        return text


class Button:
    def __init__(self, text, size_text, color_text, color_rect):
        self.text = text
        self.size_text = size_text
        self.color_text = color_text
        self.color_rect = color_rect

    def show_button(self, screen, x, y):
        self.x = x
        self.y = y
        font = pygame.font.Font('D:/Program Files/pycharmprograms/AoLB_game1/data/game_font.ttf', self.size_text)
        text = font.render(self.text, True, self.color_text)
        self.width = text.get_width() + 20
        self.height = text.get_height() + 20
        pygame.draw.rect(screen, self.color_rect, (x - 10, y - 10, self.width, self.height), 0, 7)
        screen.blit(text, (x, y))

    def check_click(self, x, y):
        return True if ((self.x <= x <= (self.x + self.width)) and (self.y <= y <= (self.y + self.height))) else False
