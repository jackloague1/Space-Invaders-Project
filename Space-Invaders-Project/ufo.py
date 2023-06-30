import pygame as pg

from pygame.sprite import Sprite, Group
from random import randint, randrange
from timer import Timer
from vector import Vector


class Ufo(Sprite):
    """Represents a UFO sprite that appears randomly during game"""
    ufo_images = [pg.transform.rotozoom
                  (pg.image.load(f'images/ufo.png'), 0, 0.7)]

    def __init__(self, game):
        """Initializes the UFO sprite's properties"""
        super().__init__()
        self.start_time = pg.time.get_ticks()
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.sound = game.sound
        self.sb = game.scoreboard

        self.image = pg.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.left = self.screen_rect.left - 120
        self.rect.top = self.screen_rect.top + 20
        self.vel = Vector()
        self.x = float(self.rect.x)
        self.score = None
        self.score_image = None
        self.score_rect = None
        self.appear = False
        self.score_appear = False
        self.off_screen = False
        self.dying = self.dead = False

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont('arial', 32)

        self.timer_normal = Timer(image_list=Ufo.ufo_images)
        self.timer = self.timer_normal

        self.sound.ufo_hovering()

    def check_edges(self):
        """Checks if the UFO sprite moves off the screen"""
        screen_rect = self.screen.get_rect()
        return self.rect.left >= screen_rect.right

    def hit(self):
        """Award points to the player since the UFO was hit"""
        if not self.dying:
            print('SHIP IS HIT !!!!!!!!!!!!!!!!!!!!!')
            self.dying = True
            self.score = self.settings.get_alien_points(3)
            score_str = str(self.score)
            self.score_image = self.font.render(score_str, True, self.text_color, pg.SRCALPHA)
            self.score_rect = self.score_image.get_rect()
            self.score_rect.right = self.rect.right
            self.sb.increment_score(self.score)

        self.score_appear = True

    def out_of_bounds(self):
        """Sets the UFO's off_screen variable to true"""
        self.dying = True
        self.off_screen = True

    def update(self):
        """Updates properties of UFO sprite"""
        if self.timer == self.timer_normal:
            self.x += 0.5
            self.rect.x = self.x

            current_time = pg.time.get_ticks()
            time_passed = current_time - self.start_time

            if time_passed/1000 > 0.15:
                self.sound.ufo_hovering()
                self.start_time = pg.time.get_ticks()
        self.draw()

    def draw(self):
        """Displays the UFO sprite on screen"""
        if self.dying == True:
            # Removes ufo sprite from any Group() which contains it
            self.kill()
        if self.timer == self.timer_normal:
            image = self.timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.rect.left, self.rect.top
            self.screen.blit(image, rect)


class Ufo_Score(Sprite):
    """Represents the score sprite displayed after a UFO is destroyed"""

    def __init__(self, game, score_image, score_rect):
        """Initializes the properties of the UFO score sprite"""
        super().__init__()

        # get_ticks() obtains the amount of time passed since game initialized in milliseconds
        self.start_time = pg.time.get_ticks()

        self.screen = game.screen
        self.score_image = score_image
        self.score_rect = score_rect
        self.score_rect.left = self.score_rect.left - 80
        self.score_rect.top = self.score_rect.top + 20
        self.remove = False

    def update(self):
        """Updates the properties of the UFO score sprite"""
        self.draw()

    def draw(self):
        """Displays the UFO score sprite on screen"""
        current_time = pg.time.get_ticks()
        time_passed = current_time - self.start_time

        # If 3 seconds have passed since UFO score was displayed, remove the score from screen
        if time_passed/1000 > 3:
            self.remove = True
            self.kill()

        self.screen.blit(self.score_image, self.score_rect)

class Ufos:
    """Represents the various UFOs throughout the game"""
    
    def __init__(self, game):
        """Initializes the properties of the UFO"""
        self.game = game
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()
        self.ship = game.ship
        self.ship_lasers = game.ship_lasers.lasers
        self.start_time = pg.time.get_ticks()

        # Creates a container class that holds UFO sprites
        self.ufos = Group()

        # Creates a container class that holds UFO score sprites
        self.ufoScores = Group()

    def add_ufo(self):
        """Creates a new UFO"""
        ufo = Ufo(game=self.game)

        # Adds UFO sprite to ufos Group() variable
        self.ufos.add(ufo)

    def add_ufo_score(self, score_image, score_rect):
        """Creates a new UFO score"""
        ufo_score = Ufo_Score(game=self.game, score_image=score_image, score_rect=score_rect)

        # Adds UFO score sprite to ufoScores Group() variable
        self.ufoScores.add(ufo_score)

    def check_collisions(self):
        """Checks if a laser has hit a UFO or if the UFO has gone off screen"""
        collisions = pg.sprite.groupcollide(self.ufos, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()

        for ufo in self.ufos.sprites():
            if ufo.rect.left >= self.screen_rect.right:
                ufo.out_of_bounds()

    def reset(self):
        """Resets the properties of the UFO"""
        self.ufos.empty()
        self.ufoScores.empty()
        self.start_time = pg.time.get_ticks()

    def update(self):
        """Updates the properties of the UFO"""
        self.check_collisions()

        for ufo in self.ufos.sprites():
            if ufo.score_appear:
                self.start_time = pg.time.get_ticks()
                self.add_ufo_score(ufo.score_image, ufo.score_rect)
            if ufo.off_screen:
                self.start_time = pg.time.get_ticks()
            if ufo.dead:
                ufo.remove()
            ufo.update()
        
        for ufo_score in self.ufoScores.sprites():
            if ufo_score.remove:
                ufo_score.remove()
            ufo_score.update()
        
        current_time = pg.time.get_ticks()
        time_passed = current_time - self.start_time

        # If there are no UFOs in the ufos Group() variable, and at least a specified amount
        # of seconds have passed since the game began or the last UFO despawned, a new UFO has 
        # a chance to be added
        if len(self.ufos.sprites()) == 0 and time_passed/1000 > self.settings.ufo_appears_every and randint(0,1000) == 0:
           self.add_ufo()

    def draw(self):
        """Displays a UFO on screen"""
        for ufo in self.ufos.sprites():
            ufo.draw()