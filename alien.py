import pygame as pg

from pygame.sprite import Sprite, Group
from random import randint
from sound import Sound
from timer import Timer


class Alien(Sprite):
    """Represents a single alien"""
    alien_images0 = [pg.transform.rotozoom
                     (pg.image.load(f'images/alien_0{n}.png'), 0, 0.7) 
                     for n in range(2)]
    alien_images1 = [pg.transform.rotozoom
                     (pg.image.load(f'images/alien_1{n}.png'), 0, 0.7) 
                     for n in range(2)]
    alien_images2 = [pg.transform.rotozoom
                     (pg.image.load(f'images/alien_2{n}.png'), 0, 0.7) 
                     for n in range(2)]
    alien_timers = {0: Timer(image_list=alien_images0),
                    1: Timer(image_list=alien_images1),
                    2: Timer(image_list=alien_images2)}
    alien_explosion_images0 = [pg.transform.rotozoom
                               (pg.image.load(f'images/alien0_explosion0{n}.png'), 0, 0.7)
                               for n in range(3)]
    alien_explosion_images1 = [pg.transform.rotozoom
                               (pg.image.load(f'images/alien1_explosion0{n}.png'), 0, 0.7)
                               for n in range(3)]
    alien_explosion_images2 = [pg.transform.rotozoom
                               (pg.image.load(f'images/alien2_explosion0{n}.png'), 0, 0.7)
                               for n in range(3)]
    alien_explosion_timers = {0: alien_explosion_images0,
                              1: alien_explosion_images1,
                              2: alien_explosion_images2}

    def __init__(self, game, alien_type):
        """Initializes the properties of alien sprite"""
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.sb = game.scoreboard

        self.image = pg.image.load('images/alien_00.png')
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = alien_type
        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.score = None       
        self.dying = self.dead = False

        self.timer_normal = Alien.alien_timers[alien_type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_timers[alien_type], 
                                     delay=200, is_loop=False)
        self.timer = self.timer_normal                                    

    def check_edges(self): 
        """Checks if alien reaches the left or right edge of the screen"""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        """Checks if alien reaches the bottom of screen or collides with the ship"""
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        """Displays the alien's explosion animation if hit"""
        if not self.dying:
            self.dying = True 
            self.timer = self.timer_explosion
            self.score = self.settings.get_alien_points(self.type)
            self.sb.increment_score(self.score)

    def update(self):
        """Updates the properties of alien sprite"""
        if self.timer == self.timer_explosion and self.timer.is_expired():
            # Removes alien sprite from any Group() which contains it
            self.kill()

        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        """Displays the alien sprite on screen"""
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    """Represents a fleet of aliens"""

    def __init__(self, game): 
        """Initializes the properties of the alien fleet"""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.ship = game.ship
        self.ship_lasers = game.ship_lasers.lasers
        self.ufos = game.ufos

        self.model_alien = Alien(game=game, alien_type=1)

        # Creates a container class that holds alien sprites
        self.aliens = Group()

        self.number_aliens = 0
        self.aliens_lasers = game.alien_lasers
        self.shoot_requests = 0

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.sound_value = 0

        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        """Returns the number of aliens that can fit from left to right on screen"""
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        """Returns the number of rows of aliens in the fleet"""
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows

    def reset(self):
        """Resets alien fleet"""

        # Removes all sprites from aliens Group() variable
        self.aliens.empty()

        self.sound_value = 0
        self.create_fleet()
        self.aliens_lasers.reset()

    def create_alien(self, alien_number, row_number):
        """Creates a single alien and adds it to the fleet"""
        # if row_number > 5: raise ValueError('row number must be less than 6')
        type = row_number // 2     
        alien = Alien(game=self.game, alien_type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number 
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.2 * alien.rect.height * row_number

        # Adds alien sprite to aliens Group() variable
        self.aliens.add(alien)

    def create_fleet(self):
        """Creates fleet of aliens"""

        # Get number of aliens that can fit from left to right in each row of the fleet
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width) 

        # Get number of rows for the fleet
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)

        number_aliens = 0

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)
                number_aliens += 1

        self.number_aliens = number_aliens

    def check_fleet_edges(self):
        """Checks if alien fleet hits edge of screen and needs to move down and change direction"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        """Checks if alien fleet reaches bottom of screen or collides with ship"""
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die()
                break

    def check_fleet_empty(self):
        """Resets game if alien fleet is empty of alien sprites"""
        if len(self.aliens.sprites()) == 0:
            print('Aliens all gone!')
            self.game.reset()

    def change_fleet_direction(self):
        """Moves alien fleet down and changes its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        """Fires laser from a random alien in the alien fleet"""
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return
        
        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def check_collisions(self):
        """Checks if a laser has hit an alien in the alien fleet"""
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)  
        if collisions:
            for alien in collisions:
                alien.hit()

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

    def speed_up_music(self):
        """Changes speed of background music based on how many aliens are left in the fleet"""
        if self.sound_value == 0:
            test = self.number_aliens
            self.sound.play_bg()
            self.sound_value = 1
        if len(self.aliens.sprites()) <= 44 and self.sound_value == 1:
            self.sound = Sound(bg_music="sounds/startrek_speed2.wav")
            self.sound.play_bg()
            self.sound_value = 2
        if len(self.aliens.sprites()) <= 22 and self.sound_value == 2:
            self.sound = Sound(bg_music="sounds/startrek_speed3.wav")
            self.sound.play_bg()
            self.sound_value = 3

    def update(self):
        """Updates the properties of alien fleet"""
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:
                alien.remove()
            # Calls update method in Alien Sprite class
            alien.update()
        self.aliens_lasers.update()
        self.speed_up_music()

    def draw(self):
        """Displays alien fleet on screen"""
        for alien in self.aliens.sprites():
            # Calls draw method in Alien Sprite class
            alien.draw() 
