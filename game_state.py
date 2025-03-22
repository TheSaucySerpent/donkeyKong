import pygame

class GameState:
    def __init__(self):
        self.score = 0 
        self.lives = 3
        self.level = 1
        self.game_over = False
    
    def add_score(self, points):
        self.score += points
    
    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
           self.game_over = True
    
    def next_level(self):
      self.level += 1

    def draw(self, screen):
      font = pygame.font.Font(None, 36)
      score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
      lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
      level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))

      # Get the screen width dynamically
      screen_width = screen.get_width()
      margin = 10

      # Create rects with top right alignment
      score_rect = score_text.get_rect(topright=(screen_width - margin, margin))
      lives_rect = lives_text.get_rect(topright=(screen_width - margin, score_rect.bottom + 5))
      level_rect = level_text.get_rect(topright=(screen_width - margin, lives_rect.bottom + 5))

      screen.blit(score_text, score_rect)
      screen.blit(lives_text, lives_rect)
      screen.blit(level_text, level_rect)

      # if game over, draw the message centered on the screen
      if self.game_over:
        game_over_font = pygame.font.Font(None, 72)  # larger font for game over message
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        # get the screen's height and width
        screen_width, screen_height = screen.get_size()
        game_over_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(game_over_text, game_over_rect)

        press_space_font = pygame.font.Font(None, 36)
        press_space_text = press_space_font.render("Press Space to Play Again", True, (255, 255, 255))
        press_space_rect = press_space_text.get_rect(center=(screen_width/2, game_over_rect.bottom + 30))
        screen.blit(press_space_text, press_space_rect)