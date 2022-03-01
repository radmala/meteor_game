import random
import sys

import pygame
from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # кнопка выхода
                    terminate()
                return


def playerHasHitRock(playerRect, rock):
    for b in rock:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
FPS = 60
ROCKMINSIZE = 10
ROCKMAXSIZE = 40
ROCKMINSPEED = 1
ROCKMAXSPEED = 8
ADDNEWROCKRATE = 6
PLAYERMOVERATE = 5


# Начинаем игру
pygame.init()
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Метеор')
pygame.mouse.set_visible(False)


# Добовляем шрифт
font = pygame.font.SysFont(None, 48)


# Добовляем музыку
gameOverSound = pygame.mixer.Sound('Sound/zvuki-quotkonets-igryiquot-game-over-sounds-30249.ogg')
pygame.mixer.music.load('Sound/Mathias Rehfeldt Dark Matter Projekt - Ice Field.mp4')


# Добовляем картинки
playerImage = pygame.image.load('Image/character.png')
playerRect = playerImage.get_rect()
rockImage = pygame.image.load('Image/rock.png')
backgroudImage = pygame.image.load("Image/background.jpg").convert()
backgroudImage = pygame.transform.smoothscale(backgroudImage, screen.get_size())


# покащываем стартовый экран
Start_backgroudImage = pygame.image.load("Image/start_background.png").convert()
Start_backgroudImage = pygame.transform.smoothscale(Start_backgroudImage, screen.get_size())
drawText('Метеор', font, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Нажмите для начала', font, screen, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # начинаем иг   ру
    rock = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    rockAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # пока игра продолжается
        score += 1  # изменяем значение набранных очков

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Можно управлять курсором мышки
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # добовляем новые метеоры
        if not reverseCheat and not slowCheat:
            rockAddCounter += 1
        if rockAddCounter == ADDNEWROCKRATE:
            rockAddCounter = 0
            rockSize = random.randint(ROCKMINSIZE, ROCKMAXSIZE)
            newrock = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - rockSize), 0 - rockSize, rockSize,
                                             rockSize),
                         'speed': random.randint(ROCKMINSPEED, ROCKMAXSPEED),
                         'surface': pygame.transform.scale(rockImage, (rockSize, rockSize)),
                         }

            rock.append(newrock)

        # движение игорока
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # подключаем мышь
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Движение метеоров учитывая читы
        for b in rock:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # удаляем метеоры
        for b in rock[:]:
            if b['rect'].top > WINDOWHEIGHT:
                rock.remove(b)

        # картинка на фон
        screen.blit(backgroudImage, (0, 0))

        # пишем значение очков
        drawText('Score: %s' % (score), font, screen, 10, 0)
        drawText('Top Score: %s' % (topScore), font, screen, 10, 40)

        # Рисуем игорока
        screen.blit(playerImage, playerRect)

        # Рисуем метеоры
        for b in rock:
            screen.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Проверяем столкнулся ли игрок с камнем
        if playerHasHitRock(playerRect, rock):
            if score > topScore:
                topScore = score  # выставляем новое значение
            break
        mainClock.tick(FPS)

    # Останавливаем игру и выводим экран проигрыша
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, screen, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
