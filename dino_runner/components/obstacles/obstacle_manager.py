import pygame, random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.pterodactyls import Pterodactyls
from dino_runner.utils.constants import SHIELD_TYPE, HAMMER_TYPE, SOUNDS


class ObstacleManager:
 
    def __init__(self):
        self.obstacles = []

    def generate_obstacle(self, obstacle_type):
        if obstacle_type == 0:
            cactus_type = 'SMALL'
            obstacle = Cactus(cactus_type)
        elif obstacle_type == 1:
            cactus_type = 'LARGE'
            obstacle = Cactus(cactus_type)
        else:
            obstacle = Pterodactyls()
        return obstacle

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_type = random.randint(0, 2)
            obstacle = self.generate_obstacle(obstacle_type)
            self.obstacles.append(obstacle)
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.type == HAMMER_TYPE:
                self.obstacles.remove(obstacle)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    self.music = False
                    if not self.music:
                        sound = pygame.mixer.Sound(SOUNDS[5])
                        sound.play()
                        self.music = True
                    game.death_count.update()
                    game.playing = False
                else:
                    self.obstacles.remove(obstacle)
            
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []