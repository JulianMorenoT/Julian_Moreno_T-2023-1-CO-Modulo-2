import pygame


from dino_runner.utils.constants import SOUNDS


class Sounds():

    def __init__(self, play, stop) -> None:
        self.sounds = SOUNDS
        self.sounds_on = play
        self.sounds_off = stop