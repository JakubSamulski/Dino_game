from typing import Sequence, Union

import pygame
import os
import pygame_textinput
import time
import sys
import mariadb
import random
from tkinter import *
from tkinter import messagebox
from pygame.surface import SurfaceType

from CustomTextbox import Textbox
from Button import Button

# Constants


pygame.init()
SCREEN_H = 729
SCREEN_W = 1280

SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# Loading assets
DINO_RUNNING = [pygame.image.load(r'Assets/Dino/DinoRun1.png'), pygame.image.load(r'Assets/Dino/DinoRun2.png')]
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
        pygame.image.load(r'Assets/Bird/Bird2.png')]

CLOUD = pygame.image.load(r'Assets/Other/Cloud.png')

BACKGROUND = pygame.image.load(r'Assets/Other/Track.png')
BACKGROUND_MENU = pygame.image.load(r'Assets/Other/main_menu_background.jpg')

# global parameters
global game_speed, increase_after_points, small_cactus_prob, large_cactus_prob, bird_prob, name,GAME_SPEED
small_cactus_prob = 0.33
large_cactus_prob = 0.33
bird_prob = 0.34
GAME_SPEED = 7
increase_after_points = 400
name = 'Guest'


class Cloud:
    def __init__(self):
        '''
            initializes cloud
            sets position and loads image
        '''
        self.x_position = SCREEN_W + random.randint(800, 1000)
        self.y_position = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
        self.y = None

    def draw(self, SCREEN: pygame.display) -> None:
        '''
        draws cloud to the SCREEN
        must be called every frame
        :param SCREEN: pygame display to draw to
        :return: None
        '''
        SCREEN.blit(self.image, (self.x_position, self.y_position))

    def update(self):
        """
        updates cloud position
        Should be called every frame
        :return None:
        """
        self.x_position -= game_speed
        if self.x_position < -self.width:
            self.x_position = SCREEN_W + random.randint(2500, 3000)
            self.y = random.randint(50, 100)


class Dinosaur:
    # class parameters

    x_position = 80
    y_position = 310
    y_position_duck = 340
    JUMP_V = 8.5

    def __init__(self)->None:
        #loading assets
        self.duck_images = DINO_DUCKING
        self.run_images = DINO_RUNNING
        self.jump_images = DINO_JUMPING

        # initial state of dino
        self.is_ducking = False
        self.is_running = True
        self.is_jumping = False
        self.is_falling_faster = False
        self.jump_velocity = self.JUMP_V
        self.step_index = 0
        self.image = self.run_images[0]

        # set a rectangle around dino for hitboxes
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position


    def update(self, user_input:Sequence[bool])->None:
        """
        Function that handles and updates the state of the dino. Must be called every frame
        :param user_input: result of pygame.key.get_pressed()
        :return: None
        """
        if self.is_ducking:
            self.duck()
        if self.is_running:
            self.run()
        if self.is_jumping:
            self.jump()
        # for animations not to be too quick
        if self.step_index >= 10:
            self.step_index = 0

        # set the state based on user input
        if user_input[pygame.K_UP] and not self.is_jumping and self.dino_rect.y >= 300:
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

    def run(self)-> None:

        '''
        Function to handle running of the dino
        :return None:
        '''
        # step index to make animations slower, every 5 frames or so
        self.image = self.run_images[self.step_index // 5]

        # updating the hitbox of the dino
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position
        self.step_index += 1

    def jump(self)->None:

        """
        Function to handle jumping of the dino
        :return: None
        """
        self.image = self.jump_images
        if (self.is_falling_faster):
            self.jump_velocity -= 1
        if self.is_jumping:
            self.dino_rect.y -= self.jump_velocity * 2
            self.jump_velocity -= 0.4

        # end of the jump
        if self.jump_velocity < - self.JUMP_V:
            self.is_jumping = False
            self.jump_velocity = self.JUMP_V

    def duck(self)->None:

        """
        Function that handles ducking of the dino
        :return:
        """
        #switch ducking image every 5 frames
        self.image = self.duck_images[self.step_index // 5]

        #update rectangle around the dino
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_position
        self.dino_rect.y = self.y_position_duck

        self.step_index += 1

    def draw(self, SCREEN:pygame.display)->None:
        """

        :param SCREEN:
        :return:
        """
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        pygame.draw.rect(SCREEN, (255, 0, 0), self.dino_rect, 2)


class Obstacle:
    def __init__(self, image: list[Union[pygame.Surface, SurfaceType]], type:int)->None:
        """
        initializes the obstacle
        :param image: list of images of the obstacle
        :param type: integer 0<=type<count of images
        """
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_W

    def update(self)-> None:
        """
        Function to update position of obstacle. Must be called every frame
        :return: None
        """
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN:pygame.display)-> None:
        """
        Function to draw obstacle to
        :param SCREEN:
        Display which to draw to
        :return:
         None
        """
        SCREEN.blit(self.image[self.type], self.rect)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN:pygame.display)->None:
        #need to override because its a animated obstacle
        if self.index >= 19:
            self.index = 0

        SCREEN.blit(self.image[self.index // 10], self.rect)
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)
        self.index += 1

def validate(gamespeed:str,increase_afer:str,prob1:str,prob2:str,prob3:str)->bool:
    try:
        gamespeed = int(gamespeed)
        increase_afer = int(increase_afer)
        prob1=int(prob1)
        prob2 = int(prob2)
        prob3 = int(prob3)
    except:
        return False
    return gamespeed>0 and increase_afer>0 and (prob1+prob2+prob3)==100




def write_scores(list,filename):
    s=""
    for elem in list:
        s+=f'{elem[0]},{elem[1]}\n'
    with open(filename,"w")as file:
        file.write(s)


def write_to_database(name,score):
    try:
        conn = mariadb.connect(
            user="root",
            password="kubasam",
            host="127.0.0.1",
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cur = conn.cursor()
    try:
        cur.execute("use Dino_Game")
    except mariadb.Error as e:
        cur.execute("CREATE DATABASE Dino_Game")
        cur.execute("use Dino_Game")
        cur.execute("CREATE TABLE leaderboard(id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,name VARCHAR(9),score INT(10) UNSIGNED NOT NULL)")
    cur.execute("INSERT INTO leaderboard(name,score) VALUES (?,?)", (name, score))
    conn.commit()
    conn.close()




def read_from_database(filename):
    # with open(filename) as file:
    #     data = file.read().split('\n')
    #     data.remove('')
    #     for i in range(len(data)):
    #         data[i] = data[i].split(',')
    #     return data
    data = []
    try:
        conn = mariadb.connect(
            user="root",
            password="kubasam",
            host="127.0.0.1",
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cur = conn.cursor()
    cur.execute("use Dino_Game")
    cur.execute("SELECT name,score FROM leaderboard ORDER BY score DESC")
    for (name, score) in cur:
        data.append((name,str(score)))
    conn.close()
    return data

def deathScreen():

    """
    Function to draw a death screen
    :return:-> None
    """

    global score, name
    write_to_database(name,score)
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render(f"You died with: {score} points", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_W // 2, 200)

    deadDino = DINO_DEAD
    deadDino_rotated = pygame.transform.rotate(DINO_DEAD, 180)

    main_menu_button = Button(SCREEN, 550, 570, 220, 75, "Play Again")
    print(name, score)
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(text, text_rect)
        SCREEN.blit(deadDino, (SCREEN_W // 2 - 100, 300))
        SCREEN.blit(deadDino_rotated, (SCREEN_W // 2, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if main_menu_button.is_clicked():
                mainMenu()

        main_menu_button.update()
        pygame.display.update()

#TODO napisać github pages jako wiki/manual do gry/opcji

# TODO uprzątnąć ten bajzel
def top_players()->None:


    """
    Function to draw leaderboard screen
    :return: None
    """
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render("Top Players", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_W // 2+20, 150)
    return_button = Button(SCREEN, 540, 570, 220, 75, "Return")

    data = read_from_database('Scores.txt')

    font_leaderboard = pygame.font.Font('freesansbold.ttf', 25)





    while True:


        SCREEN.fill((255, 255, 255))
        for i, l in enumerate(data):
            if(i>=10):
                break
            #print(l)
            name,score = l[0],l[1]
            SCREEN.blit(font_leaderboard.render(f'{i+1}.    '+name,True,(0,0,0)), (530, 220 + 25 * i))
            SCREEN.blit(font_leaderboard.render(score, True, (0, 0, 0)), (530+200, 220 + 25 * i))

        SCREEN.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if return_button.is_clicked():
            mainMenu()

        return_button.update()
        pygame.display.update()



def options():
    """
    function to draw and handle options screen
    :return:
    """

    global  increase_after_points, small_cactus_prob, large_cactus_prob, bird_prob,GAME_SPEED

    #initalize top label
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render("Options", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_W // 2, 200)

    #initialize return button
    return_button = Button(SCREEN, 550, 570, 220, 75, "Return")

    # TODO add validation

    # for changing game_speed parameter
    font = pygame.font.Font('freesansbold.ttf', 25)
    game_speed_textbox = Textbox(550, 300, 110, 25, str(GAME_SPEED))
    game_speed_label = font.render("Game speed: ", True, (0, 0, 0))
    game_speed_label_rect = game_speed_label.get_rect()
    game_speed_label_rect.center = (350, 312)

    # for changing speed_increase_after parameter
    speed_increase_textbox = Textbox(550, 350, 110, 25, str(increase_after_points))
    speed_increase_label = font.render("increase speed after points:", True, (0, 0, 0))
    speed_increase_label_rect = game_speed_label.get_rect()
    speed_increase_label_rect.center = (250, 362)

    # for changing small_cactus_prob parameter
    small_cactus_prob_textbox = Textbox(550, 400, 110, 25, str(int(small_cactus_prob * 100)))
    small_cactus_prob_label = font.render("Small cactus probability :", True, (0, 0, 0))
    small_cactus_prob_label_rect = small_cactus_prob_label.get_rect()
    small_cactus_prob_label_rect.center = (344, 412)

    # for large cactus_prob
    large_cactus_prob_textbox = Textbox(550, 450, 110, 25, str(int(large_cactus_prob * 100)))
    large_cactus_prob_label = font.render("large cactus probability :", True, (0, 0, 0))
    large_cactus_prob_label_rect = large_cactus_prob_label.get_rect()
    large_cactus_prob_label_rect.center = (344, 462)

    # for bird_prob
    bird_prob_textbox = Textbox(550, 500, 110, 25, str(int(bird_prob * 100)))
    bird_prob_label = font.render("bird probability :", True, (0, 0, 0))
    bird_prob_label_rect = bird_prob_label.get_rect()
    bird_prob_label_rect.center = (344, 512)


    #main loop
    while True:
        SCREEN.fill((255, 255, 255))
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if return_button.is_clicked():
           if validate(game_speed_textbox.value,speed_increase_textbox.value,small_cactus_prob_textbox.value,large_cactus_prob_textbox.value,bird_prob_textbox.value):
            #set parameters
                GAME_SPEED = int(game_speed_textbox.value)
                increase_after_points = int(speed_increase_textbox.value)
                small_cactus_prob = int(small_cactus_prob_textbox.value) / 100
                large_cactus_prob = int(large_cactus_prob_textbox.value) / 100
                bird_prob = int(bird_prob_textbox.value) / 100
                mainMenu()
           else:
                Tk().wm_withdraw()  # to hide the main window
                messagebox.showinfo('error'
                                    , 'make sure that all the settings are integers and that probabilities adds up to 100')

        #blit labels every frame
        SCREEN.blit(text, text_rect)
        SCREEN.blit(game_speed_label, game_speed_label_rect)
        SCREEN.blit(speed_increase_label, speed_increase_label_rect)
        SCREEN.blit(small_cactus_prob_label, small_cactus_prob_label_rect)
        SCREEN.blit(large_cactus_prob_label, large_cactus_prob_label_rect)
        SCREEN.blit(bird_prob_label, bird_prob_label_rect)

        # update all elements

        game_speed_textbox.update(events, SCREEN)
        speed_increase_textbox.update(events, SCREEN)
        small_cactus_prob_textbox.update(events, SCREEN)
        large_cactus_prob_textbox.update(events, SCREEN)
        bird_prob_textbox.update(events, SCREEN)
        return_button.update()
        pygame.display.update()


def mainMenu():


    """
    function to draw and handle main menu
    :return:
    """
    global name

    #initalize top label
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render("Main menu", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect = (550, 200)

    #initialize name text box
    name_text_box = Textbox(562, 250, 200, 25, 'type your name')
    if name != 'Guest':
        name_text_box.value = name
    name_text_box.set_border_color((255, 255, 255))

    #initialize buttons
    play_button = Button(SCREEN, 550, 330, 220, 75, "Play")
    top_players_button = Button(SCREEN, 550, 400, 220, 75, "Top Players")
    options_button = Button(SCREEN, 550, 470, 220, 75, "Options")

    #main loop
    while True:
        SCREEN.fill((255, 255, 255))
        SCREEN.blit(text, text_rect)
        events = pygame.event.get()

        #handle button clicks
        if play_button.is_clicked():
            if name_text_box.value == 'type your name':
                name = 'Guest'
            else:
                name = name_text_box.value
            main()
        if top_players_button.is_clicked():
            top_players()
        if options_button.is_clicked():
            options()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)


        # update all elements
        name_text_box.update(events, SCREEN)
        play_button.update()
        top_players_button.update()
        options_button.update()
        pygame.display.update()


def main():
    """
    main game function
    :return:
    """
    #initialize all variables
    global game_speed, x_position_background, y_position_background, score, obstacles, increase_after_points
    global small_cactus_prob, large_cactus_prob, bird_prob
    obstacles = []
    score = 0
    x_position_background = 0
    y_position_background = 380
    font = pygame.font.Font('freesansbold.ttf', 20)
    game_speed = GAME_SPEED

    def score_handler():
        """
        Function that handles counting score
        :return: None
        """

        global score, game_speed
        score += 1

        if score % increase_after_points == 0:
            game_speed += 1

        #update score label
        text = font.render(f'Points: {score}', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        SCREEN.blit(text, text_rect)



    def background():
        """
        Function to handle background of the game
        :return:
        """

        #initialize variables
        global y_position_background, x_position_background
        image_width = BACKGROUND.get_width()


        # blit two backgrounds in case one ends mid frame
        SCREEN.blit(BACKGROUND, (x_position_background, y_position_background))
        SCREEN.blit(BACKGROUND, (image_width + x_position_background, y_position_background))

        #background gets off screen
        if x_position_background < -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_position_background, y_position_background))
            x_position_background = 0
        x_position_background -= game_speed

    #initialize parameters
    run = True
    clock = pygame.time.Clock()
    dino = Dinosaur()
    cloud = Cloud()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
                run = False


        # draw stuff
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        dino.draw(SCREEN)
        dino.update(userInput)

        #handle obstacles generation
        if len(obstacles) == 0:
            population = [0, 1, 2]
            weights = [small_cactus_prob, large_cactus_prob, bird_prob]
            choice = random.choices(population, weights)[0]

            if choice == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif choice == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif choice == 2:
                obstacles.append(Bird(BIRD))
        #draw obstacles
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if dino.dino_rect.colliderect(obstacle.rect):
                deathScreen()

        #update all left elements
        background()
        cloud.draw(SCREEN)
        cloud.update()
        score_handler()

        #set frame rate
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    mainMenu()
