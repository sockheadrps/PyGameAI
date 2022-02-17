import pygame
import config
from random import randint


class Robot():
	def __init__(self):
		self.health = 250
		self.damage = 5
		self.hits = 0
		print('robot created')

	def update(self):
		print('Robot updated')

	def attack(self, player_damage):
		self.health = self.health - player_damage
		self.hits = self.hits + 1
		return self.damage



	def render(self, screen):
		screen.blit(self.image, self.rect)
		print('render')
