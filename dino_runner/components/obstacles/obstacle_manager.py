import pygame

from dino_runner.components.obstacles.cactus import Cactus, Cactus1
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
 
    def __init__(self):
        self.obstacles = []
        self.cactus_small = False

        self.obstacles1 = []
        self.pterodactyls = False

    def update(self, game):

        if len(self.obstacles) == 0 and not self.cactus_small:
            cactus = Cactus(SMALL_CACTUS)
            self.obstacles.append(cactus)
            self.cactus_small = True
        elif len(self.obstacles) == 0 and self.cactus_small:
            cactus = Cactus1(LARGE_CACTUS)
            self.obstacles.append(cactus)
            self.cactus_small = False

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)   

            if game.player.dino_rect.colliderect(obstacle.rect):
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)