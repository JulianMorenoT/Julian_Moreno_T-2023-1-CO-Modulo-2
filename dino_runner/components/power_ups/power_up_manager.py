import pygame, random

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer


class PowerManager:

    def __init__(self):
        self.power_up = []
        self.when_appears = random.randint(200, 300)
        self.duration = random.randint(3, 5)

    def generate_power_up(self):
        self.when_appears += random.randint(200, 300)
        power_up = Shield()
        self.power_up.append(power_up)

    def update(self, game):
        if len(self.power_up) == 0 and self.when_appears == game.score.count:
            self.generate_power_up()

        for power_up in self.power_up:
            power_up.update(game.game_speed, self.power_up)
            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                game.player.type = power_up.type
                game.player.has_power_up = True
                game.player.power_time_up = power_up.start_time + (self.duration * 1000)
                self.power_up.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_up:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_up = []
        self.when_appears = random.randint(200, 300)