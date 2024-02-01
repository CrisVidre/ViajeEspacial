import pygame, random

resolucion = [800,600]
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(resolucion)
pygame.display.set_caption("Viaje Espacial")
clock = pygame.time.Clock()

def escribir(surface, text, size, x, y):
	font = pygame.font.SysFont("arial", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def barra_energia(surface, x, y, percentage):
	Dimensiones = [200,10]
	fill = (percentage / 150) * Dimensiones[0]
	border = pygame.Rect(x, y, Dimensiones[0], Dimensiones[1])
	fill = pygame.Rect(x, y, fill, Dimensiones[1])
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)


class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("assets/player.png").convert(), (50,50))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = resolucion[0] // 2
		self.rect.bottom = resolucion[1] - 10
		self.speed_x = 0
		self.escudo = 150

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > resolucion[0]:
			self.rect.right = resolucion[0]
		if self.rect.left < 0:
			self.rect.left = 0

	def disparar(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(resolucion[0] - self.rect.width)
		self.rect.y = random.randrange(-180, -100)
		self.speedy = random.randrange(1, 15)
		self.speedx = random.randrange(-8, 6)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > resolucion[1] + 10 or self.rect.left < -40 or self.rect.right > resolucion[0] + 40:
			self.rect.x = random.randrange(resolucion[0] - self.rect.height)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(2, 10)
		if self.rect.y > resolucion[1]+50:
			self.kill()

class Estrella(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("assets/stars.png"), (25,25))
		self.rect = self.image.get_rect()
		self.image.set_colorkey(GREEN)
		self.rect.x = random.randrange(resolucion[0] - self.rect.width)
		self.rect.y = random.randrange(-50, resolucion[1])
		self.speedy = random.randrange(1, 100)/100
		self.speedx = random.randrange(-100, 100)/1000

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > resolucion[1] + 10 or self.rect.left < -40 or self.rect.right > resolucion[0] + 40:
			self.rect.x = random.randrange(resolucion[0] - self.rect.height)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 100)/100
		if self.rect.y > resolucion[1]+50:
			self.kill()
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/laser1.png"), (36,12)),90)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < -10:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def menu():
	screen.fill(BLACK)
	estrellas = pygame.sprite.Group()
	for i in range(50):
			estrella = Estrella()
			estrellas.add(estrella)
	estrellas.draw(screen)
	escribir(screen, "VIAJE ESPACIAL", 65, resolucion[0] // 2, resolucion[1] // 4)
	escribir(screen, "Instrucciones:", 27, resolucion[0] // 2, resolucion[1] // 2)
	escribir(screen, "- Dispara con Espacio", 27, resolucion[0] // 2, resolucion[1] // 2 + 35)
	escribir(screen, "- Usa las flechas para moverte", 27, resolucion[0] // 2, resolucion[1] // 2 + 70)
	escribir(screen, "Presiona espacio para comenzar", 20, resolucion[0] // 2, resolucion[1] * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False


meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())


explosion_anim = []
for i in range(9):
	file = "assets/Colision0{}.png".format(i)
	img_scale = pygame.transform.scale(pygame.image.load(file).convert(), (50,50))
	img_scale.set_colorkey(BLACK)
	explosion_anim.append(img_scale)



#### ----------GAME OVER
game_over = True
running = True
while running:
	if game_over:

		menu()

		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		estrellas = pygame.sprite.Group()
		player = Jugador()
		all_sprites.add(player)
		for i in range(15):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)
		for i in range(50):
			estrella = Estrella()
			all_sprites.add(estrella)
			estrellas.add(estrella)



		marcador = 0

	clock.tick(60)
 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.disparar()

	all_sprites.update()

	#colisiones entre disparo y laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		marcador += 10
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	# Coliciones entre jugador y meteoros
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.escudo -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.escudo <= 0:
			game_over = True

	screen.fill(BLACK)

	all_sprites.draw(screen)

	#Marcador
	escribir(screen, str(marcador), 25, resolucion[0] // 2, 10)

	# Escudo.
	barra_energia(screen, 5, 10, player.escudo)

	pygame.display.flip()
pygame.quit()