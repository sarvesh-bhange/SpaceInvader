import pygame
import os 
pygame.font.init()
pygame.mixer.init()


WIDTH,HIGHT=900,500

BULLET_HIT=pygame.mixer.Sound(os.path.join('Assets','bullet_sound.mp3'))
BULLET_SOUND=pygame.mixer.Sound(os.path.join('Assets','spaceship_hit.wav'))

WIN=pygame.display.set_mode((WIDTH,HIGHT))

pygame.display.set_caption(' First Game ')

WITHE=(255, 255, 255)
BLACK = (0,0,0)

HEALTH_FONT=pygame.font.SysFont('comicsans',40)

WINNER_FONT=pygame.font.SysFont('comicsans',100)



BULLET_VEL = 13

MAX_bulets = 5



YELLOW_HIT=pygame.USEREVENT+1

RED_HIT=pygame.USEREVENT+2

RED= (237, 36, 36)
YELLOW= (239, 247, 2)

FPS=60
SPACESHIP_WIDTH,SPACESHIP_HEIGHT= 55, 40
VEL=5
BORDER=pygame.Rect(WIDTH//2 -5,0,10,HIGHT)

space=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HIGHT))


YELLOW_SPACESHIP_IMAGE =pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
RED_SPACESHIP_IMAGE =pygame.image.load(os.path.join('Assets','spaceship_red.png'))	
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

def draw_winner_text(text):
	draw_text=WINNER_FONT.render(text,1,WITHE)

	WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2,HIGHT/2 - draw_text.get_height()/2))

	pygame.display.update()
	pygame.time.delay(5000)

	


def draw_window(yellow,red,yellow_bullets,red_bullets,RED_HEALTH,YELLOW_HEALTH):

	WIN.blit(space,(0,0))
	pygame.draw.rect(WIN,BLACK,BORDER)

	for bullet in yellow_bullets: 
		pygame.draw.rect(WIN,YELLOW,bullet)

	for bullet in red_bullets:
		pygame.draw.rect(WIN,RED,bullet)
		
	
	WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
	WIN.blit(RED_SPACESHIP,(red.x,red.y))
	
	red_health_text=HEALTH_FONT.render('HEALTH:'+str(RED_HEALTH),1,WITHE)
	yellow_health_text=HEALTH_FONT.render('HEALTH:'+str(YELLOW_HEALTH),1,WITHE)

	WIN.blit(red_health_text,(10,10))
	WIN.blit(yellow_health_text,(WIDTH- yellow_health_text.get_width() -10,10))
	
	pygame.display.update()


def yellow_movement(keys_pressed,yellow):
	
	if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > (BORDER.x + BORDER.width):
			yellow.x-=VEL
		
	if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < WIDTH:
			yellow.x+=VEL
		
	if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
			yellow.y-=VEL
  
	if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HIGHT -15 : 
			yellow.y+=VEL


def red_movement(keys_pressed,red):
	
	if keys_pressed[pygame.K_a] and red.x - VEL > 0:
			red.x-=VEL
		
	if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
			red.x+=VEL
		
	if keys_pressed[pygame.K_w] and red.y - VEL > 0:
			red.y-=VEL

	if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HIGHT -15 :
			red.y+=VEL


def bullet_handle(yellow_bullets,red_bullets,yellow,red):
	for bullet in yellow_bullets:
		bullet.x -=BULLET_VEL

		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		
		elif bullet.x < 0:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x +=BULLET_VEL

		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)

		elif bullet.x > WIDTH:
			red_bullets.remove(bullet)






def main():
	clock = pygame.time.Clock()
	yellow = pygame.Rect(700,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
	red = pygame.Rect(100,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

	RED_HEALTH=10
	YELLOW_HEALTH=10

	winner_text=''

	yellow_bullets = []
	red_bullets = []
	
	run=True
	while run:
		clock.tick(FPS)
		

		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				run=False
				# pygame.quit() 

			if event.type == pygame.KEYDOWN:
				if event.key== pygame.K_RCTRL and len(yellow_bullets) < MAX_bulets:
					bullet=pygame.Rect(yellow.x  , yellow.y +yellow.height//2 -2,10,5)

					yellow_bullets.append(bullet)
					BULLET_HIT.play()

				
				if event.key== pygame.K_r:
					main()	
					
					

				if event.key== pygame.K_LCTRL and len(red_bullets) < MAX_bulets:
					bullet=pygame.Rect(red.x , red.y +red.height//2 -2,10,5)

					red_bullets.append(bullet)
					BULLET_HIT.play()
					
					


			if event.type==RED_HIT:
				RED_HEALTH -=1
				BULLET_SOUND.play()

			if event.type==YELLOW_HIT:
				YELLOW_HEALTH -=1
				BULLET_SOUND.play()

			winner_text=''

		if RED_HEALTH <= 0:
			winner_text='YELLOW WINS!'

		if YELLOW_HEALTH <=0:
			winner_text='RED WINS!'

		if winner_text !='':
			draw_winner_text(winner_text)
			main()



		bullet_handle(yellow_bullets,red_bullets,yellow,red)
				






		draw_window(yellow,red,yellow_bullets,red_bullets,RED_HEALTH,YELLOW_HEALTH)	
		keys_pressed=pygame.key.get_pressed()
		yellow_movement(keys_pressed,yellow)
		red_movement(keys_pressed,red)

	pygame.quit()


				
if __name__ =='__main__':
	main()		