import pygame
import random
import time
import sys

pygame.init()
display_width=700
display_height=600

crash_music = pygame.mixer.Sound("E:/Python/Car Race/music/Red-Screen-Sound.ogg")

black=(0,0,0)
white=(255,255,255)
red=(200,0,0)
bright_red=(255,0,0)
yellow=(255, 216, 0)
blue=(0, 0, 255)
green=(0, 200, 0)
bright_green=(0,255,0)
orange=(255, 118, 0)

def score(counter):
    font= pygame.font.SysFont(None, 25)
    text= font.render("score: " + str(counter), True, orange)
    gameDisplay.blit(text, (0, 0))

gameDisplay= pygame.display.set_mode((display_width,display_height))

def text_object(text, font, color):
    Text_surfase= font.render (text, True, color)
    return Text_surfase, Text_surfase.get_rect()
        

pygame.display.set_caption("Race Car")

clock=pygame.time.Clock()

carImg=pygame.image.load("E:/Python/Car Race/picture/Car.png")

car_width = carImg.get_width()
car_height = carImg.get_height()

def button(massage, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h), border_radius=10)
        if click[0] == 1 and action is not None:
            if action == "Play!":
                game_loop()
            elif action == "Quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h), border_radius=10) 

    pygame.draw.rect(gameDisplay, black, (x, y, w, h), 3, border_radius=10)

    smalltext = pygame.font.Font("freesansbold.ttf", 20)  
    textSurf, textRect = text_object(massage, smalltext, black)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)  

def game_intro():
    intro = True

    pygame.mixer.music.load("E:/Python/Car Race/music/Crash.ogg")
    pygame.mixer.music.play(-1,0.0)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.fill(white)
        largetext= pygame.font.Font("freesansbold.ttf", 65)
        Text_surf , Text_rect= text_object("Let's Play Game", largetext, black)
        Text_rect . center=( (display_width/2), (display_height/2))
        gameDisplay.blit(Text_surf, Text_rect)
        button("Play!", 150,450 ,100,50 , green,bright_green ,"Play!")
        button("Quit", 450,450 ,100,50 , red,bright_red ,"Quit")

        pygame.display.update()

def stuff (stuff_x,stuff_y,stuff_w,stuff_h,color):
    pygame.draw.rect(gameDisplay, color, [stuff_x,stuff_y,stuff_w,stuff_h])

def game_loop():

    pygame.mixer.music.stop()

    x=(display_width * 0.42)
    y=(display_height * 0.7)

    pygame.mixer.music.load("E:/Python/Car Race/music/Sergios Magic Dustbin.ogg")
    pygame.mixer.music.play(-1,0.0)
    
    x_change = 0

    def car(x,y):
        gameDisplay.blit(carImg,(x,y))
        
    def massage_display(text):
        largetext= pygame.font.Font("freesansbold.ttf", 80)
        Text_surf , Text_rect= text_object( text, largetext, black)
        Text_rect . center=( (display_width/2), (display_height/2))
        gameDisplay.blit(Text_surf, Text_rect)
        pygame.display.update()

        time.sleep(2)
        game_loop()
        
    def lose():
        pygame.mixer.music.stop()
        crash_music.play()
        
        largetext= pygame.font.Font("freesansbold.ttf", 80)
        Text_surf , Text_rect= text_object( "You a LOSER", largetext, black)
        Text_rect . center=( (display_width/2), (display_height/4))
        gameDisplay.blit(Text_surf, Text_rect)

        score_text = "Your Score: " + str(counter)
        score_font = pygame.font.SysFont("freesansbold.ttf", 50)
        Score_surf, Score_rect = text_object(score_text, score_font, orange)
        Score_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(Score_surf, Score_rect)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
            button("Try again", 150,450 ,100,50 , green,bright_green ,"Play!")
            button("Quit", 450,450 ,100,50 , red,bright_red ,"Quit")
            pygame.display.update()
            

    stuff_start_x = random.randrange (0,display_width)
    stuff_start_y = -600
    stuff_speed = 6
    stuff_width = 70
    stuff_height = 70

    counter = 0

    crashed=False

    start_time = time.time()
    while not crashed :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed= True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            #print(event)
        
        x = x + x_change
        
        if x <= 0:
            x = 0
        elif x >= display_width - car_width:
            x = display_width - car_width

        elapsed_time = time.time() - start_time
        speed_incrase = 1 + (elapsed_time / 10)
        stuff_speed = 6 * speed_incrase
                
        gameDisplay.fill(white)

        stuff ( stuff_start_x, stuff_start_y, stuff_width, stuff_height,blue)
        stuff_start_y = stuff_start_y + stuff_speed

        if stuff_start_y > display_height:
            stuff_start_y = 0 - stuff_height
            stuff_start_x = random.randrange(0, display_width)

            counter = counter + 1

        if y < stuff_start_y + stuff_height:
            if x > stuff_start_x and x < stuff_start_x + stuff_width or x + car_width > stuff_start_x and x + car_width <  stuff_start_x + stuff_width:
                lose()

        car(x,y)
        score(counter)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
game_intro()
game_loop()
