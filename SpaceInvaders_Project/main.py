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

# define game variables
rows = 5
columns = 5
last_alien_shot = pygame.time.get_ticks()
alien_cooldown = 1000 # bullet cooldown in milliseconds


# define colours(for the health bar)
red = (255, 0, 0)
green = (0, 255, 0)

# load image
bg = pygame.image.load("img/bg.png")    # background image loaded

def draw_bg():
    '''
    Function to draw the background
    '''
    screen.blit(bg, (0, 0))  # blit() is used to when we want to put an image on to the screen

# create spaceship class
class Spaceship(pygame.sprite.Sprite):  # child class of Sprite class
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)  # Here we are inheriting the functionality of pygame Sprite class within our spaceship class
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()  # converting image into rectangle
        self.rect.center = [x, y]  # midpoint if rect object will be x, y
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks() # it will be used check when the bullet was initiated

    def update(self):  # overriding Sprite method of Sprite class
        # set movement speed
        speed = 8
        # set a cooldown variable
        cooldown = 100 # milliseconds

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0: # it will move upto the screen left width only
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width: # it will move upto the right width of screen
            self.rect.x += speed

        # record current time
        time_now = pygame.time.get_ticks()

        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:  # if space key is pressed
            bullet = Bullets(self.rect.centerx, self.rect.top) # creates a new bullet and put it at the coordinates
            Bullets_group.add(bullet) # and add it to the group.
            self.last_shot = time_now

        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+2), self.rect.width, 8))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom+2), int(self.rect.width * (self.health_remaining/self.health_start)), 8))
            # 'int(self.rect.width * (self.health_remaining/self.health_start))' will adjust the green health bar according to health remaining

# creating bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5  # it will keep moving the bullets after creation of it by pressing spacebar
        if self.rect.bottom < 50:  # kills the bullets after bullet bottom  reaching 50 pixels below the top
            self.kill()
        if pygame.sprite.spritecollide(self, aliens_group, True): # it is an inbuilt function to detect collision
            self.kill() 

# create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        '''
        for the left right movement of aliens
        '''
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

# creating alien bullet class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2  # it will keep moving the bullets after creation of it by pressing spacebar
        if self.rect.top > screen_height:  # kills the bullets after bullet bottom  reaching 50 pixels below the top
            self.kill()


# create sprite groups
spaceship_group = pygame.sprite.Group()
Bullets_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
aliens_bullets_group = pygame.sprite.Group()

def create_alien():
    '''
    generate aliens
    '''
    for row in range(rows):
        for item in range(columns):
            alien = Aliens(100 + item*100, 50 + row * 50)  # x, y axis defined
            aliens_group.add(alien)

create_alien()



# create player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3) # last arguent '3' define how many times the player can be hit.
spaceship_group.add(spaceship)

# creating game loop
run = True # game condition
while run: # till its true the game will continue to run

    clock.tick(fps)  # limiting the fps

    #draw background
    draw_bg() # it will add background to the screen but it doesnt update the screen automatically

    # create random alien bullets
    # record current time
    time_now = pygame.time.get_ticks()

    # shoot
    if time_now - last_alien_shot > alien_cooldown and len(aliens_bullets_group) < 5 and len(aliens_group) > 0: #
        attacking_alien = random.choice(aliens_group.sprites())
        alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
        aliens_bullets_group.add(alien_bullet)
        last_alien_shot = time_now

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # cross 'x' button on top right when clicked game terminates
            run = False     # condition becomes false and gets out of loop and game stops

    # update spaceship
    spaceship.update()

    # update sprite groups
    Bullets_group.update()
    aliens_group.update()
    aliens_bullets_group.update()

    # draw sprite group
    spaceship_group.draw(screen)
    Bullets_group.draw(screen)
    aliens_group.draw(screen)
    aliens_bullets_group.draw(screen)

    pygame.display.update()  # for automatic background updation we use it

pygame.quit()

# explosion_fx = pygame.mixer.Sound("img/explosion.wav")
# explosion_fx.set_volume(0.25)
#
# explosion2_fx = pygame.mixer.Sound('img/explosion2.wav')



