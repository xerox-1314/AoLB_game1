import pygame
from main_window import MainWindow
import database_work as db
import os

SIZE = (500, 400)


class LevelsWindow(MainWindow):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__(width, height)

    def view_window(self):
        pygame.display.set_caption('Levels: AoLB')
        self.screen.fill((204, 152, 255))
        text = self.text_generation('Levels', 30, (0, 153, 153))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 15))

        levels_list = db.get_all_levels()
        x, y = 60, 120
        r = 30
        for i in range(len(levels_list)):
            pygame.draw.circle(self.screen, (172, 64, 235), (x, y), r)
            num = self.text_generation(str(levels_list[i][0]), 25, (0, 153, 153))
            name = self.text_generation(str(levels_list[i][1]), 20, (0, 153, 153))
            self.screen.blit(num, (x - (num.get_width() // 2), y - num.get_height() // 2))
            self.screen.blit(name, (x - name.get_width() // 2, y + r // 2 + 10))
            if x <= (self.width - r - 30):
                x += r + 60
            else:
                x = 60
                y += r // 2 + 50
            pygame.display.flip()

def main():
    window = LevelsWindow(*SIZE)
    window.view_window()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()
