import pygame
import os
pygame.init()

#Constants

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


class Dinosaur:
    x_position=80
    y_position = 310
    def __init__(self):
        self.duck_images = DINO_DUCKING
        self.run_images = DINO_RUNNING
        self.jump_images = DINO_JUMPING

        #initial state of dino
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False

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
        elif user_input[pygame.K_DOWN] and not self.is_jumping:
            self.is_ducking = True
            self.is_running = False
            self.is_jumping = False
        elif not (self.is_jumping or user_input[pygame.K_DOWN]):
            self.is_ducking = False
            self.is_running = True
            self.is_jumping = False


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
        pass
    def duck(self):
        pass
    def draw(self,SCREEN):
        ''' draws dino to the screen'''
        SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))

def main():
    run = True
    clock  = pygame.time.Clock()
    dino = Dinosaur()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255,255,255))
        user_input = pygame.key.get_pressed()

        dino.draw(SCREEN)
        dino.update(user_input)
        clock.tick(30)
        pygame.display.update()


if __name__ =='__main__':
    main()

