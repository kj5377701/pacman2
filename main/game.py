import pygame
import os
from parameter import *
from defs import get_image_surface


class game:

    def __init__(self):
        self.levelNum = 0
        self.score = 0
        self.lives = 3

        self.mode = 0
        self.modeTimer = 0
        self.ghostTimer = 0
        self.ghostValue = 0
        self.fruitTimer = 0
        self.fruitScoreTimer = 0
        self.fruitScorePos = (0, 0)

        self.SetMode(3)

        # camera variables
        self.screenTileSize = (SCREEN_TILE_SIZE_HEIGHT, SCREEN_TILE_SIZE_WIDTH)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)

        self.screenPixelPos = (0, 0)  # absolute x,y position of the screen from the upper-left corner of the level
        self.screenNearestTilePos = (0, 0)  # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position

        # numerical display digits
        self.digit = {}
        for i in range(0, 10, 1):
            self.digit[i] = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", str(i) + ".gif"))
        self.imLife = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "life.gif"))
        self.imGameOver = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "gameover.gif"))
        self.imReady = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "ready.gif"))
        self.imLogo = get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "logo.gif"))
        self.imHiscores = self.makehiscorelist()

    @staticmethod
    def defaulthiscorelist():
        return [(100000, "David"), (80000, "Andy"), (60000, "Count Pacula"), (40000, "Cleopacra"),
                (20000, "Brett Favre"), (10000, "Sergei Pachmaninoff")]

    @staticmethod
    def writehiscores(hs):
        """Given a new list, write it to the default file."""
        fname = os.path.join(SCRIPT_PATH, "res", "hiscore.txt")
        f = open(fname, "w")
        for line in hs:
            f.write(str(line[0]) + " " + line[1] + "\n")
        f.close()

    @staticmethod
    def getplayername():
        """Ask the player his name, to go on the high-score list."""
        if NO_WX:
            return USER_NAME
        # noinspection PyBroadException
        try:
            import wx
        except:
            print("""Pacman Error: No module wx. Can not ask the user his name!
                     :(       Download wx from http://www.wxpython.org/"
                     :(       To avoid seeing this error again, set NO_WX in file pacman.pyw.""")
            return USER_NAME
        app = wx.App(None)
        dlog = wx.TextEntryDialog(None, "You made the high-score list! Name:")
        dlog.ShowModal()
        name = dlog.GetValue()
        dlog.Destroy()
        app.Destroy()
        return name

    @staticmethod
    def PlayBackgoundSound(snd):
        channel_backgound.stop()
        channel_backgound.play(snd, loops=-1)

    def gethiscores(self):
        """If res/hiscore.txt exists, read it. If not, return the default high scores.
           Output is [ (score,name) , (score,name) , .. ]. Always 6 entries."""
        try:
            f = open(os.path.join(SCRIPT_PATH, "res", "hiscore.txt"))
            hs = []
            for line in f:
                while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"):
                    line = line[1:]
                while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"):
                    line = line[:-1]
                score = int(line.split(" ")[0])
                name = line.partition(" ")[2]
                if score > 99999999: score = 99999999
                if len(name) > 22: name = name[:22]
                hs.append((score, name))
            f.close()
            if len(hs) > 6: hs = hs[:6]
            while len(hs) < 6: hs.append((0, ""))
            return hs
        except IOError:
            return self.defaulthiscorelist()

    def updatehiscores(self, newscore):
        """Add newscore to the high score list, if appropriate."""
        hs = self.gethiscores()
        for line in hs:
            if newscore >= line[0]:
                hs.insert(hs.index(line), (newscore, self.getplayername()))
                hs.pop(-1)
                break
        self.writehiscores(hs)

    def makehiscorelist(self):
        global rect_list
        "Read the High-Score file and convert it to a useable Surface."
        # My apologies for all the hard-coded constants.... -Andy
        f = pygame.font.Font(os.path.join(SCRIPT_PATH, "res", "zig_____.ttf"), HS_FONT_SIZE)
        scoresurf = pygame.Surface((HS_WIDTH, HS_HEIGHT), pygame.SRCALPHA)
        scoresurf.set_alpha(HS_ALPHA)
        linesurf = f.render("HIGH SCORES".center(28), 1, (255, 255, 0))
        scoresurf.blit(linesurf, (0, 0))
        hs = self.gethiscores()
        vpos = 0
        for line in hs:
            vpos += HS_LINE_HEIGHT
            linesurf = f.render(line[1].ljust(18) + str(line[0]).rjust(10), 1, (255, 255, 255))
            scoresurf.blit(linesurf, (0, vpos))
        return scoresurf

    def drawmidgamehiscores(self):
        """Redraw the high-score list image after pacman dies."""
        self.imHiscores = self.makehiscorelist()

    def StartNewGame(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3

        self.SetMode(0)
        thisLevel.LoadLevel(thisGame.GetLevelNum())

    def AddToScore(self, amount):
        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore <= self.score + amount:
                snd_extralife.play()
                thisGame.lives += 1

        self.score += amount

    def DrawScore(self):
        global rect_list
        self.DrawNumber(self.score, (SCORE_XOFFSET, self.screenSize[1] - SCORE_YOFFSET))

        for i in range(0, self.lives, 1):
            screen.blit(self.imLife, (34 + i * 10 + 16, self.screenSize[1] - 18))

        screen.blit(thisFruit.imFruit[thisFruit.fruitType], (4 + 16, self.screenSize[1] - 28))

        if self.mode == 3:
            screen.blit(self.imGameOver, (self.screenSize[0] / 2 - (self.imGameOver.get_width() / 2),
                                          self.screenSize[1] / 2 - (self.imGameOver.get_height() / 2)))
        elif self.mode == 0 or self.mode == 4:
            screen.blit(self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12))

        self.DrawNumber(self.levelNum, (0, self.screenSize[1] - 20))

    def DrawNumber(self, number, x_y):
        global rect_list
        (x, y) = x_y

        strNumber = str(number)

        for i in range(0, len(str(number)), 1):
            if strNumber[i] == '.':
                break
            iDigit = int(strNumber[i])
            screen.blit(self.digit[iDigit], (x + i * SCORE_COLWIDTH, y))

    def SmartMoveScreen(self):
        possibleScreenX = player.x - self.screenTileSize[1] / 2 * TILE_WIDTH
        possibleScreenY = player.y - self.screenTileSize[0] / 2 * TILE_HEIGHT

        if self.screenSize[0] >= thisLevel.lvlWidth * TILE_WIDTH:
            possibleScreenX = -(self.screenSize[0] - thisLevel.lvlWidth * TILE_WIDTH) / 2
        elif possibleScreenX < 0:
            possibleScreenX = 0
        elif possibleScreenX > thisLevel.lvlWidth * TILE_WIDTH - self.screenSize[0]:
            possibleScreenX = thisLevel.lvlWidth * TILE_WIDTH - self.screenSize[0]

        if self.screenSize[1] >= thisLevel.lvlHeight * TILE_HEIGHT:
            possibleScreenY = -(self.screenSize[1] - thisLevel.lvlHeight * TILE_HEIGHT) / 2
        elif possibleScreenY < 0:
            possibleScreenY = 0
        elif possibleScreenY > thisLevel.lvlHeight * TILE_HEIGHT - self.screenSize[1]:
            possibleScreenY = thisLevel.lvlHeight * TILE_HEIGHT - self.screenSize[1]

        thisGame.MoveScreen((possibleScreenX, possibleScreenY))

    def MoveScreen(self, newX_newY):
        (newX, newY) = newX_newY
        self.screenPixelPos = (newX, newY)
        self.screenNearestTilePos = (
            int(newY / TILE_HEIGHT), int(newX / TILE_WIDTH))  # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (
            newX - self.screenNearestTilePos[1] * TILE_WIDTH, newY - self.screenNearestTilePos[0] * TILE_HEIGHT)

    def GetScreenPos(self):
        return self.screenPixelPos

    def GetLevelNum(self):
        return self.levelNum

    def SetNextLevel(self):
        self.levelNum += 1

        self.SetMode(0)
        thisLevel.LoadLevel(thisGame.GetLevelNum())

        player.velX = 0
        player.velY = 0
        player.anim_pacmanCurrent = player.anim_pacmanS

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0

        if newMode == 0:
            self.PlayBackgoundSound(snd_levelintro)
        elif newMode == 1:
            self.PlayBackgoundSound(snd_default)
        elif newMode == 2:
            self.PlayBackgoundSound(snd_death)
        elif newMode == 8:
            self.PlayBackgoundSound(snd_gh2gohome)
        elif newMode == 9:
            self.PlayBackgoundSound(snd_extrapac)
        elif newMode == 11:
            self.PlayBackgoundSound(snd_love)
        else:
            channel_backgound.stop()