class level:
    def __init__(self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.map = {}

        self.pellets = 0
        self.powerPelletBlinkTimer = 0

    def SetMapTile(self, row_col, newValue):
        (row, col) = row_col
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row_col):
        (row, col) = row_col
        if 0 <= row < self.lvlHeight and 0 <= col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0

    @staticmethod
    def IsWall(row_col):
        (row, col) = row_col
        if row > thisLevel.lvlHeight - 1 or row < 0:
            return True

        if col > thisLevel.lvlWidth - 1 or col < 0:
            return True

        # check the offending tile ID
        result = thisLevel.GetMapTile((row, col))

        # if the tile was a wall
        if 100 <= result <= 199:
            return True
        else:
            return False

    def CheckIfHitWall(self, possiblePlayerX_possiblePlayerY, row_col):
        (possiblePlayerX, possiblePlayerY) = possiblePlayerX_possiblePlayerY
        (row, col) = row_col
        numCollisions = 0

        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (possiblePlayerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        possiblePlayerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):

                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1

        if numCollisions > 0:
            return True
        else:
            return False

    @staticmethod
    def CheckIfHit(playerX_playerY, x_y, cushion):
        (playerX, playerY) = playerX_playerY
        (x, y) = x_y
        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (
                playerY - y > -cushion):
            return True
        else:
            return False

    @staticmethod
    def CheckIfHitSomething(playerX_playerY, row_col):
        (playerX, playerY) = playerX_playerY
        (row, col) = row_col
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (playerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        playerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        playerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        playerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):
                    # check the offending tile ID
                    result = thisLevel.GetMapTile((iRow, iCol))

                    if result == tileID['pellet']:
                        # got a pellet
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        snd_pellet[player.pelletSndNum].play()
                        player.pelletSndNum = 1 - player.pelletSndNum

                        thisLevel.pellets -= 1

                        thisGame.AddToScore(10)

                        if thisLevel.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            thisGame.SetMode(6)


                    elif result == tileID['pellet-power']:
                        # got a power pellet
                        thisGame.SetMode(9)
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        snd_powerpellet.play()

                        thisGame.AddToScore(100)
                        thisGame.ghostValue = 200

                        thisGame.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if ghosts[i].state == 1:
                                ghosts[i].state = 2

                                """
                                # Must line up with grid before invoking a new path (for now)
                                ghosts[i].x = ghosts[i].nearestCol * TILE_HEIGHT
                                ghosts[i].y = ghosts[i].nearestRow * TILE_WIDTH								

                                # give each ghost a path to a random spot (containing a pellet)
                                (randRow, randCol) = (0, 0)

                                while not self.GetMapTile((randRow, randCol)) == tileID[ 'pellet' ] or (randRow, randCol) == (0, 0):
                                    randRow = random.randint(1, self.lvlHeight - 2)
                                    randCol = random.randint(1, self.lvlWidth - 2)
                                ghosts[i].currentPath = path.FindPath( (ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol) )

                                ghosts[i].FollowNextPathWay()
                                """

                    elif result == tileID['door-h']:
                        # ran into a horizontal door
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile((iRow, i)) == tileID['door-h']:
                                    player.x = i * TILE_WIDTH

                                    if player.velX > 0:
                                        player.x += TILE_WIDTH
                                    else:
                                        player.x -= TILE_WIDTH

                    elif result == tileID['door-v']:
                        # ran into a vertical door
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile((i, iCol)) == tileID['door-v']:
                                    player.y = i * TILE_HEIGHT

                                    if player.velY > 0:
                                        player.y += TILE_HEIGHT
                                    else:
                                        player.y -= TILE_HEIGHT

                    elif result == tileID['heart']:
                        thisGame.SetMode(11)

    def GetGhostBoxPos(self):
        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['ghost-door']:
                    return row, col

        return False

    def GetPathwayPairPos(self):
        doorArray = []

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['door-h']:
                    # found a horizontal door
                    doorArray.append((row, col))
                elif self.GetMapTile((row, col)) == tileID['door-v']:
                    # found a vertical door
                    doorArray.append((row, col))

        if len(doorArray) == 0:
            return False

        chosenDoor = random.randint(0, len(doorArray) - 1)

        if self.GetMapTile(doorArray[chosenDoor]) == tileID['door-h']:
            # horizontal door was chosen
            # look for the opposite one
            for i in range(0, thisLevel.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if thisLevel.GetMapTile((doorArray[chosenDoor][0], i)) == tileID['door-h']:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            # vertical door was chosen
            # look for the opposite one
            for i in range(0, thisLevel.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if thisLevel.GetMapTile((i, doorArray[chosenDoor][1])) == tileID['door-v']:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])

        return False

    def PrintMap(self):
        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
                outputLine += str(self.GetMapTile((row, col))) + ", "

    def DrawMap(self):
        global rect_list
        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 40:
            self.powerPelletBlinkTimer = 0

        for row in range(-1, thisGame.screenTileSize[0] + 1, 1):
            for col in range(-1, thisGame.screenTileSize[1] + 1, 1):

                # row containing tile that actually goes here
                actualRow = thisGame.screenNearestTilePos[0] + row
                actualCol = thisGame.screenNearestTilePos[1] + col

                useTile = self.GetMapTile((actualRow, actualCol))
                if useTile != 0 and useTile != tileID['door-h'] and useTile != tileID['door-v']:
                    # if this isn't a blank tile
                    if useTile == tileID['pellet-power']:
                        if self.powerPelletBlinkTimer < 20:
                            screen.blit(tileIDImage[useTile], (col * TILE_WIDTH - thisGame.screenPixelOffset[0],
                                                               row * TILE_HEIGHT - thisGame.screenPixelOffset[1]))

                    elif useTile == tileID['showlogo']:
                        screen.blit(thisGame.imLogo, (col * TILE_WIDTH - thisGame.screenPixelOffset[0],
                                                      row * TILE_HEIGHT - thisGame.screenPixelOffset[1]))

                    elif useTile == tileID['hiscores']:
                        screen.blit(thisGame.imHiscores, (col * TILE_WIDTH - thisGame.screenPixelOffset[0],
                                                          row * TILE_HEIGHT - thisGame.screenPixelOffset[1]))

                    else:
                        screen.blit(tileIDImage[useTile], (col * TILE_WIDTH - thisGame.screenPixelOffset[0],
                                                           row * TILE_HEIGHT - thisGame.screenPixelOffset[1]))

    def LoadLevel(self, levelNum):
        self.map = {}
        self.pellets = 0

        f = open(os.path.join(SCRIPT_PATH, "res", "levels", str(levelNum) + ".txt"), 'r')
        lineNum = -1
        rowNum = 0
        isReadingLevelData = False

        for line in f:

            lineNum += 1

            # print " ------- Level Line " + str(lineNum) + " -------- "
            while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
            while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"): line = line[1:]
            str_splitBySpace = line.split(' ')

            j = str_splitBySpace[0]

            if j == "'" or j == "":
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
            elif j == "#":
                # special divider / attribute line
                useLine = False

                firstWord = str_splitBySpace[1]

                if firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])

                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])

                elif firstWord == "edgecolor":
                    # edge color keyword for backwards compatibility (single edge color) mazes
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "edgelightcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)

                elif firstWord == "edgeshadowcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "fillcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.fillColor = (red, green, blue, 255)

                elif firstWord == "pelletcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.pelletColor = (red, green, blue, 255)

                elif firstWord == "fruittype":
                    thisFruit.fruitType = int(str_splitBySpace[2])

                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    # print "Level data has begun"
                    rowNum = 0

                elif firstWord == "endleveldata":
                    isReadingLevelData = False
            # print "Level data has ended"

            else:
                useLine = True

            # this is a map data line
            if useLine:

                if isReadingLevelData:

                    # print str( len(str_splitBySpace) ) + " tiles in this column"

                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))

                        thisID = int(str_splitBySpace[k])
                        if thisID == 4:
                            # starting position for pac-man

                            player.homeX = k * TILE_WIDTH
                            player.homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0)

                        elif 10 <= thisID <= 13:
                            # one of the ghosts

                            ghosts[thisID - 10].homeX = k * TILE_WIDTH
                            ghosts[thisID - 10].homeY = rowNum * TILE_HEIGHT
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID == 2:
                            # pellet

                            self.pellets += 1

                    rowNum += 1
        f.close()
        # reload all tiles and set appropriate colors
        GetCrossRef()

        # load map into the pathfinder object
        path.ResizeMap((self.lvlHeight, self.lvlWidth))

        for row in range(0, path.size[0], 1):
            for col in range(0, path.size[1], 1):
                if self.IsWall((row, col)):
                    path.SetType((row, col), 1)
                else:
                    path.SetType((row, col), 0)

        # do all the level-starting stuff
        self.Restart()

    def Restart(self):
        if thisGame.levelNum == 2:
            player.speed = 4

        for i in range(0, 4, 1):
            # move ghosts back to home
            ghosts[i].x = ghosts[i].homeX
            ghosts[i].y = ghosts[i].homeY
            ghosts[i].velX = 0
            ghosts[i].velY = 0
            ghosts[i].state = 1
            ghosts[i].speed = 2
            ghosts[i].Move()

            # give each ghost a path to a random spot (containing a pellet)
            (randRow, randCol) = (0, 0)

            while not self.GetMapTile((randRow, randCol)) == tileID['pellet'] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.lvlHeight - 2)
                randCol = random.randint(1, self.lvlWidth - 2)

            # print "Ghost " + str(i) + " headed towards " + str((randRow, randCol))
            ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol))
            ghosts[i].FollowNextPathWay()

        thisFruit.active = False

        thisGame.fruitTimer = 0

        player.x = player.homeX
        player.y = player.homeY
        player.velX = 0
        player.velY = 0

        player.anim_pacmanCurrent = player.anim_pacmanS
        player.animFrame = 3


class pacman:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 3

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}

        self.animFrame = 1

        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-l " + str(i) + ".gif"))
            self.anim_pacmanR[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-r " + str(i) + ".gif"))
            self.anim_pacmanU[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-u " + str(i) + ".gif"))
            self.anim_pacmanD[i] = get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-d " + str(i) + ".gif"))
            self.anim_pacmanS[i] = get_image_surface(os.path.join(SCRIPT_PATH, "res", "sprite", "pacman.gif"))

        self.pelletSndNum = 0

    def Move(self):
        self.nearestRow = int(((self.y + (TILE_WIDTH / 2)) / TILE_WIDTH))
        self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_HEIGHT))

        # make sure the current velocity will not cause a collision before moving
        if not thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol)):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY

            # check for collisions with other tiles (pellets, etc)
            thisLevel.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol))

            # check for collisions with the ghosts
            for i in range(0, 4, 1):
                if thisLevel.CheckIfHit((self.x, self.y), (ghosts[i].x, ghosts[i].y), TILE_WIDTH / 2):
                    # hit a ghost

                    if ghosts[i].state == 1:
                        # ghost is normal
                        thisGame.SetMode(2)

                    elif ghosts[i].state == 2:
                        # ghost is vulnerable
                        # give them glasses
                        # make them run
                        thisGame.AddToScore(thisGame.ghostValue)
                        thisGame.ghostValue = thisGame.ghostValue * 2
                        snd_eatgh.play()

                        ghosts[i].state = 3
                        ghosts[i].speed = ghosts[i].speed * 4
                        # and send them to the ghost box
                        ghosts[i].x = ghosts[i].nearestCol * TILE_WIDTH
                        ghosts[i].y = ghosts[i].nearestRow * TILE_HEIGHT
                        ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (
                            thisLevel.GetGhostBoxPos()[0] + 1, thisLevel.GetGhostBoxPos()[1]))
                        ghosts[i].FollowNextPathWay()

                        # set game mode to brief pause after eating
                        thisGame.SetMode(5)

            # check for collisions with the fruit
            if thisFruit.active:
                if thisLevel.CheckIfHit((self.x, self.y), (thisFruit.x, thisFruit.y), TILE_WIDTH / 2):
                    thisGame.AddToScore(2500)
                    thisFruit.active = False
                    thisGame.fruitTimer = 0
                    thisGame.fruitScoreTimer = 80
                    snd_eatfruit.play()

        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0

        # deal with power-pellet ghost timer
        if thisGame.ghostTimer > 0:
            thisGame.ghostTimer -= 1

            if thisGame.ghostTimer == 0:
                thisGame.PlayBackgoundSound(snd_default)
                for i in range(0, 4, 1):
                    if ghosts[i].state == 2:
                        ghosts[i].state = 1
                thisGame.ghostValue = 0

        # deal with fruit timer
        thisGame.fruitTimer += 1
        if thisGame.fruitTimer == 380:
            pathwayPair = thisLevel.GetPathwayPairPos()

            if not pathwayPair == False:
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]

                thisFruit.active = True

                thisFruit.nearestRow = pathwayEntrance[0]
                thisFruit.nearestCol = pathwayEntrance[1]

                thisFruit.x = thisFruit.nearestCol * TILE_WIDTH
                thisFruit.y = thisFruit.nearestRow * TILE_HEIGHT

                thisFruit.currentPath = path.FindPath((thisFruit.nearestRow, thisFruit.nearestCol), pathwayExit)
                thisFruit.FollowNextPathWay()

        if thisGame.fruitScoreTimer > 0:
            thisGame.fruitScoreTimer -= 1

    def Draw(self):
        global rect_list
        if thisGame.mode == 3:
            return False

        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU

        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        if thisGame.mode == 1 or thisGame.mode == 8 or thisGame.mode == 9:
            if self.velX != 0 or self.velY != 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1