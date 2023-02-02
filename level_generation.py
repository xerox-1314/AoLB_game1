import pygame
from main_window import MainWindow
import database_work as db
from pygame.locals import *
from level_base import Hero, Platform, Angry, Bullet, Spike
import os


def main(platform_dict, spike_dict, money_dict, angry_dict, win_count):
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
    game_over = False
    win = False

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
            door_sprites.draw(window.screen)
            angry_sprites.draw(window.screen)
        pygame.display.flip()
        time.tick(30)
    pygame.quit()