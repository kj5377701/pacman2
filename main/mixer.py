import pygame
from parameter import *

pygame.mixer.pre_init(22050, -16, 1, 1024)
pygame.mixer.init()
pygame.mixer.set_num_channels(7)
channel_backgound = pygame.mixer.Channel(6)

snd_pellet = {
    0: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet1.wav")),
    1: pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "pellet2.wav"))
}

snd_levelintro = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "levelintro.wav"))
snd_default = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "default.wav"))
snd_extrapac = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extrapac.wav"))
snd_gh2gohome = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "gh2gohome.wav"))
snd_death = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "death.wav"))
snd_powerpellet = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "powerpellet.wav"))
snd_eatgh = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatgh2.wav"))
snd_fruitbounce = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "fruitbounce.wav"))
snd_eatfruit = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "eatfruit.wav"))
snd_extralife = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "extralife.wav"))
snd_love = pygame.mixer.Sound(os.path.join(SCRIPT_PATH, "res", "sounds", "All You Need Is Love.wav"))