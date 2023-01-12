import pygame

class UI:
	def __init__(self,surface):

		# setup 
		self.display_surface = surface # this will be our drawing surface

		# health 
		self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha() # upload the health image i made on ps
		self.health_bar_topleft = (54,39) #where to draw the rect
		self.bar_max_width = 152 # width and height of the bar that i will superpose on the health picture
		self.bar_height = 4

		# coins 
		self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha() # upload the coin picture
		self.coin_rect = self.coin.get_rect(topleft = (50,61)) #where to draw the rect ( gives us the center )
		self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',30) #get the font ( that will be used on the score )

	def show_health(self,current,full): # health bar has measure between 0 and 152 and the player has health between 0 and 100 so :
		self.display_surface.blit(self.health_bar,(20,10)) #draw the health bar we uploaded
		current_health_ratio = current / full #this gives us the right ratio and solves the issue i mentionned before
		current_bar_width = self.bar_max_width * current_health_ratio # this applies the radio and we have it applies on the bar
		health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height)) # to draw the bar we need the rect
		pygame.draw.rect(self.display_surface,'#dc4330',health_bar_rect) #voila , all we needed is which color , i put red

	def show_coins(self,amount):
		self.display_surface.blit(self.coin,self.coin_rect) # draw the coin pic
		coin_amount_surf = self.font.render(str(amount),False,'#33323d') # the amount we passed as a parameter will be made into a surface and eventually drawn I cast it into a string because the pygame method rect() expects an string alors que we have an int
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
		self.display_surface.blit(coin_amount_surf,coin_amount_rect) # voila the drawing !