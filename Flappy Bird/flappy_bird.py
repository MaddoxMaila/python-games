import pygame
import time
import os
import random

WINDOW_WIDTH = 270
WINDOW_HEIGHT = 400

# For Reusability, function to handle all image loads

def load_img(img_name) :

	return pygame.image.load(os.path.join('assets', img_name))

# Since The Bird Changes Through 3 Different States
# Init A List To Hold All Those 3 States

BIRD_IMGS = [
							load_img('bird1.png'),
							load_img('bird2.png'),
							load_img('bird3.png')
            ]

PIPE_IMG = load_img('pipe.png') # Pipe Image

BACKGROUND_IMG = load_img('background.png') # Background Image

BASE_IMG = load_img('base.png') # Base Image

class Bird :

	# Class Variables

	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIME_TIME = 5

	def __init__(self, x, y) :

		# Instance Variables

		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.velocity = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self) : 

		self.velocity = -5.5
		self.tick_count = 0
		self.height = self.y


	def move(self) :

		# Game Time
		self.tick_count = self.tick_count + 1

		# Get Displacement
		d = self.velocity*self.tick_count + 1.5*self.tick_count**2 # Get Displacement Of The Bird, Itll Be In Pixels

		if d >= 5 :

			d = 4

		if d < 0 : 

			d -= 2

		self.y += d # This Is Going To Confuse Me In The Future

		if d < 0 or self.y < self.height + 30 :

			if self.tilt < self.MAX_ROTATION :

				self.tilt = self.MAX_ROTATION

		else :

			if self.tilt > -90 :

				self.tilt -= self.ROT_VEL


	def draw(self, win) :

		 self.img_count += 1

		# Change The Image States After Some Time
		# To Animate The Bird To Symbolise Thats Its Flapping Its Wings

		if self.img_count < self.ANIME_TIME :

			self.img = self.IMGS[0]

		elif self.img_count < self.ANIME_TIME * 2 :

			self.img = self.IMGS[1]

		elif self.img_count < self.ANIME_TIME * 3 :

			self.img = self.IMGS[2]

		elif self.img_count < self.ANIME_TIME * 4 :

			self.img = self.IMGS[1]

		elif self.img_count == self.ANIME_TIME * 4 + 1 :

			self.img = self.IMGS[0]

			self.img_count = 0

		if self.tilt <= -80 :

			self.img = self.IMGS[1]

			self.img_count = self.ANIME_TIME * 2
 
		rotated_image = pygame.transform.rotate(self.img, self.tilt)

		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)

		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self) :

		return pygame.mask.from_surface(self.img)


class Pipe :

	GAP = 90
	VEL = 2

	def __init__(self, x) :

		self.x = x
		self.height = 0
		self.gap = 30

		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self) :

		self.height = random.randrange(50, 200)

		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self) : 

		self.x -= self.VEL

	def draw(self, window) :

		window.blit(self.PIPE_TOP, (self.x, self.top))
		window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird) :

		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		top_point = bird_mask.overlap(top_mask, top_offset)
		bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

		if top_point or bottom_point :

			return True

		return False

class Base :

	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y) :

		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self) :

		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0 :

			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0 :

			self.x2 = self.x1 + self.WIDTH

	def draw(self, window) :

		window.blit(self.IMG, (self.x1, self.y))
		window.blit(self.IMG, (self.x2, self.y))



def draw_window(window, bird, pipes, base) :

	window.blit(BACKGROUND_IMG, (0, 0))

	for pipe in pipes :

		pipe.draw(window)

	base.draw(window)
	bird.draw(window)
	pygame.display.update()


def main() : # MAIN method to run the whole class

	bird = Bird(50, 130) # Create A Bird Object

	pipes = [Pipe(300)]
	base = Base(380)

	window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Draw Game Display

	clock = pygame.time.Clock() # Game Clock

	score = 0

	run = True
	pygame.joystick.init()

	while run : # Main Game Loop

		clock.tick(30) # Should Run At 30FPS - 30 Frames Per Second

		rem = []
		add_pipe = False

		for event in pygame.event.get() :

			if event.type == 3 :

				if event.dict.get('key') == pygame.K_SPACE : # Move The Bird UPPPPP

					#code...
					bird.jump()
				

			if event.type == pygame.QUIT :

				run = False

		for pipe in pipes :

			if pipe.collide(bird) :

				# print('-- Collision Detected  -- DIE BITCHHH DIEEEE')
				run = False

				pass

			if pipe.x + pipe.PIPE_TOP.get_width() < 0 :

				rem.append(pipe)

			if not pipe.passed and pipe.x < bird.x :

				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe :

			score += 1
			pipes.append(Pipe(300))

			for r in rem :

				pipes.remove(r)

		bird.move()
		base.move()
		draw_window(window, bird, pipes, base)

	# pygame.quit()

	if not run :

		print('--- Collision Detected --- \n=====================\n=   YOU\'RE A LOSER  =\n=   SCORE : {}       = \n====================='.format(score))

main()
   