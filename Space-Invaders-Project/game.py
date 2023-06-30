import sys
import time
import game_functions as gf
import pygame as pg

from alien import Aliens
from laser import Lasers, LaserType
from menu import Menu
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from sound import Sound
from ufo import Ufos


class Game:
    """Creates the Space Invaders game"""

    def __init__(self):
        """Initializes the properties of the game"""
        pg.init()

        self.settings = Settings()
        self.settings.initialize_speed_settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, 
                                  laser_type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, 
                                   laser_type=LaserType.ALIEN)
        
        self.ship = Ship(game=self)
        self.ufos = Ufos(game=self)
        self.aliens = Aliens(game=self)

        self.menu = Menu(game=self)

        self.title_font = pg.font.SysFont('arial', 80)
        self.button_font = pg.font.SysFont('arial', 64)
        self.text_font = pg.font.SysFont('arial', 32)

    def display_menu(self):
        """Displays the main menu of the game"""
        self.menu.title_screen()

    def reset(self):
        """Resets the game."""
        print('Resetting game...')
        time.sleep(1.5)
        self.ship.reset()
        self.aliens.reset()
        self.ufos.reset()

    def game_over(self):
        """Ends the current game and resets back to title screen."""
        print('All ships gone: game over!')

        # Write current score to high scores text file
        file = open("highscores.txt", "a")
        score_str = repr(self.scoreboard.score)
        file.write(score_str + "\n")
        file.close()

        self.sound.gameover()
        main()

    def play(self):
        """Initializes the game"""
        while True:
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.blit(self.settings.bg_image, self.settings.bg_image_rect)
            self.ship.update()
            self.aliens.update()
            self.ufos.update()
            self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.display_menu()


if __name__ == '__main__':
    main()
