import pygame as pg

from enum import Enum
from pygame.sprite import Sprite, Group
from random import randint
from timer import Timer


class LaserType(Enum):
    """Enumeration class that defines laser types with values"""
    ALIEN = 1
    SHIP = 2


class Laser(Sprite):
    """Manages lasers fired from aliens or the ship"""
    alien_laser_images = [pg.transform.rotozoom
                          (pg.image.load(f'images/alien_laser{n}.png'), 0, 0.7) 
                          for n in range(2)]
    ship_laser_images = [pg.transform.rotozoom
                         (pg.image.load(f'images/ship_laser{n}.png'), 0, 0.7) 
                         for n in range(2)]
    laser_images = {LaserType.ALIEN: alien_laser_images, 
                    LaserType.SHIP: ship_laser_images}

    def __init__(self, settings, screen, x, y, sound, laser_type):
        """Initializes the properties of laser sprite"""
        super().__init__()
        self.rect = pg.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.screen = screen
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)
        self.type = laser_type
        self.speed_factor = settings.laser_speed_factor
        imagelist = Laser.laser_images[laser_type]
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.timer = Timer(image_list=imagelist, delay=200)

        sound.shoot_laser()

    def update(self):
        """Updates the properties of laser sprite"""
        self.y += self.speed_factor if self.type == LaserType.ALIEN else -self.speed_factor
        self.rect.y = self.y
        self.draw()

    def draw(self):
        """Displays laser sprite on screen"""
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Lasers:
    """Represents a group of lasers"""

    def __init__(self, settings, laser_type):
        """Initializes the properties of the laser group"""
        self.settings = settings
        self.type = laser_type

        # Creates a container class that holds laser sprites
        self.lasers = Group()

    def reset(self):
        """Removes all sprites from lasers Group() variable"""
        self.lasers.empty()

    def shoot(self, game, x, y):
        """Adds laser sprites to lasers Group() variable"""
        self.lasers.add(Laser(settings=game.settings, screen=game.screen,
                              x=x, y=y, sound=game.sound, laser_type=self.type))

    def update(self):
        """Updates the properties of laser group"""

        # Calls update method in Laser Sprite class
        self.lasers.update()

        # laster.copy() creates a copy of the lasers Group() variable with all the same sprites
        for laser in self.lasers.copy():
            # If laser reaches the bottom of screen, remove it from lasers Group() variable
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

    def draw(self):
        """Displays group of lasers on screen"""

        # lasers.sprites() returns a list of all sprites from lasers Group() variable
        for laser in self.lasers.sprites():
            # Calls draw method in Laser Sprite class
            laser.draw()