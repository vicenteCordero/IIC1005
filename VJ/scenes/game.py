'''
Hola este es modulo game,
este modulo manejara la escena donde ocurre nuestro juego
'''

import pygame

from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT, K_f, K_m, K_d)

from elements.jorge import Player

from elements.entities import Enemy, Coin

from elements.parametros import ENEMY_RATE_MS, ENEM_VELOC_RANGE, USER_SPEED

from elements.parametros import font_name

import csv

import os

def cargar_puntajes():
    with open('elements/records.csv', 'r') as file:

        puntajes = dict()
        rec_reader = csv.DictReader(file)

        for fila in rec_reader:
            puntajes[fila['dificultad']] = {'pasada': fila['pasada'], 'record': fila['record']}

    return puntajes


def StartScene(dificultad):
    pygame.init()

    SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
    SCREEN_HEIGHT = 750  # revisar alto de la imagen de fondo

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('assets/pixelBackground.jpg').convert()

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
    addcoin = pygame.USEREVENT + 2
    coins = pygame.sprite.Group()
    pygame.time.set_timer(addcoin, 6000)
    time_coin = -1
    active_coin = -10
    
    running = True

    while running:

        screen.blit(background_image, [0, 0])

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        if pygame.sprite.spritecollideany(player, enemies):
            
            player.kill()
            
            update_scores(time_count, dificultad)
            menu()
            running = False

        if pygame.sprite.spritecollideany(player, coins):

            active_coin = time_count
            for entity in coins:
                entity.kill()

        if active_coin + 2 > time_count:
            for entity in enemies:
                entity.kill()
        
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    running = False

            elif event.type == ADDENEMY:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, ENEM_VELOC_RANGE[dificultad])
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == QUIT:
                running = False

            elif event.type == conteo:
                time_count += 1

            elif event.type == addcoin and not len(coins):
                new_coin = Coin(SCREEN_WIDTH, SCREEN_HEIGHT)
                all_sprites.add(new_coin)
                coins.add(new_coin)
                time_coin = time_count

            elif len(coins) and time_coin + 4 < time_count:
                for ent in coins:
                    ent.kill()
        
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
    
    ''' iniciamos los modulos de pygame'''
    pygame.init()

    ''' Creamos y editamos la ventana de pygame (escena) '''
    '''definir el tamaño de la ventana'''
    SCREEN_WIDTH = 1000  # revisar ancho de la imagen de fondo
    SCREEN_HEIGHT = 750  # revisar alto de la imagen de fondo

    '''crear el objeto pantalla'''
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load('assets/menu_background.png').convert()

    puntajes = cargar_puntajes()

    ''' Preparamos el gameloop '''
    '''creamos el reloj del juego'''
    clock = pygame.time.Clock()

    big_font = pygame.font.Font(font_name, 50)
    big_font.bold = True

    medium_font = pygame.font.Font(font_name, 30)
    medium_font.bold = True

    small_font = pygame.font.Font(font_name, 15)
    small_font.bold = True
    
    # título
    menu_text = big_font.render('- JORGE  VS.  BUGS -', True, (255, 255, 255))
    menu_rect = menu_text.get_rect()
    menu_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 300)

    # dificultades:
    press_text = medium_font.render('Presiona:', True, (255, 255, 255))
    press_rect = press_text.get_rect()
    press_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)

    objs = list()
    for i, dif in enumerate(('Facil', 'Medio', 'Dificil')):
        
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

                if event.key == K_f:
                    StartScene("Facil")
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

