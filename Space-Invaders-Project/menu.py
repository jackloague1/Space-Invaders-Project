import sys
import pygame as pg


class Menu:
    """The main menu of the game, consisting of the title screen and high scores screen"""

    def __init__(self, game):
        """Initializes the menu's properties"""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        self.title_font = pg.font.SysFont('arial', 80)
        self.button_font = pg.font.SysFont('arial', 64)
        self.text_font = pg.font.SysFont('arial', 32)

        # Creates text file for high scores if it does not already exist
        file = open("highscores.txt", "a+")
        file.close()

    def title_screen(self):
        """Represents the title screen"""
        title_space = self.title_font.render("Space", True, (255, 255, 255))
        title_invaders = self.title_font.render("Invaders", True, (0, 255, 0))
        alien0 = pg.transform.rotozoom(pg.image.load('images/alien_00.png'), 0, 0.8)
        alien1 = pg.transform.rotozoom(pg.image.load('images/alien_10.png'), 0, 0.8)
        alien2 = pg.transform.rotozoom(pg.image.load('images/alien_20.png'), 0, 0.8)
        ufo = pg.transform.rotozoom(pg.image.load('images/ufo.png'), 0, 0.7)
        alien0_points = self.text_font.render("= 40 PTS", True, (255, 255, 255))
        alien1_points = self.text_font.render("= 20 PTS", True, (255, 255, 255))
        alien2_points = self.text_font.render("= 10 PTS", True, (255, 255, 255))
        ufo_points = self.text_font.render("= ???", True, (255, 255, 255))
        start_button = self.button_font.render("Start", True, (0, 0, 255))
        high_scores_button = self.button_font.render("High Scores", True, (0, 0, 255))
        title_space_rect = title_space.get_rect(center=(self.settings.screen_width/2, 120))
        title_invaders_rect = title_invaders.get_rect(center=(self.settings.screen_width/2, 180))
        alien0_rect = alien0.get_rect(center=((self.settings.screen_width/2) - 80, 280))
        alien1_rect = alien1.get_rect(center=((self.settings.screen_width/2) - 80, 340))
        alien2_rect = alien2.get_rect(center=((self.settings.screen_width/2) - 80, 400))
        ufo_rect = ufo.get_rect(center=((self.settings.screen_width/2) - 80, 460))
        start_button_rect = start_button.get_rect(center=(self.settings.screen_width/2, 520))
        high_scores_button_rect = high_scores_button.get_rect(center=(self.settings.screen_width/2, 600))

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            mouse_position = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()
            if start_button_rect.collidepoint(mouse_position):
                if mouse_clicked[0]:
                    self.game.play()
            elif high_scores_button_rect.collidepoint(mouse_position):
                if mouse_clicked[0]:
                    self.high_scores_screen()

            self.screen.fill((0, 0, 0))
            self.screen.blit(title_space, title_space_rect)
            self.screen.blit(title_invaders, title_invaders_rect)
            self.screen.blit(alien0, alien0_rect)
            self.screen.blit(alien0_points, (580, 260))
            self.screen.blit(alien1, alien1_rect)
            self.screen.blit(alien1_points, (580, 320))
            self.screen.blit(alien2, alien2_rect)
            self.screen.blit(alien2_points, (580, 380))
            self.screen.blit(ufo, ufo_rect)
            self.screen.blit(ufo_points, (580, 440))
            self.screen.blit(start_button, start_button_rect)
            self.screen.blit(high_scores_button, high_scores_button_rect)
            pg.display.flip()

    def high_scores_screen(self):
        """Represents the high scores screen."""
        title = self.title_font.render("High Scores", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.settings.screen_width/2, 120))
        return_button = self.button_font.render("Return", True, (0, 0, 255))
        return_button_rect = return_button.get_rect(center=(self.settings.screen_width/2, 700))
        file = open("highscores.txt", "r")
        scores = []
        for line in file:
            scores.append(int(line[:-1]))
        file.close()
        scores.sort(reverse=True)
        top_scores = scores[:10]
        score_surfaces = []
        score_rects = []
        y = 240
        for score in top_scores:
            score_surfaces.append(self.text_font.render(repr(score), True, (255, 255, 255)))
        for surface in score_surfaces:
            score_rects.append(surface.get_rect(center=(self.settings.screen_width/2, y)))
            y += 40

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            mouse_position = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()
            if return_button_rect.collidepoint(mouse_position):
                if mouse_clicked[0]:
                    return False
            self.screen.fill((0, 0, 0))
            self.screen.blit(title, title_rect)
            for i in range(len(score_rects)):
                self.screen.blit(score_surfaces[i], score_rects[i])
            self.screen.blit(return_button, return_button_rect)
            pg.display.flip()
