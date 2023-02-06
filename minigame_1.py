import pygame
import os

SIZE = WIDTH, HEIGHT = (400, 400)
FPS = 20
RECT_SIZE = 50


class Labyrint:
    def __init__(self, namefile, exit_number):
        self.map = list()
        with open(os.path.join('data', 'maps', namefile), 'r', encoding='utf-8') as file:
            for line in file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.rect_size = RECT_SIZE
        self.exit_number = exit_number

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (120, 120, 120), 2: (200, 200, 50)}
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, colors[self.map[i][j]], (j * self.rect_size, i * self.rect_size,
                                 self.rect_size, self.rect_size))
                pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    screen.fill((0, 0, 0))
    labyrint = Labyrint('map1.txt', 2)
    labyrint.render(screen)
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()

