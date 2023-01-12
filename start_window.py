import pygame
from main_window import MainWindow
SIZE = (800, 500)


class StartWindow(MainWindow):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__(width, height)

    def view_window(self):
        all_sprites = pygame.sprite.Group()
        image = self.load_image("welcome_image.png")
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(image, (self.width, self.height))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 0
        sprite.rect.y = 0
        all_sprites.add(sprite)
        all_sprites.draw(self.screen)

        text_play = self.text_generation('Играть!', 35, (224, 103, 184))
        x_play = self.width // 2 - text_play.get_width() // 2
        y_play = self.height // 2 - text_play.get_height() // 2 - 50
        self.add_button('Играть!', 35, (224, 103, 184), (18, 137, 184), x_play, y_play)

        text_store = self.text_generation('Магазин', 30, (224, 103, 184))
        x_store = self.width // 2 - text_store.get_width() // 2
        y_store = y_play + text_play.get_height() + 50
        self.add_button('Магазин', 30, (224, 103, 184), (18, 137, 184), x_store, y_store)
        pygame.display.flip()

        text_exit = self.text_generation('Выйти', 30, (224, 103, 184))
        x_exit = self.width // 2 - text_exit.get_width() // 2
        y_exit = y_store + text_store.get_height() + 30
        self.add_button('Выйти', 30, (224, 103, 184), (18, 137, 184), x_exit, y_exit)
        pygame.display.flip()


if __name__ == '__main__':
    window = StartWindow(*SIZE)
    window.view_window()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

