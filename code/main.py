import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

class Game:
	def __init__(self):

		# game attributes
		self.max_level = 2 # we set the number of available levels at 0 ( default )
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0

		# overworld creation
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'

		# user interface 
		self.ui = UI(screen)


	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		#self.overworld_bg_music.stop()
		#self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		#self.overworld_bg_music.play(loops = -1)
		#self.level_bg_music.stop()

	def change_coins(self,amount): # mathod that affects coins by an amount ( method to be called in the level (create_lvl) )
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount

	def check_game_over(self): # a method to stop the game upon player death and resets everything ( gets us also back to the overworld )
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()

			screen.blit(text, (130, 600))
		else:
			self.level.run()
			self.ui.show_health(self.cur_health,self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
pygame.display.set_caption("RedHat Adventures: JP Edition")
font_path = "../graphics/ui/ARCADEPI.TTF"
font = pygame.font.Font(font_path, 40)
text = font.render(" PRESS SPACE TO CONTINUE ", True, (255, 255, 255))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('grey')
	game.run()

	pygame.display.update()
	clock.tick(60)