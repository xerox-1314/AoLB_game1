import pygame
from main_window import MainWindow, Button
import database_work as db
import start_window
import os

SIZE = (800, 500)


class StoreWindow(MainWindow):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_sprites = pygame.sprite.Group()
        self.width_rect, self.height_rect = 300, 350
        self.x_rect = self.width // 2 - self.width_rect // 2
        self.y_rect = (self.height + 60) // 2 - self.height_rect // 2
        self.x_left, self.y_left = 50, (self.height + 60) // 2 - 30
        self.x_right, self.y_right = self.width - 80, (self.height + 60) // 2 - 30
        self.width_rl = 50
        self.character_status = 0

        self.characters_list = db.get_characters()
        self.character_now = 0
        super().__init__(width, height)

    def sprites_generation(self):
        image = self.load_image('strela.png')
        sprite_1 = pygame.sprite.Sprite()
        sprite_2 = pygame.sprite.Sprite()
        sprite_1.image, sprite_2.image = pygame.transform.scale(image, (50, 50)), pygame.transform.scale(image, (50, 50))
        sprite_1.image = pygame.transform.flip(sprite_1.image, True, False)
        sprite_1.rect, sprite_2.rect = sprite_1.image.get_rect(), sprite_1.image.get_rect()
        sprite_1.rect.x, sprite_1.rect.y = self.x_left, self.y_left
        sprite_2.rect.x, sprite_2.rect.y = self.x_right, self.y_right
        self.all_sprites.add(sprite_1, sprite_2)

    def view_window(self):
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption('Store: AoLB')
        pygame.draw.rect(self.screen, (172, 64, 235), (0, 0, self.width, 60))
        count_text = self.text_generation(f'Золотыми {str(db.get_count_now())} B', 30, (255, 255, 255))
        self.screen.blit(count_text, (self.width - count_text.get_width() - 20, 8))
        self.exit_but = Button('Назад', 15, (255, 255, 255), (233, 183, 235))
        self.exit_but.show_button(self.screen, 30, 18)
        pygame.draw.rect(self.screen, (233, 183, 235), (self.x_rect, self.y_rect, self.width_rect, self.height_rect), 0, 10)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        self.sprite_now = pygame.sprite.Sprite(self.all_sprites)

    def view_character(self):
        image = self.load_image(self.characters_list[self.character_now][5], directory='characters', colorkey=-1)
        self.sprite_now.image = pygame.transform.scale(image, (250, 300))
        self.sprite_now.rect = self.sprite_now.image.get_rect()
        self.sprite_now.rect.x, self.sprite_now.rect.y = self.x_rect + 20, self.y_rect + 10

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

        name = self.text_generation(self.characters_list[self.character_now][2], 25, (255, 255, 255))
        count = self.text_generation(str(self.characters_list[self.character_now][3]) + ' B', 30, (255, 255, 255))
        self.screen.blit(name, (30, 60 + 30))
        self.screen.blit(count, (30, 60 + 30 + name.get_height() + 20))

        if self.characters_list[self.character_now][4] == 1:
            if db.get_character_now()[0] == self.characters_list[self.character_now][0]:
                self.character_status = 0
                text = self.text_generation('Выбран!', 25, (172, 64, 235))
                self.screen.blit(text, (self.x_left - 20, self.y_left + 100))
            else:
                self.character_status = 1
                self.but = Button('Выбрать', 25, (255, 255, 255), (172, 64, 235))
                self.but.show_button(self.screen, self.x_left - 20, self.y_left + 100)
        else:
            self.character_status = 2
            self.but = Button('Купить', 25, (255, 255, 255), (172, 64, 235))
            self.but.show_button(self.screen, self.x_left, self.y_left + 100)
        pygame.display.flip()

    def check_clicked(self, x, y):
        if self.x_left <= x <= self.x_left + self.width_rl and self.y_left <= y <= self.y_left + self.width_rl:
            self.character_now -= 1
            self.character_now %= len(self.characters_list)
            self.all_sprites = pygame.sprite.Group()
            self.sprites_generation()
            self.view_window()
            self.view_character()
        elif self.x_right <= x <= self.x_right + self.width_rl and self.y_right <= y <= self.y_right + self.width_rl:
            self.character_now += 1
            self.character_now %= len(self.characters_list)
            self.all_sprites = pygame.sprite.Group()
            self.sprites_generation()
            self.view_window()
            self.view_character()
        elif self.exit_but.x <= x <= self.exit_but.x + self.exit_but.width and \
                self.exit_but.y <= y <= self.exit_but.y + self.exit_but.height:
            start_window.main()

    def error_buyed(self):
        text = self.text_generation('Недостаточно монет!', 15, (255, 255, 255))
        self.screen.blit(text, (self.x_rect + self.width_rect // 2 - text.get_width() // 2, self.y_rect + self.height_rect + 10))
        pygame.display.flip()


def main():
    pygame.init()
    window = StoreWindow(*SIZE)
    window.sprites_generation()
    window.view_window()
    window.view_character()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    window.check_clicked(*event.pos)
                    if window.character_status == 1 and window.but.check_click(*event.pos):
                        db.change_character(window.characters_list[window.character_now][0])
                        window.view_window()
                        window.view_character()
                    elif window.character_status == 2 and window.but.check_click(*event.pos):
                        result = db.buy_character(window.characters_list[window.character_now][0])
                        if result is False:
                            window.error_buyed()
                            window.view_character()
                        else:
                            window.view_window()
                            window.view_character()

    pygame.quit()


if __name__ == '__main__':
    main()
