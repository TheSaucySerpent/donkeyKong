import pygame
import sys

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Donkey Kong")

running = True # variable to control the game loop
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False