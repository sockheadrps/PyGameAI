import pygame
import config
import time


class Player():
	def __init__(self, x_position, y_position):
		self.position = [x_position, y_position]
		self.image = pygame.image.load("imgs/player/player17.png")
		self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
		self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE,
								config.SCALE)
		self.health = 5
		self.strength_xp = 1
		self.defense_xp = 1
		self.score = 0
		self.traveled = [(1, 1)]
		self.strength = 1
		self.attack_timer = time.time()
		self.attack_speed = 0
		self.is_attacking = False
		self.attack_cooldown = False
		self.xp_multiplier = 1
		self.damage = 3
		self.attack_sprites = []
		self.attack_sprites.append([pygame.transform.scale(pygame.image.load("imgs/player/p_r_1.png"),
														   (config.SCALE, config.SCALE))])
		self.attack_sprites.append([pygame.transform.scale(pygame.image.load("imgs/player/p_r_mid.png"),
														   (config.SCALE, config.SCALE))])
		self.attack_sprites.append([pygame.transform.scale(pygame.image.load("imgs/player/p_r_end.png"),
														   (config.SCALE, config.SCALE))])
		self.current_sprite = 0
		self.allowed = False
		self.bot_delta = []

	def update_position(self, new_position):
		self.position[0] = new_position[0]
		self.position[1] = new_position[1]



	def render(self, screen, camera):
		if not self.is_attacking:
			self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)
			screen.blit(self.image, self.rect)
		if self.is_attacking:
			image = pygame.image.load("imgs/player/punch.png")
			self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)
			screen.blit(image, self.rect)
			self.attack(screen, camera)




	def get_level(self, xp):
		if xp in range(1, 100):
			return 1
		if xp in range(100, 225):
			return 2
		if xp in range(225, 350):
			return 3
		if xp in range(350, 475):
			return 4
		if xp in range(475, 600):
			return 5
		if xp in range(600, 750):
			return 7
		if xp in range(600, 1000):
			return 8
		if xp in range(600, 1500):
			return 9
		if xp in range(600, 3000):
			return 10
		if xp > 3000:
			return 10


	def attack(self, screen, camera):
		attack_time = time.time()
		if attack_time - self.attack_timer >= self.attack_speed:
			self.strength_xp += 3 * self.xp_multiplier
			self.attack_cooldown = False
			self.is_attacking = True
			pygame.image.load("imgs/player/p_r_1.png")
			self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
			self.rect = pygame.Rect(self.position[0] * config.SCALE,
									self.position[1] * config.SCALE - (camera[1] * config.SCALE), config.SCALE,
									config.SCALE)
			screen.blit(self.image, self.rect)
			self.attack_timer = time.time()
			self.is_attacking = False
			str_level = self.get_level(self.strength_xp)
			damage = 5 * str_level + self.strength
			self.damage = damage
			if self.strength_xp >= 3000:
				self.strength_xp = 3000
			return self.damage

		else:
			self.attack_cooldown = True

	def player_dmg(self):
		return self.damage

	def take_damage(self, dmg):
		self.health = self.health - dmg




