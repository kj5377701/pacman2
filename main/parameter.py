import os
import sys

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()
else:
    SCRIPT_PATH = sys.path[0]

SCREEN_TILE_SIZE_HEIGHT = 23
SCREEN_TILE_SIZE_WIDTH = 30

TILE_WIDTH = TILE_HEIGHT = 24

# constants for the high-score display
HS_FONT_SIZE = 16
HS_LINE_HEIGHT = 16
HS_WIDTH = 408
HS_HEIGHT = 120
HS_XOFFSET = 180
HS_YOFFSET = 400
HS_ALPHA = 200

# new constants for the score's position
SCORE_XOFFSET = 50  # pixels from left edge
SCORE_YOFFSET = 34  # pixels from bottom edge (to top of score)
SCORE_COLWIDTH = 13  # width of each character

# See GetCrossRef() -- where these colors occur in a GIF, they are replaced according to the level file
IMG_EDGE_LIGHT_COLOR = (255, 206, 255, 255)
IMG_FILL_COLOR = (132, 0, 132, 255)
IMG_EDGE_SHADOW_COLOR = (255, 0, 255, 255)
IMG_PELLET_COLOR = (128, 0, 128, 255)

# NO_GIF_TILES -- tile numbers which do not correspond to a GIF file
# currently only "23" for the high-score list
NO_GIF_TILES = [23]

NO_WX = 0  # if set, the high-score code will not attempt to ask the user his name
USER_NAME = "User"  # USER_NAME=os.getlogin() # the default user name if wx fails to load or NO_WX

# Joystick defaults - maybe add a Preferences dialog in the future?
JS_DEVNUM = 0  # device 0 (pygame joysticks always start at 0). if JS_DEVNUM is not a valid device, will use 0
JS_XAXIS = 0  # axis 0 for left/right (default for most joysticks)
JS_YAXIS = 1  # axis 1 for up/down (default for most joysticks)
JS_STARTBUTTON = 0

ghostcolor = {
    0: (255, 0, 0, 255),
    1: (255, 128, 255, 255),
    2: (128, 255, 255, 255),
    3: (255, 128, 0, 255),
    4: (50, 50, 255, 255),
    5: (255, 255, 255, 255)
}

rect_list = []
