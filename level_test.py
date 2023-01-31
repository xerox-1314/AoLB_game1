import pygame
from main_window import MainWindow
import database_work as db
from pygame.locals import *

SIZE = width, height = (600, 360)
ground_height = 100
hero_width, hero_height = 60, 90
player_speed = 8

window = MainWindow(*SIZE)
sound = pygame.mixer.Sound('data/sounds/level1.mp3')
sound_gameover = pygame.mixer.Sound('data/sounds/game_over.mp3')
sound_win = pygame.mixer.Sound('data/sounds/win.mp3')
platform_sprites = pygame.sprite.Group()
money_sprites = pygame.sprite.Group()
angry_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
spike_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
angry_list = list()
win_count = 350
game_over = False
win = False


class Hero(pygame.sprite.Sprite):
    hero_image = window.load_image(db.get_character_now()[5], directory='characters', colorkey=-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Hero.hero_image, (hero_width, hero_height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, height - ground_height - hero_height + 5
        self.on_platform = False
        self.stop_x_left = -1
        self.stop_x_right = -1

    def update_x(self, value):
        global game_over
        if pygame.sprite.spritecollideany(self, platform_sprites) and self.on_platform is True:
            if not (self.rect.x <= 5 and value < 0) and not (self.rect.x >= width // 2 and value > 0):
                self.rect.x += value
        elif pygame.sprite.spritecollideany(self, platform_sprites) and self.on_platform is False:
            sprite = pygame.sprite.spritecollideany(self, platform_sprites)
            if self.rect.x < sprite.rect.x:
                self.rect.x = sprite.rect.x - self.rect.width
            else:
                self.rect.x = sprite.rect.x + sprite.rect.width
        else:
            if not (self.rect.x <= 5 and value < 0) and not (self.rect.x >= width // 2 and value > 0):
                self.rect.x += value
        if not pygame.sprite.spritecollideany(self, platform_sprites):
            self.on_platform = False
        if pygame.sprite.spritecollideany(self, money_sprites):
            pygame.sprite.spritecollideany(self, money_sprites).kill()
            db.add_money()

    def update_y(self, value):
        global game_over
        self.rect.y += value
        if pygame.sprite.spritecollideany(self, platform_sprites):
            sprite = pygame.sprite.spritecollideany(self, platform_sprites)
            if self.rect.y - value <= sprite.rect.y:
                self.on_platform = True
                self.rect.y = sprite.rect.y - self.rect.height + 10
        else:
            self.on_platform = False

    def check_landing(self):
        if self.on_platform is False and self.rect.y < height - ground_height - hero_height + 5:
            self.rect.y -= 5

    def check_collide(self):
        global game_over
        if pygame.sprite.spritecollideany(self, bullet_sprites):
            sound.stop()
            sound_gameover.play()
            game_over = True
        if pygame.sprite.spritecollideany(self, spike_sprites):
            sound.stop()
            sound_gameover.play()
            game_over = True


class Door(pygame.sprite.Sprite):
    image = pygame.transform.scale(window.load_image('door.png'), (80, 80))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Door.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x -= 7


class Spike(pygame.sprite.Sprite):
    image = pygame.transform.scale(window.load_image('chart.png'), (40, 40))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Spike.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x -= 7


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.flip(window.load_image('bullet.png', colorkey=-1), True, False)

    def __init__(self, x_start, y_start, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Bullet.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x_start
        self.rect.y = y_start

class Money(pygame.sprite.Sprite):
    image = pygame.transform.scale(window.load_image('money.png', colorkey=-1), (20, 20))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Money.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Angry(pygame.sprite.Sprite):
    image = pygame.transform.scale(window.load_image('angry_1.png', colorkey=-1), (80, 50))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.image = Angry.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_bullet = False
        angry_list.append(self)

    def move(self):
        self.rect.x -= 7
        if self.is_bullet is False and self.rect.x <= width:
            self.is_bullet = True
            self.bullet = Bullet(self.rect.x, self.rect.y, bullet_sprites)

    def move_bullet(self):
        self.bullet.rect.x -= 7

    def bullet_reset(self):
        self.bullet.rect.x = self.rect.x

class Platform(pygame.sprite.Sprite):
    image = pygame.transform.scale(window.load_image('platform.png', colorkey=-1), (250, 40))

    def __init__(self, x, y, *group, spike=0, door=False, num_money=0, angry=False):
        super().__init__(*group)
        self.image = self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.money_list = list()

        if num_money != 0 and num_money <= 3:
            for i in range(num_money):
                self.money_list.append(Money(x + 10, self.rect.y - 30, money_sprites))
                x += 40
        x += 50

        if angry is True:
            self.is_angry = True
            self.angry = Angry(x, self.rect.y - 50, angry_sprites)
        else:
            self.is_angry = False

        if door is True and angry is False:
            self.is_door = True
            self.door = Door(x, self.rect.y - 80, door_sprites)
        else:
            self.is_door = False

    def move(self):
        self.rect.x -= 7
        for money in self.money_list:
            money.rect.x -= 7
        if self.is_angry is True:
            self.angry.move()
        if self.is_door is True:
            self.door.move()

def main():
    sound.play()
    game_count = 0
    color_count = 0
    game_over_color = 'red'
    global game_over
    global win
    global win_count
    font = pygame.font.Font('D:/Program Files/pycharmprograms/AoLB_game1/data/game_font.ttf', 55)
    game_over_text = font.render('GAME OVER', True, 'white')
    win_text = font.render('YOU WIN', True, 'white')

    background_x = 0
    window.screen.fill((255, 255, 255))
    pygame.display.set_caption('Level')
    static_sprites = pygame.sprite.Group()
    background_image = window.load_image('background.png')
    pygame.display.flip()

    platform_dict = {100: Platform(width + 5, 150, platform_sprites, num_money=2, angry=False), 200: Platform(width + 5, 180, platform_sprites, num_money=1, angry=False),
                     300: Platform(width + 5, 130, platform_sprites, num_money=3, angry=False), 400: Platform(width + 5, 160, platform_sprites, num_money=0, angry=False, door=True)}
    spike_dict = {150: Spike(width + 5, height - ground_height - 40, spike_sprites), 250: Spike(width + 5, height - ground_height - 40, spike_sprites),
                     350: Spike(width + 5, height - ground_height - 40, spike_sprites), 450: Spike(width + 5, height - ground_height - 40, spike_sprites)}

    spike_list = list()
    platform_list = list()
    hero_sprites = pygame.sprite.Group()
    hero = Hero(hero_sprites)
    hero_sprites.draw(window.screen)
    pygame.display.flip()

    run = True
    is_jump = False
    jump_level = 9
    time = pygame.time.Clock()

    while run:
        if game_over is True:
            color_count += 1
            if color_count == 10:
                color_count = 0
                game_over_color = 'blue' if game_over_color == 'red' else 'red'
            pygame.draw.rect(window.screen, game_over_color, (0, 0, width, height))
            window.screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        elif win is True:
            color_count += 1
            if color_count == 10:
                color_count = 0
                game_over_color = 'blue' if game_over_color == 'red' else 'red'
            pygame.draw.rect(window.screen, game_over_color, (0, 0, width, height))
            window.screen.blit(win_text, (width // 2 - game_over_text.get_width() // 2, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        else:
            hero.check_collide()
            if pygame.key.get_pressed()[K_LEFT]:
                hero.update_x(-player_speed)
            if pygame.key.get_pressed()[K_RIGHT]:
                game_count += 1
                hero.update_x(player_speed)
                background_x -= 7
                for platform in platform_list:
                    platform.move()
                for spike in spike_list:
                    spike.move()
            elif pygame.key.get_pressed()[K_a]:
                hero.update_x(-player_speed)
            elif pygame.key.get_pressed()[K_d]:
                hero.update_x(player_speed)
                background_x -= 7

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not is_jump:
                            is_jump = True
            if is_jump:
                if jump_level >= -9:
                    if jump_level > 0:
                        hero.update_y(-((jump_level ** 2) // 2))
                    else:
                        hero.update_y((jump_level ** 2) // 2)
                    jump_level -= 1
                else:
                    is_jump = False
                    jump_level = 9

            if is_jump is False and hero.on_platform is False:
                hero.rect.y = height - ground_height - hero_height + 5

            if background_x <= -width:
                background_x = 0

            if is_jump is False:
                hero.check_landing()

            for item, value in platform_dict.items():
                if item == game_count:
                    platform_list.append(value)

            for item, value in spike_dict.items():
                if item == game_count:
                    spike_list.append(value)

            for angry in angry_list:
                if angry.is_bullet is True:
                    if angry.bullet.rect.x >= 0:
                        angry.move_bullet()
                    else:
                        angry.bullet_reset()

            if game_count == win_count:
                sound.stop()
                sound_win.play()
                win = True

            window.screen.blit(background_image, (background_x, 0))
            window.screen.blit(background_image, (background_x + width, 0))
            static_sprites.draw(window.screen)
            bullet_sprites.draw(window.screen)
            hero_sprites.draw(window.screen)
            spike_sprites.draw(window.screen)
            platform_sprites.draw(window.screen)
            money_sprites.draw(window.screen)
            door_sprites.draw(window.screen)
            angry_sprites.draw(window.screen)
        pygame.display.flip()
        time.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()