import pygame
from main_window import MainWindow, Button
import store_window
import levels_window
SIZE = (800, 500)


class StartWindow(MainWindow):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__(width, height)

    def view_window(self):
        pygame.display.set_caption('Adventures of Little Benjamin')
        all_sprites = pygame.sprite.Group()
        image = self.load_image("welcome_image_new.png")
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(image, (self.width, self.height))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 0
        sprite.rect.y = 0
        all_sprites.add(sprite)
        all_sprites.draw(self.screen)

        name_text = self.text_generation('Adventures of Little Benjamin', 30, (172, 64, 235))
        x_name = self.width // 2 - name_text.get_width() // 2
        y_name = self.height // 2 - name_text.get_height() // 2
        self.screen.blit(name_text, (x_name, y_name - 200))

        text_play = self.text_generation('Играть!', 35, (224, 103, 184))
        x_play = self.width // 2 - text_play.get_width() // 2
        y_play = self.height // 2 - text_play.get_height() // 2 - 20
        self.but_play = Button('Играть!', 35, (172, 64, 235), (233, 153, 236))
        self.but_play.show_button(self.screen, x_play, y_play)

        text_store = self.text_generation('Магазин', 30, (224, 103, 184))
        x_store = self.width // 2 - text_store.get_width() // 2
        y_store = y_play + text_play.get_height() + 50
        self.but_store = Button('Магазин', 30, (172, 64, 235), (233, 153, 236))
        self.but_store.show_button(self.screen, x_store, y_store)

        text_exit = self.text_generation('Выйти', 30, (224, 103, 184))
        x_exit = self.width // 2 - text_exit.get_width() // 2
        y_exit = y_store + text_store.get_height() + 30
        self.but_exit = Button('Выйти', 30, (172, 64, 235), (233, 153, 236))
        self.but_exit.show_button(self.screen, x_exit, y_exit)
        pygame.display.flip()


def main():
    pygame.init()
    window = StartWindow(*SIZE)
    window.view_window()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if window.but_play.check_click(*event.pos) is True:
                        levels_window.main()
                    elif window.but_store.check_click(*event.pos) is True:
                        store_window.main()
                    elif window.but_exit.check_click(*event.pos) is True:
                        run = False
                    else:
                        pass

    pygame.quit()


if __name__ == '__main__':
    main()