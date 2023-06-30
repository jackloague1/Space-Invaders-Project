import time
import pygame as pg


class Sound:
    """Manages sound in game"""

    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.1)

        ship_explosion_sound = pg.mixer.Sound('sounds/ship_explosion.wav')
        laser_sound = pg.mixer.Sound('sounds/laser.wav')
        ufo_sound = pg.mixer.Sound('sounds/ufo.wav')
        gameover_sound = pg.mixer.Sound('sounds/gameover.wav')

        self.sounds = {'ship_explosion': ship_explosion_sound, 'laser': laser_sound, 
                       'ufo': ufo_sound, 'gameover': gameover_sound}

    def play_bg(self):
        """Plays main background music of game"""
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        """Stops background music"""
        pg.mixer.music.stop()

    def ship_explosion(self):
        """Plays ship explosion sound effect when a laser hits the ship"""
        ship_explosion = pg.mixer.Sound.play(self.sounds['ship_explosion'])
        ship_explosion.set_volume(0.3)

    def shoot_laser(self):
        """Plays laser sound when a laser is fired from ship or an alien"""
        pg.mixer.Sound.play(self.sounds['laser'])

    def ufo_hovering(self):
        """Plays UFO sound when it appears in game"""
        ufo_sound = pg.mixer.Sound.play(self.sounds['ufo'])
        ufo_sound.set_volume(0.2)

    def gameover(self): 
        """Stops main background music and plays game over theme"""
        self.stop_bg() 
        pg.mixer.music.load('sounds/gameover.wav')
        self.play_bg()
        time.sleep(2.8)
