import pygame
from config import FONT_SIZE, FONT_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
import os


class Lives:
    def __init__(self, player, player_lives):
        self.player = player
        self.lives = player_lives
        self.x = 50
        self.y = 785

    def draw_lives_text(self, screen):
        # Load the font
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Create a text surface with "Credits"
        # print(f"Lives class self.lives: {self.lives}")
        text_surface = font.render(str(self.lives), True, (255, 255, 255))  # White color
        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        # Set the position of the text surface relative to the baseline
        text_rect.midtop = (self.x, self.y)
        # Draw the text surface on the screen
        screen.blit(text_surface, text_rect)

    def draw_lives_lost_text(self, screen):
        self.lives -= 1
        # Load the font
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Create a black surface with the same size as the text surface
        text_surface = font.render("-1 Life", True, (255, 255, 255))  # White color
        text_rect = text_surface.get_rect()
        # Set the position of the text surface to the center of the screen
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        # Draw the text surface on the screen
        screen.blit(text_surface, text_rect)

    def draw_player_sprites(self, screen):
        if self.lives >= 2:
            # Draw the first player image
            screen.blit(self.player.image, (self.x + 50, self.y))
        if self.lives == 3:
            # Draw the second player image next to the first one
            screen.blit(self.player.image, (self.x + 130, self.y))

    def update_lives(self, screen):
        self.draw_lives_text(screen)
        self.draw_player_sprites(screen)


class Scoreboard:
    def __init__(self, starting_score):
        self.score = starting_score
        self.highscore = self.get_top_score()
        self.score_x = 0
        self.score_y = 0
        self.highscore_x = 0
        self.highscore_y = 0

    def draw_starting_score(self, screen):
        # Load font
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE - 10)

        # Create Score and Highscore surfaces
        score_surface = font.render(str(self.score), True, (255, 255, 255))
        highscore_surface = font.render(str(self.highscore), True, (255, 255, 255))

        # Set locations of each score element
        score_surface_loc = (120, 40)
        highscore_surface_loc = (410, 40)

        # display score text on screen
        screen.blit(score_surface, score_surface_loc)
        screen.blit(highscore_surface, highscore_surface_loc)

    def update_score(self, increment):
        # Update score with increment
        self.score += increment
        # Update highscore if score surpasses highscore
        if self.score > self.highscore:
            self.highscore = self.score
            self.update_top_score(self.highscore)

    @staticmethod
    def get_top_score():
        top_score_file = "top_score.txt"

        if os.path.exists(top_score_file):
            with open(top_score_file, "r") as file:
                try:
                    top_score = int(file.read().strip())
                    return top_score
                except ValueError:
                    print("Error reading top score. Resetting to 0.")
                    return 0
        else:
            print("Top score file not found. Creating a new one.")
            with open(top_score_file, "w") as file:
                file.write("0")
            return 0

    def update_top_score(self, new_score):
        top_score_file = "top_score.txt"
        current_top_score = self.get_top_score()

        if new_score > current_top_score:
            with open(top_score_file, "w") as file:
                file.write(str(new_score))
            print(f"New top score: {new_score}")
        else:
            print(f"Current top score: {current_top_score}")

    @staticmethod
    def draw_static_score(screen):
        # Load font
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE - 10)
        # # Create a text surface for static score and other elements
        score_surface = font.render("S C O R E < 1 >", True, (255, 255, 255))
        highscore_surface = font.render("H I - S C O R E", True, (255, 255, 255))
        score2_surface = font.render("S C O R E < 2 >", True, (255, 255, 255))
        # create locations for all static score text
        score_surface_loc = (45, 6)
        highscore_surface_loc = (380, 6)
        score2_surface_loc = (725, 6)
        # Create blits for all static score text
        screen.blit(score_surface, score_surface_loc)
        screen.blit(highscore_surface, highscore_surface_loc)
        screen.blit(score2_surface, score2_surface_loc)
