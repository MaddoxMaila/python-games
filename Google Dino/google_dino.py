''' 
  
  Author : Tshepang Maddox Maila
  Date   : 30 - 03 - 2020
  Descrp : Attempt At Recreating Of Google's Offline Dino Game

'''

import pygame
import random
import os
import time


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 460

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Maddoxs\' Google Dino')

def loadImage(image_name) :

	'''
	  use : load images from pygame
	  param : image name to be loaded
	  return : loaded image from pygame

	'''

	return pygame.image.load(os.path.join('assets', image_name))

# All Images To Of Dino To Be Animate To Simulate Movement 

DINO_STATES = [
                loadImage('dino1.jpeg'),
                loadImage('dino2.jpeg'),
                loadImage('dino3.jpeg'),
                loadImage('dino4.jpeg')
              ]

TREES_IMAGES = [
                 loadImage('tree1.jpeg'),
                 loadImage('tree2.jpeg'),
                 loadImage('tree3.jpeg'),
                 loadImage('tree4.jpeg')
               ]

BACKGROUND_IMAGE = [loadImage('bg.jpeg')]

BASE_IMAGE = [loadImage('base.jpeg')]

class Dino :

	DINOS = DINO_STATES
	ANIME_TIME = 5

	def __init__(self, x_position, y_position) :

		self.x = x_position
		self.y = y_position
		self.ground = self.y
		self.height = self.y
		self.tick_count = 0
		self.velocity = 0
		self.DINO_IMG = self.DINOS[0]
		self.image_count = 0

	def jump(self) :

		self.velocity = -5.5
		self.tick_count = 0

		self.height = self.y

	def move(self) :

		self.tick_count = self.tick_count + 1

		displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2 # Calculate The Displacement Of The Dino

		if displacement >= 5 :

			displacement = 4

		if displacement < 0 : 

			displacement -= 2

		self.x += displacement # Move The Dino In The X - AXIS


	def draw(self, window) : 

		self.image_count += 1

		if self.image_count < self.ANIME_TIME :

			self.DINO_IMG = self.DINOS[1]

		elif self.image_count < self.ANIME_TIME * 2 :

			self.DINO_IMG = self.DINOS[2]

			self.image_count  = 0

		window.blit(self.DINO_IMG, (self.x, self.y))



def drawGameWindow(window, dino) :

	window.blit(BACKGROUND_IMAGE[0], (0, 0))

	dino.draw(window)

	pygame.display.update()


def main() :

	dino = Dino(40, 330)

	run = True
	clock = pygame.time.Clock()

	while run:

		clock.tick(60)
		
		for event in pygame.event.get() :

			if event.type == 3 :

				if event.dict.get('key') == pygame.K_SPACE :

					dino.jump()

			if event.type == pygame.QUIT :

				run = False

		dino.move()
		drawGameWindow(GAME_WINDOW, dino)

	pygame.quit()

main()