import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, GAME_OVER, RESET, DEFAULT_TYPE, CLOUD, CONTROL_UP, CONTROL_DOWN, SHIELD, HAMMER, SOUNDS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.menu import Menu
from dino_runner.components.counter import Counter
from dino_runner.components.power_ups.power_up_manager import PowerManager


class Game:
    GAME_SPEED = 20

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False 
        self.playing = False
        self.music = False
        self.game_speed = self.GAME_SPEED
        self.cloud = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.menu = Menu(self.screen)
        self.score = Counter()
        self.death_count = Counter()
        self.highest_score = Counter()
        self.power_up_manager = PowerManager()
        
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.reset_game()
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.score.update()
        self.update_game_speed()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_clouds()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        self.score.draw(self.screen)
        pygame.display.update()
        #pygame.display.flip()
    
    def draw_clouds(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (image_width + self.x_pos_bg +1020, self.y_pos_bg -250))
        self.screen.blit(CLOUD, (image_width + self.x_pos_bg +1070, self.y_pos_bg -250))
        self.screen.blit(CLOUD, (image_width + self.x_pos_bg +2030, self.y_pos_bg -300))

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        
    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count.count == 0:
            self.screen.blit(ICON, (half_screen_width - 50, half_screen_height - 140))
            self.screen.blit(CONTROL_UP, (30, 480))
            self.screen.blit(CONTROL_DOWN, (30, 530))
            self.screen.blit(SHIELD, (1020, 480))
            self.screen.blit(HAMMER, (1020, 530))
            self.menu.draw(self.screen, 'Press any key to start ...')
            self.menu.draw(self.screen, '<-- Jumping', 180, 503)
            self.menu.draw(self.screen, '<-- Ducking', 180, 553)
            self.menu.draw(self.screen, 'Inmortal -->', 915, 503)
            self.menu.draw(self.screen, 'Slow Speed -->', 890, 553)
            self.menu.draw(self.screen, 'Power Ups:', 945, 450)
            self.menu.draw(self.screen, 'Controls:', 130, 450)
            if not self.music:
                sounds = pygame.mixer.Sound(SOUNDS[0])
                sounds.play(-1)
                sounds.set_volume(0.3)
                self.music = True
        else:
            self.screen.blit(GAME_OVER, (360, 140))
            self.screen.blit(RESET, (510, 180))
            self.update_highest_score()
            self.menu.draw(self.screen, 'Press any key to restart')
            self.menu.draw(self.screen, f'Your score: {self.score.count}', half_screen_width, 350, )
            self.menu.draw(self.screen, f'Highest score: {self.highest_score.count}', half_screen_width, 400, )
            self.menu.draw(self.screen, f'Total deaths: {self.death_count.count}', half_screen_width, 450, )
            if not self.music:
                sounds = pygame.mixer.Sound(SOUNDS[1])
                sounds.play(-1)
                sounds.set_volume(0.3)
                self.music = True    
        self.menu.update(self)
                
    def update_game_speed(self):
        if self.score.count % 100 == 0 and self.game_speed < 500:
            self.game_speed += 3
            
    def update_highest_score(self):
        if self.score.count > self.highest_score.count:
            self.highest_score.set_count(self.score.count)
            
    def reset_game(self):
        self.power_up_manager.reset_power_ups()
        self.obstacle_manager.reset_obstacles()
        self.score.reset()
        self.game_speed = self.GAME_SPEED
        self.player.reset()
    
    def draw_power_up_time(self):
        if not self.music:
            sound = pygame.mixer.Sound(SOUNDS[2])
            sound.play(-1)
            sound.stop(SOUNDS[0])
            sound.set_volume(0.3)
            self.music = True
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >=0:
                self.menu.draw(self.screen, f'{self.player.type.capitalize()} enabled for {time_to_show} seconds', 300, 550)
            else :
                time_to_show = False
                self.player.type = DEFAULT_TYPE