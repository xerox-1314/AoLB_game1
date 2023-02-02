import pygame
from main_window import MainWindow, Button
import database_work as db
import level_base
import start_window
import os

SIZE = (500, 400)


class LevelsWindow(MainWindow):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.levels_list = db.get_all_levels()
        super().__init__(width, height)

    def view_window(self):
        pygame.display.set_caption('Levels: AoLB')
        self.screen.fill((204, 152, 255))
        text = self.text_generation('Levels', 30, (0, 153, 153))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 15))
        self.exit_but = Button('Назад', 15, (255, 255, 255), (233, 183, 235))
        self.exit_but.show_button(self.screen, 30, 30)

        x, y = 60, 120
        r = 30
        for i in range(len(self.levels_list)):
            pygame.draw.circle(self.screen, (172, 64, 235), (x, y), r)
            num = self.text_generation(str(self.levels_list[i][0]), 25, (0, 153, 153))
            name = self.text_generation(str(self.levels_list[i][1]), 20, (0, 153, 153))
            self.screen.blit(num, (x - (num.get_width() // 2), y - num.get_height() // 2))
            self.screen.blit(name, (x - name.get_width() // 2, y + r // 2 + 10))
            if x <= (self.width - r - 30):
                x += r + 60
            else:
                x = 60
                y += r // 2 + 50
            pygame.display.flip()

    def check_click(self, x_mouse, y_mouse):
        x, y = 60, 120
        r = 30
        for i in range(len(self.levels_list)):
            if (x - r) <= x_mouse <= (x + r) and (y - r) <= y_mouse <= (y + r):
                SIZE = width, height = (600, 360)
                window = pygame.display.set_mode(SIZE)
                level_base.level_generation(self.levels_list[i][2])
            if x <= (self.width - r - 30):
                x += r + 60
            else:
                x = 60
                y += r // 2 + 50
        if self.exit_but.x <= x_mouse <= self.exit_but.x + self.exit_but.width and \
        self.exit_but.y <= y_mouse <= self.exit_but.y + self.exit_but.height:
            start_window.main()


def main():
    window = LevelsWindow(*SIZE)
    window.view_window()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    window.check_click(*event.pos)

    pygame.quit()

if __name__ == '__main__':
    main()
