import pygame as pg

from game_functions import clamp
from pygame.sprite import Sprite
from timer import Timer
from vector import Vector


class Ship(Sprite):
    """Represents the player ship"""
    ship_images = [pg.transform.rotozoom
                   (pg.image.load(f'images/ship1.png'), 0, 1.0)]
    ship_explosion_images = [pg.transform.rotozoom
                             (pg.image.load(f'images/ship_explosion{n}.png'), 0, 1.0)
                             for n in range(9)]

    def __init__(self, game):
        """Initializes the properties of the ship"""
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.sound = game.sound

        self.image = pg.image.load('images/ship1.png')
        self.rect = self.image.get_rect()
        self.posn = self.center_ship()
        self.vel = Vector()
        self.lasers = game.ship_lasers
        self.shooting = False
        self.lasers_attempted = 0
        self.dying = self.dead = False
        self.ships_left = game.settings.ship_limit

        self.timer_normal = Timer(image_list=Ship.ship_images)
        self.timer_explosion = Timer(image_list=Ship.ship_explosion_images, delay=50, is_loop=False)
        self.timer = self.timer_normal

    def center_ship(self):
        """Centers the ship at the bottom of the screen when starting each game"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)

    def reset(self):
        """Resets the ship's properties when beginning a new game"""
        self.vel = Vector()
        self.dying = self.dead = False
        self.posn = self.center_ship()
        self.timer = self.timer_normal
        self.timer_explosion.reset()
        self.lasers.reset()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y


    def hit(self):
        """Checks if ship is hit by an alien or alien laser"""
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            self.sound.ship_explosion()

    def die(self):
        """Resets or exits game based on remaining lives of ship"""
        self.ships_left -= 1
        print(f'Ship is dead! Only {self.ships_left} ships left')

        self.game.reset() if self.ships_left > 0 else self.game.game_over()

    def update(self):
        """Updates the properties of the ship"""
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.die()
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(game=self.game, x=self.rect.centerx, y=self.rect.top)
        self.lasers.update()
        self.draw()

    def draw(self):
        """Displays the ship on screen"""
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
