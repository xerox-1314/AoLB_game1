import pygame
from main_window import MainWindow, Button
import database_work as db
from pygame.locals import *
import levels_window
import sys
import os


SIZE = width, height = (600, 360)
FPS = 30
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
global_namefile = ''
game_over = False
win = False


def load_image(name, directory=None, colorkey=None):
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


def level_generation(namefile):
    global global_namefile
    global platform_sprites
    global money_sprites
    global angry_sprites
    global bullet_sprites
    global spike_sprites
    platform_sprites = pygame.sprite.Group()
    money_sprites = pygame.sprite.Group()
    angry_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    spike_sprites = pygame.sprite.Group()
    global_namefile = namefile
    platform_dict = dict()
    angry_dict = dict()
    money_dict = dict()
    spike_dict = dict()
    win = 10
    all_namefile = os.path.join('data', 'levels', namefile)
    with open(all_namefile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].split(' ')
            if line[0] == 'Platform':
                platform_dict[int(line[1])] = Platform(width + 5, int(line[2]), platform_sprites, num_money=int(line[3]), spike=int(line[4]), angry=bool(line[5]))
            elif line[0] == 'Spike':
                spike_dict[int(line[1])] = Spike(width + 5, height - ground_height - 40, spike_sprites)
            elif line[0] == 'Money':
                money_dict[int(line[1])] = Money(width + 5, height - ground_height - 40, money_sprites)
            elif line[0] == 'Angry':
                angry_dict[int(line[1])] = Angry(width + 5, height - ground_height - 60, angry_sprites)
            elif line[0] == 'Win':
                win = int(line[1])
    pygame.init()
    main(platform_dict, spike_dict, money_dict, angry_dict, win)


class Hero(pygame.sprite.Sprite):
    hero_image = load_image(db.get_character_now()[5], directory='characters', colorkey=-1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Hero.hero_image, (hero_width, hero_height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, height - ground_height - hero_height + 5
        self.on_platform = False
        self.stop_x_left = -1
        self.stop_x_right = -1
        self.mask = pygame.mask.from_surface(self.image)

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


class Spike(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('chart.png'), (40, 40))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Spike.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x -= 7


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.flip(load_image('bullet.png', colorkey=-1), True, False)

    def __init__(self, x_start, y_start, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(Bullet.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x_start
        self.rect.y = y_start
        self.mask = pygame.mask.from_surface(self.image)


class Money(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('money.png', colorkey=-1), (20, 20))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Money.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x -= 7


class Angry(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('angry_1.png', colorkey=-1), (80, 50))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = self.image = Angry.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_bullet = False

    def move(self):
        self.rect.x -= 7
        if self.is_bullet is False and self.rect.x <= width:
            print('is bullet true')
            self.is_bullet = True
            self.bullet = Bullet(self.rect.x, self.rect.y, bullet_sprites)

    def move_bullet(self):
        self.bullet.rect.x -= 7

    def bullet_reset(self):
        self.bullet.rect.x = self.rect.x


class Platform(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('platform.png', colorkey=-1), (250, 40))

    def __init__(self, x, y, *group, spike=0, num_money=0, angry=False):
        super().__init__(*group)
        self.image = self.image = Platform.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.money_list = list()
        self.spike_list = list()
        count = 0

        if num_money != 0 and num_money <= 3:
            for i in range(num_money):
                count += 1
                self.money_list.append(Money(x + 10, self.rect.y - 30, money_sprites))
                x += 40
        x += 50
        if spike != 0 and count <= 5:
            for i in range(spike):
                count += 1
                self.spike_list.append(Spike(x + 10, self.rect.y - 40, spike_sprites))

        if angry is True:
            self.is_angry = True
            self.angry = Angry(x, self.rect.y - 50, angry_sprites)
        else:
            self.is_angry = False

    def move(self):
        self.rect.x -= 7
        for money in self.money_list:
            money.rect.x -= 7
        for spike in self.spike_list:
            spike.rect.x -= 7
        if self.is_angry is True:
            self.angry.move()


def main(platform_dict, spike_dict, money_dict, angry_dict, win_count):
    pygame.init()
    global win
    global game_over
    global global_namefile

    sound.play()
    game_count = 0
    color_count = 0
    game_over_color = 'red'
    filename = os.path.join('data', 'game_font.ttf')
    font = pygame.font.Font(filename, 55)
    game_over_text = font.render('GAME OVER', True, 'white')
    win_text = font.render('YOU WIN', True, 'white')

    background_x = 0
    window.screen.fill((255, 255, 255))
    pygame.display.set_caption('Level')
    static_sprites = pygame.sprite.Group()
    background_image = window.load_image('background.png')
    pygame.display.flip()

    spike_list = list()
    platform_list = list()
    money_list = list()
    angry_list = list()

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
            reset_but = Button('Заново', 20, (255, 255, 255), (172, 64, 235))
            exit_but = Button('Выход', 20, (255, 255, 255), (172, 64, 235))
            reset_but.show_button(window.screen, width // 2 - reset_but.width // 2, 200)
            exit_but.show_button(window.screen, width // 2 - exit_but.width // 2, 280)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if reset_but.check_click(*event.pos):
                            game_over = False
                            run = False
                            print(global_namefile)
                            level_generation(global_namefile)
                        elif exit_but.check_click(*event.pos):
                            SIZE = (500, 400)
                            pygame.display.set_mode(SIZE)
                            levels_window.main()
        elif win is True:
            color_count += 1
            if color_count == 10:
                color_count = 0
                game_over_color = 'blue' if game_over_color == 'red' else 'red'
            pygame.draw.rect(window.screen, game_over_color, (0, 0, width, height))
            window.screen.blit(win_text, (width // 2 - game_over_text.get_width() // 2, 50))
            exit_but = Button('Выход', 20, (255, 255, 255), (172, 64, 235))
            exit_but.show_button(window.screen, width // 2 - exit_but.width // 2, 280)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if exit_but.check_click(*event.pos):
                            SIZE = (500, 400)
                            pygame.display.set_mode(SIZE)
                            levels_window.main()
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
                for money in money_list:
                    money.move()
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
                    if value.is_angry is True:
                        angry_list.append(value.angry)

            for item, value in spike_dict.items():
                if item == game_count:
                    spike_list.append(value)

            for item, value in money_dict.items():
                if item == game_count:
                    money_list.append(value)

            for item, value in angry_dict.items():
                if item == game_count:
                    angry_list.append(value)

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
            angry_sprites.draw(window.screen)
        pygame.display.flip()
        time.tick(FPS)
    pygame.quit()