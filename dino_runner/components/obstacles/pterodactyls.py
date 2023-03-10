import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Pterodactyls(Obstacle):
    Pterodactyls_Heights = [260, 210, 180]

    def __init__(self):
        self.type = 0
        super().__init__(BIRD, self.type)
        self.rect.y = self.Pterodactyls_Heights[random.randint(0, 2)]
        self.step_index = 0

    def draw(self, screen):        
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(BIRD[self.step_index // 5], self.rect)
        self.step_index += 1