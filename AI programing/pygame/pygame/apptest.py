import pygame
from JsonLoader import *
from MapLoader import *

# Load the Json file.
JsonLoader.LoadInJson()
windowSpecs = JsonLoader.Data["windowspecs"]
pygame.init()

done = False
clock = pygame.time.Clock()

screen = pygame.display.set_mode((windowSpecs["width"], windowSpecs["height"]))
pygame.display.set_caption("test")

# change window color to white
screen.fill((255,255,255))

map = Map("Karta Laboration 2.txt")
map.MakeGrid(screen)

# game loop
while not done:
	clock.tick(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True