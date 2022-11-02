import pygame
from parameter import *
from classes import *

pygame.init()

if pygame.joystick.get_count() > 0:
    if JS_DEVNUM < pygame.joystick.get_count():
        js = pygame.joystick.Joystick(JS_DEVNUM)
    else:
        js = pygame.joystick.Joystick(0)
    js.init()
else:
    js = None


def get_image_surface(file_path):
    image = pygame.image.load(file_path).convert()
    # image_rect = image.get_rect()
    # image_surface = pygame.Surface((image_rect.width, image_rect.height))
    # image_surface.blit(image, image_rect)
    return image


def CheckIfCloseButton(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)


def CheckInputs():
    if thisGame.mode == 1 or thisGame.mode == 8 or thisGame.mode == 9:
        if pygame.key.get_pressed()[pygame.K_RIGHT] or (js is not None and js.get_axis(JS_XAXIS) > 0.5):
            if not (player.velX == player.speed and player.velY == 0) and not thisLevel.CheckIfHitWall(
                    (player.x + player.speed, player.y), (player.nearestRow, player.nearestCol)):
                player.velX = player.speed
                player.velY = 0

        elif pygame.key.get_pressed()[pygame.K_LEFT] or (js is not None and js.get_axis(JS_XAXIS) < -0.5):
            if not (player.velX == -player.speed and player.velY == 0) and not thisLevel.CheckIfHitWall(
                    (player.x - player.speed, player.y), (player.nearestRow, player.nearestCol)):
                player.velX = -player.speed
                player.velY = 0

        elif pygame.key.get_pressed()[pygame.K_DOWN] or (js is not None and js.get_axis(JS_YAXIS) > 0.5):
            if not (player.velX == 0 and player.velY == player.speed) and not thisLevel.CheckIfHitWall(
                    (player.x, player.y + player.speed), (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = player.speed

        elif pygame.key.get_pressed()[pygame.K_UP] or (js is not None and js.get_axis(JS_YAXIS) < -0.5):
            if not (player.velX == 0 and player.velY == -player.speed) and not thisLevel.CheckIfHitWall(
                    (player.x, player.y - player.speed), (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = -player.speed

    if pygame.key.get_pressed()[pygame.K_ESCAPE] or (js is not None and js.get_button(7)) :
        sys.exit(0)

    elif thisGame.mode == 3:
        if pygame.key.get_pressed()[pygame.K_RETURN] or (js is not None and js.get_button(JS_STARTBUTTON)):
            thisGame.StartNewGame()


def GetCrossRef():
    f = open(os.path.join(SCRIPT_PATH, "res", "crossref.txt"), 'r')

    lineNum = 0

    for i in f.readlines():
        # print " ========= Line " + str(lineNum) + " ============ "
        while len(i) > 0 and (i[-1] == '\n' or i[-1] == '\r'): i = i[:-1]
        while len(i) > 0 and (i[0] == '\n' or i[0] == '\r'): i = i[1:]
        str_splitBySpace = i.split(' ')

        j = str_splitBySpace[0]

        if j == "'" or j == "" or j == "#":
            # comment / whitespace line
            # print " ignoring comment line.. "
            useLine = False
        else:
            # print str(wordNum) + ". " + j
            useLine = True

        if useLine:
            tileIDName[int(str_splitBySpace[0])] = str_splitBySpace[1]
            tileID[str_splitBySpace[1]] = int(str_splitBySpace[0])

            thisID = int(str_splitBySpace[0])
            if not thisID in NO_GIF_TILES:
                tileIDImage[thisID] = get_image_surface(
                    os.path.join(SCRIPT_PATH, "res", "tiles", str_splitBySpace[1] + ".gif"))
            else:
                tileIDImage[thisID] = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))

            # change colors in tileIDImage to match maze colors
            for y in range(0, TILE_WIDTH, 1):
                for x in range(0, TILE_HEIGHT, 1):

                    if tileIDImage[thisID].get_at((x, y)) == IMG_EDGE_LIGHT_COLOR:
                        # wall edge
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeLightColor)

                    elif tileIDImage[thisID].get_at((x, y)) == IMG_FILL_COLOR:
                        # wall fill
                        tileIDImage[thisID].set_at((x, y), thisLevel.fillColor)

                    elif tileIDImage[thisID].get_at((x, y)) == IMG_EDGE_SHADOW_COLOR:
                        # pellet color
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeShadowColor)

                    elif tileIDImage[thisID].get_at((x, y)) == IMG_PELLET_COLOR:
                        # pellet color
                        tileIDImage[thisID].set_at((x, y), thisLevel.pelletColor)

        lineNum += 1
    f.close()
