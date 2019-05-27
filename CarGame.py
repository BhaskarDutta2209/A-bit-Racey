import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("Crash.wav")


display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("A bit Racey")

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
block_color = (53,115,255)
bright_red = (255,0,0)
bright_green = (0,255,0)

dodged = 0

clock = pygame.time.Clock()


carImg = pygame.image.load("racecar.png")
car_width = 73
car_height = 82

pause = True

def quitGame():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,i,a,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()   
        
    if(x+w > mouse[0] > x and y+h > mouse[1] > y):
        pygame.draw.rect(gameDisplay,a,(x,y,w,h))
        if click[0]==1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay,i,(x,y,w,h))
        
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf,textRect = text_objects(msg,smallText)
    textRect.center = ((x+w/2),(y+h/2))
    gameDisplay.blit(textSurf,textRect)
        
def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False

def crash_paused():
    global dodged
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
        
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        
        largeText = pygame.font.Font("freesansbold.ttf",115)
        TextSurf, TextReact = text_objects("Crashed",largeText) 
        TextReact.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf,TextReact)


        font = pygame.font.SysFont(None,45)
        text = font.render("Your Score:"+str(dodged),True,black)
        gameDisplay.blit(text,(345,350))
        
        button("Replay",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitGame)
           
        
        
        pygame.display.update()
        clock.tick(10)


def paused():
    pygame.mixer.music.pause()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font("freesansbold.ttf",115)
        TextSurf, TextReact = text_objects("Paused",largeText) 
        TextReact.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf,TextReact)
        
        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitGame)
           
        
        
        pygame.display.update()
        clock.tick(10)



def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font("freesansbold.ttf",115)
        TextSurf, TextReact = text_objects("A Bit Racey",largeText) 
        TextReact.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf,TextReact)
        
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitGame)
           
        
        
        pygame.display.update()
        clock.tick(10)

def things_dodge(count):
    font = pygame.font.SysFont(None,25)
    text = font.render("Dodged:"+str(count),True,black)
    gameDisplay.blit(text,(0,0))

def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))
    
def text_objects(text, font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf",115)
    TextSurf, TextReact = text_objects(text,largeText) 
    TextReact.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextReact)
    
    pygame.display.update()
    time.sleep(2)
    game_loop()
    
def crash():
    message_display("You Crashed")
    
def game_loop():
    pygame.mixer.music.load("My_Peeps.wav")
    pygame.mixer.music.play(-1)
    global pause
    gameExit = False
    x = (display_width*0.45)
    y = (display_height*0.8)
    x_change = 0
    
    thing_startx = random.randrange(0,display_width)
    thing_starty = -600
    thing_speed = 3
    thing_width = 100
    thing_height = 100
    global dodged
    dodged = 0
        
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        x+= x_change
                
        gameDisplay.fill(white)
        
        things(thing_startx,thing_starty,thing_width,thing_height,block_color)
        thing_starty += thing_speed
        car(x,y)
        things_dodge(dodged)
        
        if x>display_width-car_width or x<0:
            crash_paused()
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width-thing_width)
            dodged+=1
            thing_speed+=1
            
        if y < thing_starty+thing_height and y+car_height>thing_starty:

            if x>thing_startx and x<thing_startx+thing_width or x+car_width>thing_startx and x+car_width<thing_startx + thing_width:

                crash_paused()
        pygame.display.update()
        clock.tick(60)
game_intro()
game_loop()    
pygame.quit()
quit() 
