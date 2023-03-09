import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
import random

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            cactus_type = random.choice([SMALL_CACTUS, LARGE_CACTUS])
            self.obstacles.append(Cactus(cactus_type))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    pygame.time.delay(1000)
                    game.death_count +=1
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)
                    game.death_count += 1

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []