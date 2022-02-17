import pygame
import config
import game
from game_state import GameState
import player

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

pygame.display.set_caption("Game")

clock = pygame.time.Clock()

game = game.Game(screen)
game.set_up()
tick = 0

while game.game_state == GameState.RUNNING:
	tick +=1
	# clock.tick(1000000)
	game.update()
	print(game.player.strength_xp)
	pygame.display.flip()
	g_time = pygame.time.get_ticks() / 1000

