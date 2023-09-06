import pygame

from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT, K_p, K_m, K_d)

from elements.jorge import Player

from elements.entities import Enemy, Heart

from elements.parametros import (ENEMY_RATE_MS, ENEM_VELOC_RANGE, USER_SPEED,
                                font_name,menu_song, game_song)

import csv

import os

import time


pygame.init()

big_font = pygame.font.Font(font_name, 50)
big_font.bold = True

medium_font = pygame.font.Font(font_name, 30)
medium_font.bold = True

small_font = pygame.font.Font(font_name, 15)
small_font.bold = True


def cargar_puntajes():
    with open('elements/records.csv', 'r') as file:

        puntajes = dict()
        rec_reader = csv.DictReader(file)

        for fila in rec_reader:
            puntajes[fila['dificultad']] = {'pasada': fila['pasada'], 'record': fila['record']}

    return puntajes


def StartScene(dificultad):
    # config music y playlist
    pygame.mixer.music.load(game_song)
    pygame.mixer.music.play(-1)

    SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
    SCREEN_HEIGHT = 750  # revisar alto de la imagen de fondo

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('assets/pixelBackground.jpg').convert()

    # set enemies speed
    enemy_speed_range = ENEM_VELOC_RANGE[dificultad]
    
    # add music
    pygame.mixer.music.unpause()
    
    # creamos el reloj del juego
    clock = pygame.time.Clock()
    # contador de tiempo
    time_count = 0
    conteo = pygame.USEREVENT + 1
    pygame.time.set_timer(conteo, 1000)

    # generador de enemigos
    ADDENEMY = pygame.USEREVENT + 0
    pygame.time.set_timer(ADDENEMY, ENEMY_RATE_MS[dificultad])

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, USER_SPEED[dificultad])

    # contenedores de enemigos y jugador
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # generador monedas
    addheart = pygame.USEREVENT + 2
    hearts = pygame.sprite.Group()
    pygame.time.set_timer(addheart, 6000)

    # texto
    vidas_text = medium_font.render(f'Vidas {player.vidas}', True, (255, 255, 255), (0, 0, 0))
    vidas_rect = vidas_text.get_rect()
    vidas_rect.center = (100, SCREEN_HEIGHT - 50)

    timer_text = medium_font.render(f'{time_count}s', True, (255, 255, 255), (0, 0, 0))
    timer_rect = timer_text.get_rect()
    timer_rect.center = (100, SCREEN_HEIGHT - 100)
    
    running = True

    while running:
        
        if time_count == 15 and dificultad == 'Progresivo':
            ADDENEMY = pygame.USEREVENT + 3
            pygame.time.set_timer(ADDENEMY, ENEMY_RATE_MS['Medio'])
            player.speed = USER_SPEED['Medio']
            enemy_speed_range = ENEM_VELOC_RANGE['Medio']

        if time_count == 30 and dificultad == 'Progresivo':
            ADDENEMY = pygame.USEREVENT + 4
            pygame.time.set_timer(ADDENEMY, ENEMY_RATE_MS['Dificil'])
            player.speed = USER_SPEED['Dificil']
            enemy_speed_range = ENEM_VELOC_RANGE['Dificil']
        
        screen.blit(background_image, [0, 0])
        screen.blit(vidas_text, vidas_rect)
        screen.blit(timer_text, timer_rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        
        if pygame.sprite.spritecollideany(player, enemies):
            # aún le quedan vidas
            if player.die():
                vidas_text = medium_font.render(f'Vidas {player.vidas}', True, (255, 255, 255), (0, 0, 0))
                for enem in enemies:
                    enem.kill()
                for heart in hearts:
                    heart.kill()
            # muere definitivo :(
            else:
                player.kill()
                pygame.mixer.music.play(-1)
                update_scores(time_count, dificultad)
                menu()
                running = False

        if pygame.sprite.spritecollideany(player, hearts):

            player.vidas += 1
            vidas_text = medium_font.render(f'Vidas {player.vidas}', True, (255, 255, 255), (0, 0, 0))

            for entity in hearts:
                entity.kill()
        
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, enemy_speed_range)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == QUIT:
                running = False

            elif event.type == conteo:
                time_count += 1
                timer_text = medium_font.render(f'{time_count}s', True, (255, 255, 255), (0, 0, 0))

            # añade un corazon solo si no hay otros
            elif event.type == addheart and not len(hearts):
                new_heart = Heart(SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(new_heart)
                hearts.add(new_heart)
        
        pygame.display.flip()

        # FPS
        clock.tick(60)


def update_scores(actual_score, dificultad):
    with open('elements/records.csv', 'r') as f_in, open('elements/tmp.csv', 'w') as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=['dificultad', 'pasada', 'record'])

        writer.writeheader()

        for row in reader:
            # la fila que debo modificar
            if row['dificultad'] == dificultad:
                new_dict = dict()
                new_dict['dificultad'] = dificultad
                new_dict['pasada'] = actual_score

                if int(row['record']) < actual_score:
                    new_dict['record'] = actual_score

                else:
                    new_dict['record'] = row['record']

                writer.writerow(new_dict)

            else:
                writer.writerow(row)

    os.rename('elements/tmp.csv', 'elements/records.csv')


def menu():
    pygame.mixer.music.load(menu_song)
    pygame.mixer.music.play(-1)
    
    pygame.init()

    SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
    SCREEN_HEIGHT = 750  # revisar alto de la imagen de fondo

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('assets/menu_background.png').convert()

    puntajes = cargar_puntajes()

    clock = pygame.time.Clock()
    
    # título
    menu_text = big_font.render('- JORGE  VS.  BUGS -', True, (255, 255, 255))
    menu_rect = menu_text.get_rect()
    menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300)

    # dificultades:
    press_text = medium_font.render('Presiona:', True, (255, 255, 255))
    press_rect = press_text.get_rect()
    press_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)

    objs = list()
    for i, dif in enumerate(('Progresivo', 'Medio', 'Dificil')):
        
        for j, color in enumerate(((153, 255, 102), (200, 200, 200), (0, 255, 255))):
            
            if j == 0:
                text = medium_font.render(f"'{dif[0]}' - Modo {dif}.", True, color)

            elif j == 1:
                text = medium_font.render(f"Última partida: {puntajes[dif]['pasada']}s", True, color)

            elif j == 2:
                text = medium_font.render(f"Record: {puntajes[dif]['record']}s", True, color)

            rect = text.get_rect()
            rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 160 + j * 40 - 150)

            objs.append((text, rect))
    
    running = True

    while running:

        screen.blit(background_image, [0, 0])
        screen.blit(menu_text, menu_rect)
        
        screen.blit(press_text, press_rect)
        
        for obj in objs:
            screen.blit(*obj)

        for event in pygame.event.get():
            
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_p:
                    StartScene("Progresivo")
                    running = False

                if event.key == K_m:
                    StartScene("Medio")
                    running = False

                if event.key == K_d:
                    StartScene("Dificil")
                    running = False
            
            elif event.type == QUIT:
                running = False
        
        pygame.display.flip()

        # FPS
        clock.tick(60)