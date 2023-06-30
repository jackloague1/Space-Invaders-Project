import pygame as pg 


class Scoreboard:
    """Represents the score in game"""

    def __init__(self, game):
        """Initializes the properties of the scoreboard"""
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont('arial', 32)

        self.score_image = None
        self.label = None
        self.score_rect = None
        self.label_rect = None

        self.score = 0
        self.level = 0
        self.high_score = 0

        self.prep_score()

    def increment_score(self, alien_points):
        """Increments the score of the game"""
        self.score += alien_points
        self.prep_score()

    def prep_score(self):
        """Displays score in game"""
        self.label = self.font.render("Score:", True, self.text_color, pg.SRCALPHA)
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, pg.SRCALPHA)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.label_rect = self.label.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.label_rect.right = self.screen_rect.right - 100
        self.score_rect.top = 20
        self.label_rect.top = 20

    def reset(self):
        """Resets the score of game to zero"""
        self.score = 0
        self.update()

    def update(self):
        """Calls draw() method of scoreboard"""
        self.draw()

    def draw(self):
        """Displays score text on screen"""
        self.screen.blit(self.label, self.label_rect)
        self.screen.blit(self.score_image, self.score_rect)
