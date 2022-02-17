import pygame
import config


class Beer():
	def __init__(self, x_position, y_position):
		print('Player created')
		self.position = [x_position, y_position]
		self.image = pygame.image.load("imgs/beer.png")
		self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
		self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE,
								config.SCALE)

	def update(self):
		print('beer updated')

	def render(self, screen):
		screen.blit(self.image, self.rect)


class Book():
	def __init__(self, x_position, y_position):
		print('Player created')
		self.position = [x_position, y_position]
		self.image = pygame.image.load("imgs/book.png")
		self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
		self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE,
								config.SCALE)

	def update(self):
		print('book updated')

	def render(self, screen):
		screen.blit(self.image, self.rect)
