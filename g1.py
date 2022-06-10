import pygame 
from sys import exit
from random import randint

start_time = 0

def player_animation():
	global  player_surface , player_index 
	if player_rect.bottom == 200 :
		player_index  = player_index + 0.2
		if player_index > 1 :
			player_index = 0 
		player_surface = player_walk[int(player_index)]
	else :
		player_surface = player_jump

def player_jump_Sound():
	if player_rect.bottom < 200:
		jump_sound.play()

def display_score():
	curr_time = pygame.time.get_ticks() - start_time
	time = int(curr_time/100) 
	actual_score_surface = test_font.render(f'{time}' , False , 'Black')
	actual_score_rect = actual_score_surface.get_rect(midtop = (700,40))
	screen.blit(actual_score_surface , actual_score_rect )
	return time

def obstacle_movement(obstacle_list):
	if obstacle_list :
		for obstacle_rect in obstacle_list :
			obstacle_rect.x -= 8
			if obstacle_rect.bottom == 200 :
				screen.blit(snail_surface , obstacle_rect)
			else :
				screen.blit(fly_surface , obstacle_rect)
		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50 ]
		return obstacle_list
	else :
		return [] 

def collisions(player , obstacle):
	if obstacle :
		for obstacle_rect in obstacle :
			if player.colliderect(obstacle_rect):
				return False
	return True

pygame.init()
screen = pygame.display.set_mode((800,300))
pygame.display.set_caption('UnsuperMario')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None , 40)
player_gravity = 0 
score  = 0
game_active = False
obstacle_rect_list = []

gameover_text = test_font.render('GAME OVER' , False,'Red') 
gameover_rect =gameover_text.get_rect( center = (400 , 50))
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('Unsuper Mario' , False, 'Red')
text_rect = text_surface.get_rect(center= (400,20))
score_text = test_font.render('score' , False,'Black')

#snail
snail_surface1 = pygame.image.load('graphics/snail/snail1.png')
snail_surface2 = pygame.image.load('graphics/snail/snail2.png')
snail_action = [snail_surface1 , snail_surface2]
snail_index = 0


#player
player_surface = pygame.image.load('graphics/player/player_stand.png')
player_w1 = pygame.image.load('graphics/player/player_walk_1.png')
player_w2 = pygame.image.load('graphics/player/player_walk_2.png')
player_walk = [player_w1 , player_w2]
player_index = 0 
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect( midbottom = (75,200))
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_jump1 = pygame.transform.rotozoom( player_jump , 180 , 1.5)
playerjump1_rect = player_jump1.get_rect( center = (400 ,150))
playerjump_rect = player_jump.get_rect( center = (400 ,150))



score_rect=score_text.get_rect(midtop =(700,10))
instruction_text = test_font.render('Hit <SPACE> to Play' , False , 'Black')
instruction_rect = instruction_text.get_rect(center = (400 , 250))

#fly
fly_surface1 = pygame.image.load('graphics/fly/fly1.png')
fly_surface1= pygame.transform.rotozoom(fly_surface1 , 0 , 0.4 )
fly_surface2 = pygame.image.load('graphics/fly/fly2.png')
fly_surface2= pygame.transform.rotozoom(fly_surface2 , 0 , 0.4 )
fly_action =[fly_surface1 , fly_surface2]
fly_index = 0 

#sound 

jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.1)
gameover_sound = pygame.mixer.Sound('audio/gameover.wav')
gameover_sound.set_volume(0.2)
#timer

obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer , 1100)

fly_timer = pygame.USEREVENT +2
pygame.time.set_timer(fly_timer , 200)

snail_timer = pygame.USEREVENT +3
pygame.time.set_timer(snail_timer , 300)


while True :
	for event in pygame.event.get():
		if event.type==pygame.QUIT :
			pygame.quit()
			exit()
		if game_active :
			if event.type == pygame.MOUSEBUTTONDOWN :
				if player_rect.collidepoint(event.pos) :
					if player_rect.bottom == 200 : 
						player_gravity = -18
						
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_UP :
					if player_rect.bottom == 200:
						player_gravity = -18
						
			if event.type == snail_timer :
				if snail_index == 0 :
					snail_index = 1 
				else :
					snail_index = 0
				snail_surface = snail_action[snail_index]
			if event.type == fly_timer :
				if fly_index == 0:
					fly_index = 1
				else :
					fly_index = 0 
				fly_surface= fly_action[fly_index]			
		else :
			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_SPACE :
					game_active = True
					start_time = pygame.time.get_ticks()
		if event.type == obstacle_timer and game_active :
			if randint(0,2) == 0 :
				obstacle_rect_list.append(snail_surface.get_rect( midbottom = (randint( 900 ,1400) ,200)))
			else :
				obstacle_rect_list.append(fly_surface.get_rect( center=  (randint( 900 ,1200)  ,80)) )	
	if game_active :		
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,200))
		
		pygame.draw.rect(screen , 'pink' , text_rect)
		pygame.draw.rect(screen , 'pink' , text_rect , 10 , 30 )
		screen.blit(text_surface , text_rect)
		#screen.blit(snail_surface,snail_rect)
	
		pygame.draw.rect(screen , 'Pink' , score_rect)
		pygame.draw.rect(screen , 'Pink' , score_rect, 10 , 30 )
		screen.blit(score_text, score_rect)
			
#displaying scores		
		score = display_score()

#playercodes 	
		player_gravity +=  1
		player_rect.y += player_gravity
		
		if player_rect.bottom > 200 : 
			player_rect.bottom = 200
		
		player_animation()
		player_jump_Sound()
		screen.blit(player_surface,player_rect) 
		
#obstacles
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)
#collisions
		game_active = collisions(player_rect , obstacle_rect_list)
	else : 
		
		screen.fill('Grey')
		obstacle_rect_list.clear()
		player_rect.bottom = 200
		player_gravity = 0 	
		if score== 0 :
			
			screen.blit(instruction_text , instruction_rect)
			screen.blit(player_jump , playerjump_rect)	
		else : 
			gameover_sound.play()
			score_disp = test_font.render(f'Your Score : {score}' , False , 'Black' )
			score_disp_rect = score_disp.get_rect( center= (400 , 250))
			screen.blit(score_disp , score_disp_rect)
			screen.blit(gameover_text , gameover_rect)
			screen.blit(player_jump1 , playerjump1_rect)
	pygame.display.update()
	clock.tick(60)

