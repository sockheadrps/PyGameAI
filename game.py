from player import Player
import pygame
from game_state import GameState
import config
from items import Beer, Book
from robot import Robot
from random import randint
import math
import richer

def get_delta_from_bot(player_coords):
	bot_delta_x = (player_coords[0] - 16) ** 2
	bot_delta_y = (player_coords[1] - 13) ** 2
	return math.sqrt(bot_delta_x + bot_delta_y)

class Game:
	def __init__(self, screen):
		self.screen = screen
		self.objects = []
		self.game_state = GameState.NONE
		self.map = []
		self.camera = [0, 0]
		self.render = False
		self.bot_delta = get_delta_from_bot([0, 0])

	def set_up(self):
		player = Player(0, 0)
		robot = Robot()
		self.player = player
		self.robot = robot
		self.objects.append(player)
		self.game_state = GameState.RUNNING

		self.load_map("01")

	def b_delta(self):
		return self.bot_delta

	def update(self):
		self.screen.fill(config.BLACK)
		self.handle_events()

		if self.render:
			self.render_map(self.screen)

		for object in self.objects:
			object.render(self.screen, self.camera)
		if self.player.health <= 0:
			self.game_state = GameState.ENDED
		if self.robot.health <= 0:
			self.game_state = GameState.WON
		# print(f"str xp {self.player.strength_xp} health: {self.player.health}, robot health: {self.robot.health}")

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game_state = GameState.ENDED
			# Key Events
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.game_state = GameState.ENDED
				elif event.key == pygame.K_w:
					self.move_unit(self.player, [0, -1])
				elif event.key == pygame.K_s:
					self.move_unit(self.player, [0, 1])
				elif event.key == pygame.K_a:
					self.move_unit(self.player, [-1, 0])
				elif event.key == pygame.K_d:
					self.move_unit(self.player, [1, 0])
				elif event.key == pygame.K_KP_1:
					self.player.is_attacking = True
				elif event.key == pygame.K_KP_PLUS:
					self.render = True
				elif event.key == pygame.K_KP_MINUS:
					self.render = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_KP_1:
					self.player.is_attacking = False

	def load_map(self, file_name):
		with open('maps/' + file_name + ".txt") as map_file:
			for line in map_file:
				tiles = []
				for i in range(0, len(line) - 1, 2):
					tiles.append(line[i])
				self.map.append(tiles)

	def render_map(self, screen):
		y_pos = 0
		for line in self.map:
			x_pos = 0
			for tile in line:
				image = map_tile_image[tile]
				rect = pygame.Rect(x_pos * config.SCALE, y_pos * config.SCALE, config.SCALE, config.SCALE)
				screen.blit(image, rect)
				x_pos = x_pos + 1

			y_pos = y_pos + 1

	def move_unit(self, unit, position_change):
		new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]
		self.player.xp_multiplier = 1


		if new_position[0] < 0 or new_position[0] > (len(self.map[0]) - 1):
			return
		if new_position[1] < 0 or new_position[1] > (len(self.map) - 1):
			return
		if self.map[new_position[1]][new_position[0]] == "W":
			return
		if self.map[new_position[1]][new_position[0]] == "R":
			self.player.strength = self.player.strength + 5
			self.map[new_position[1]][new_position[0]] = "G"
		if self.map[new_position[1]][new_position[0]] == "K":
			self.map[new_position[1]][new_position[0]] = "G"
			self.player.strength = self.player.strength - 6
		if new_position[0] <= (len(self.map[0]) - 1) and new_position[1] < 0 or new_position[1] <= 14:
			unit.update_position(new_position)
		if self.player.position == [16, 13]:
			self.player.is_attacking = True
			player_damage = self.player.player_dmg()
			if player_damage:
				return_damage = self.robot.attack(player_damage)
				self.player.health = self.player.health - return_damage
		self.player.bot_delta = get_delta_from_bot(new_position)
		if self.player.position == [9, 13]:
			self.player.health += 5
		if self.player.position == [8, 7]:
			self.player.xp_multiplier = 3


	def determine_camera(self):
		max_y_position = len(self.map) - config.SCREEN_HEIGHT / config.SCALE
		y_position = self.player.position[1] - math.ceil(round(config.SCREEN_HEIGHT / config.SCALE / 2))

		if y_position <= max_y_position and y_position >= 0:
			self.camera[1] = y_position
		elif y_position < 0:
			self.camera[1] = 0
		else:
			self.camera[1] = max_y_position


map_tile_image = {
	"G": pygame.transform.scale(pygame.image.load("imgs/tileGrass1.png"), (config.SCALE, config.SCALE)),
	"W": pygame.transform.scale(pygame.image.load("imgs/water.png"), (config.SCALE, config.SCALE)),
	"R": pygame.transform.scale(pygame.image.load("imgs/beer.png"), (config.SCALE, config.SCALE)),
	"K": pygame.transform.scale(pygame.image.load("imgs/book.png"), (config.SCALE, config.SCALE)),
	"B": pygame.transform.scale(pygame.image.load("imgs/robo.png"), (config.SCALE, config.SCALE)),
	"T": pygame.transform.scale(pygame.image.load("imgs/rai.png"), (config.SCALE, config.SCALE)),
	"H": pygame.transform.scale(pygame.image.load("imgs/health.png"), (config.SCALE, config.SCALE)),
}