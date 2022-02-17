import gym
from gym import spaces
import pygame
import config
from game import *
from game_state import GameState
import numpy as np
from time import time, sleep
import richer
import os
from math import floor

TICK_RATE = 10000
class GameEnv(gym.Env):
	"""Custom Environment that follows gym interface"""
	metadata = {'render.modes': ['human']}

	def __init__(self):
		super(GameEnv, self).__init__()
		# Define action and observation space
		# They must be gym.spaces objects
		# Example when using discrete actions:
		self.action_space = spaces.Discrete(5)
		# Example for using image as input:
		self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
											shape=(5,), dtype=np.float32)
		self.reward = 10
		self.iteration = 0
		self.games_won = 0
		self.games_lost = 0
		self.start_time = time()
		self.now_time = time()
		self.flip_time = time()
		self.e_time = time()
		self.done = False

	def step(self, action):
		self.iteration += 1
		self.clock.tick(TICK_RATE)
		previous_xp = self.game.player.strength_xp
		player_x = self.game.player.position[0]
		player_y = self.game.player.position[1]
		previous_health = self.game.player.health
		elapsed_time = int("%.0f" % (time() - self.e_time % 60))
		elapsed_time = int("%.0f" % (elapsed_time % 60))
		rich_elapsed_time = int("%.0f" % (time() - self.start_time % 60))
		rich_elapsed_time = int("%.0f" % (rich_elapsed_time % 60))

		if elapsed_time > 1:
			self.reward -= 1
			self.e_time = time()
		if rich_elapsed_time > 15:
			self.done = True
			self.reward = -100
			self.game.game_state = self.game.game_state.ENDED

		if action == 0:
			self.game.move_unit(self.game.player, [0, -1])
		if action == 1:
			self.game.move_unit(self.game.player, [0, 1])
		if action == 2:
			self.game.move_unit(self.game.player, [-1, 0])
		if action == 3:
			self.game.move_unit(self.game.player, [1, 0])
		if action == 4:
			self.game.player.is_attacking = True
			if self.game.player.position == [16, 13]:
				self.game.player.is_attacking = True
				player_damage = self.game.player.player_dmg()
				if player_damage:
					self.reward = self.reward + 100
					return_damage = self.game.robot.attack(player_damage)
					self.game.player.health = self.game.player.health - return_damage
			if self.game.player.position == [4, 21] and self.game.player.strength_xp <= 3000:
				self.reward += .25

		self.game.update()
		pygame.display.flip()
		self.flip_time = time()

		if self.game.player.health > previous_health:
			self.reward = self.reward + 100
		if previous_xp < self.game.player.strength_xp and self.game.player.strength_xp <= 3000:
			self.reward = self.reward + .1


		info = {}

		if self.game.game_state == self.game.game_state.WON:
			self.reward = self.reward + 1500
			self.reward += self.game.robot.hits * 5
			print('GAME WON!')
			richer.make_table(rich_elapsed_time, self.games_won, self.games_lost, self.reward, self.game.player.strength_xp, self.game.player.health,
							  self.game.robot.health, self.game.robot.hits)
			self.games_won += 1
			self.done = True
		elif self.game.game_state == self.game.game_state.ENDED:
			richer.make_table(rich_elapsed_time, self.games_won, self.games_lost, self.reward, self.game.player.strength_xp, self.game.player.health,
							  self.game.robot.health, self.game.robot.hits)
			print('GAME LOST!')
			self.games_lost += 1
			self.done = True

		elif self.iteration % 300 == 0:
			richer.make_table(rich_elapsed_time, self.games_won, self.games_lost, self.reward, self.game.player.strength_xp, self.game.player.health,
							  self.game.robot.health, self.game.robot.hits)
			print(self.observation)

		self.observation = np.float32([self.game.player.strength,
							self.game.player.strength_xp, self.game.player.health, self.game.robot.hits,
							self.game.robot.health], dtype=np.float32)


		return self.observation, self.reward, self.done, info


	def reset(self):
		self.start_time = time()
		self.done = False
		self.now_time = time()
		self.iteration += 1
		pygame.init()
		t = time()
		screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
		pygame.display.set_caption("Game")
		self.game = Game(screen)
		self.game.set_up()
		self.clock = pygame.time.Clock()
		self.reward = 0
		self.game.game_state = self.game.game_state.RUNNING
		player_x = self.game.player.position[0]
		player_y = self.game.player.position[1]
		self.reward = 0
		player_strength = self.game.player.strength
		player_score = self.game.player.score
		self.observation = np.array([self.game.player.strength,
							self.game.player.strength_xp, self.game.player.health, self.game.robot.hits,
							self.game.robot.health], dtype=np.float32)
		print(self.observation)
		return self.observation  # reward, done, info can't be included
