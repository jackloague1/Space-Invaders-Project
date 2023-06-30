import pygame as pg

from random import randrange


class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)
        self.bg_image = pg.image.load('images/space_background.jpg')
        self.bg_image_rect = self.bg_image.get_rect()
        
        # Laser settings
        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 50           # change to 1 to see faster lasers

        # Alien settings
        self.aliens_shoot_every = 500    # about every 2 seconds at 60 fps
        self.ufo_appears_every = 10
        self.alien_points = {0: 40, 1: 20, 2: 10}

        # Ship settings
        self.ship_limit = 3         # total ships allowed in game before game over

        # Fleet settings
        self.fleet_drop_speed = 10
        self.fleet_direction = 1     # change to a Vector(1, 0) move to the right, and ...
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        """Stores speed settings of ships, aliens, and lasers for game"""
        self.alien_speed_factor = 0.25
        self.ship_speed_factor = 3
        self.laser_speed_factor = 1

    def increase_speed(self):
        """Increases speed of ship and lasers"""
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale

    def get_alien_points(self, alien_type):
        if alien_type != 3:
            return self.alien_points[alien_type]
        else:
            return randrange(50, 100, 10)