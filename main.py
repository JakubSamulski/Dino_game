import pygame
import os

import time
import random
#Constants


pygame.init()
SCREEN_H=729
SCREEN_W=1280

SCREEN = pygame.display.set_mode((SCREEN_W,SCREEN_H))

#Loading assets
DINO_RUNNING = [pygame.image.load(r'Assets/Dino/DinoRun1.png'),pygame.image.load(r'Assets/Dino/DinoRun2.png')]
DINO_JUMPING = pygame.image.load(r'Assets/Dino/DinoJump.png')
DINO_DUCKING = [pygame.image.load(r'Assets/Dino/DinoDuck1.png'),
                pygame.image.load(r'Assets/Dino/DinoDuck2.png')]
DINO_DEAD = pygame.image.load(r'Assets/Dino/DinoDead.png')
DINO_START = pygame.image.load(r'Assets/Dino/DinoDead.png')

LARGE_CACTUS = [pygame.image.load(r'Assets/Cactus/LargeCactus1.png'),
                pygame.image.load(r'Assets/Cactus/LargeCactus2.png'),
                pygame.image.load(r'Assets/Cactus/LargeCactus2.png')]
SMALL_CACTUS = [pygame.image.load(r'Assets/Cactus/SmallCactus1.png'),
                pygame.image.load(r'Assets/Cactus/SmallCactus2.png'),
                pygame.image.load(r'Assets/Cactus/SmallCactus3.png')]
BIRD = [pygame.image.load(r'Assets/Bird/Bird1.png'),
        pygame.image.load(r'Assets/Bird/Bird1.png')]

CLOUD = pygame.image.load(r'Assets/Other/Cloud.png')

BACKGROUND = pygame.image.load(r'Assets/Other/Track.png')


class Cloud:
    def __init__(self):
        self.x_position = SCREEN_W +random.randint(800,1000)
        self.y_position = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.x_position,self.y_position))

    def update(self):
        self.x_position -= game_speed
        if self.x_position < -self.width:
            self.x_position = SCREEN_W + random.randint(2500, 3000)
            self.y = random.randint(50, 100)




class Dinosaur:
    x_position=80
    y_position = 310
    y_position_duck=340
    JUMP_V = 8.5

    def __init__(self):
        self.duck_images = DINO_DUCKING
        self.run_images = DINO_RUNNING
        self.jump_images = DINO_JUMPING

        #initial state of dino
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False
        self.is_falling_faster=False
        self.jump_velocity = self.JUMP_V
        self.step_index =0
        self.image = self.run_images[0]

        #draw a rectangle around dino for hitboxes
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position

    #function called every gameLoop iteration
    def update(self,user_input):
        '''function that is called every frame and handles the state of the dino '''
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()
        #for easier animations
        if self.step_index>=10:
            self.step_index=0


        #set the state based on input
        if user_input[pygame.K_UP] and not self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
            self.is_falling_faster = False
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
            self.is_falling_faster = False
        elif user_input[pygame.K_DOWN] and self.is_jumping:
            self.is_ducking = False
            self.is_running = False
            self.is_jumping = True
            self.is_falling_faster = True
        elif not (self.is_jumping or user_input[pygame.K_DOWN]):
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False
            self.is_falling_faster = False


    def run(self):

        '''
        handles the running of the dino
        :return:
        '''
        # step index to make animations slower, every 5 frames or so
        self.image = self.run_images[self.step_index//5]
        #updating the hitbox of the dino
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position
        self.step_index +=1

    def jump(self):
        if self.dino_rect.y<400:
            self.image = self.jump_images
            if(self.is_falling_faster):
                self.jump_velocity -= 1
            if self.is_jumping:
                self.dino_rect.y-=self.jump_velocity*2
                self.jump_velocity -=0.4
            #if self.dino_rect.y>=self.y_position:
            if self.jump_velocity< - self.JUMP_V:
                self.is_jumping=False
                self.jump_velocity = self.JUMP_V

    def duck(self):
        self.image = self.duck_images[self.step_index//5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position_duck
        self.step_index += 1

    def draw(self,SCREEN):
        ''' draws dino to the screen'''
        SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))


def main():
    global game_speed,x_position_background,y_position_background
    game_speed=7
    x_position_background=0
    y_position_background=380

    def background():
        global y_position_background,x_position_background
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND,(x_position_background,y_position_background))
        SCREEN.blit(BACKGROUND, (image_width+x_position_background, y_position_background))
        if(x_position_background < -image_width):
            SCREEN.blit(BACKGROUND, (image_width + x_position_background, y_position_background))
            x_position_background=0
        x_position_background -= game_speed




    run = True
    clock  = pygame.time.Clock()
    dino = Dinosaur()
    cloud=  Cloud()


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255,255,255))
        user_input = pygame.key.get_pressed()
        background()
        dino.draw(SCREEN)
        dino.update(user_input)
        cloud.draw(SCREEN)
        cloud.update()
        clock.tick(60)
        pygame.display.update()


if __name__ =='__main__':
    main()

