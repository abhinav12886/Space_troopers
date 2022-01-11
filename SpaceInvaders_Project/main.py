import pygame # open source module used to create games
from pygame import mixer
from pygame.locals import *
import random

# pygame.mixer.pre_init(44100, -16, 2, 512)
# mixer.init()
# pygame.init()

# define fps to limit the fps . Because for some device it will be too fast and for some too slow
clock = pygame.time.Clock()
fps = 60

# Game Window
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height)) # creates an untitled window
pygame.display.set_caption('Space Troopers') # windows top left prints space troopers

# load image
bg = pygame.image.load("img/bg.png")    # background image loaded

def draw_bg():
    '''
    Function to draw the background
    '''
    screen.blit(bg, (0, 0))  # blit() is used to when we want to put an image on to the screen

# create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # Here we are inheriting the functionality of pygame Sprite class within our spaceship class
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()  # converting image into rectangle
        self.rect.center = [x, y]  # midpoint if rect object will be x, y

# create sprite groups
spaceship_group = pygame.sprite.Group()

# create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100)
spaceship_group.add(spaceship)

# creating game loop
run = True # game condition
while run: # till its true the game will continue to run

    clock.tick(fps)  # limiting the fps

    #draw background
    draw_bg() # it will add background to the screen but it doesnt update the screen automatically

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # cross 'x' button on top right when clicked game terminates
            run = False     # condition becomes false and gets out of loop and game stops

    # draw sprite group
    spaceship_group.draw(screen)
     
    pygame.display.update()  # for automatic background updation we use it

pygame.quit()

# explosion_fx = pygame.mixer.Sound("img/explosion.wav")
# explosion_fx.set_volume(0.25)
#
# explosion2_fx = pygame.mixer.Sound('img/explosion2.wav')



