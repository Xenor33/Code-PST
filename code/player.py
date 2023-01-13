import pygame 
from support import import_folder


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,change_health):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0 # the index used to switch between animations
		self.animation_speed = 0.15 # our animations speed
		self.image = self.animations['idle'][self.frame_index] # "idle" will be our default animation
		self.rect = self.image.get_rect(topleft = pos)

		# hadouken particles
		self.import_hadouken_particles()
		self.hadouken_frame_index = 0
		self.hadouken_animation_speed = 0.15
		self.display_surface = surface

		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface

		# player movement
		self.direction = pygame.math.Vector2(0,0) #in order to make player ineractions easier to code we needed to make a vector that defines the player directions ( vertical or horizontal by direction.x or .y )
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))

		# player status
		self.status = 'idle'# as mentionned before we will initialize the player as idle
		self.facing_right = True #starts facing right
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500 #the concept of vincibility was introduced because pygame doesnt see colisions as one but as so many , which is why we needed to make a concept of invicibility to give the player time to react to taking damage
		self.hurt_time = 0

		# audio 
		self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)


	def import_hadouken_particles(self):
		self.hadouken_particles = import_folder('../graphics/character/hadouken')

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0 #set it as 0 when we reach the max

		image = animation[int(self.frame_index)] # takes the last element of the arborescence
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.collision_rect.bottomleft
		else:
			flipped_image = pygame.transform.flip(image,True,False) # if the player is facing left the image switches just like what we did with the enemy when they hit the contraction
			self.image = flipped_image
			self.rect.bottomright = self.collision_rect.bottomright


		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)		

	def run_hadouken_animation(self):
		self.hadouken_frame_index += self.hadouken_animation_speed
		if self.hadouken_frame_index >= len(self.hadouken_particles):
			self.hadouken_frame_index=0

		hadouken_particle = self.hadouken_particles[int(self.hadouken_frame_index)]
		if self.facing_right:
				pos = self.rect.center - pygame.math.Vector2(-100,10)
				self.display_surface.blit(hadouken_particle,pos)

		else:
			pos = self.rect.center - pygame.math.Vector2(100,10)
			flipped_hadouken_particle = pygame.transform.flip(hadouken_particle, True, False)
			self.display_surface.blit(flipped_hadouken_particle, pos)


	def get_input(self): # game bindings :
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
	#	if keys[pygame.K_a]:
	#		self.run_hadouken_animation()

	def get_status(self): # change player status depending on the player vector's status
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self): # gravity concept
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed
		self.jump_sound.play()

	def get_damage(self):
		if not self.invincible: # we get damaged only when the invicility atttribute is off
			self.hit_sound.play()
			self.change_health(-10)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks() # get the time to make a timer correctly which will be used in the timer method

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks() # the timer we mentionned
			if current_time - self.hurt_time >= self.invincibility_duration: #when the time we took damage - the current time are supreior than the invibility duration we set up we can get damaged again
				self.invincible = False # we can get damaged once again



	def update(self):
		self.get_input()
		self.get_status()
		self.animate()

		self.invincibility_timer()
