import pygame

from dino_runner.components.obstacles.cactus import Cactus, Cactus1
from dino_runner.components.obstacles.pterodactyls import Pterodactyls
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
 
    def __init__(self):
        self.obstacles = []
        self.cactus_small = False
        self.cactus_large = False
        self.pterodactyls = True
        
    def update(self, game):

        if len(self.obstacles) == 0 and not self.cactus_small:
            cactus = Cactus(SMALL_CACTUS)
            self.obstacles.append(cactus)
            self.cactus_small = True
            self.cactus_large = True
            self.pterodactyls = False
        elif len(self.obstacles) == 0 and self.cactus_large:
            cactus = Cactus1(LARGE_CACTUS)
            self.obstacles.append(cactus)
            self.pterodactyls = True
            self.cactus_small = True
            self.cactus_large = False
        elif len(self.obstacles) == 0 and self.pterodactyls:
            pterodactyls = Pterodactyls(BIRD)
            self.obstacles.append(pterodactyls)
            self.pterodactyls = False
            self.cactus_large = False
            self.cactus_small = False

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)   

            if game.player.dino_rect.colliderect(obstacle.rect):
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)