import pygame # open source module used to create games
from pygame import mixer # used for sound effects
from pygame.locals import *
import random

pygame.mixer.pre_init(44100, -16, 2, 512) # pre initialization of mixer (setting up few variables/condition value)
mixer.init() # initialization of mixer
pygame.init()

# define fps to limit the fps . Because for some device it will be too fast and for some too slow
clock = pygame.time.Clock()
fps = 60

# Game Window
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height)) # creates an untitled window
pygame.display.set_caption('Space Troopers') # windows top left prints space troopers

# define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# load sound
explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)

# define game variables
rows = 5
columns = 5
last_alien_shot = pygame.time.get_ticks()
alien_cooldown = 1000 # bullet cooldown in milliseconds
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0 # 0 is no game over, 1 means player has won, -1 means player has lost


# define colours(for the health bar and play and quit button)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# load image
bg = pygame.image.load("img/bg.png")    # background image loaded

def draw_bg():
    '''
    Function to draw the background
    '''
    screen.blit(bg, (0, 0))  # blit() is used to when we want to put an image on to the screen

# defining function to create image from text(because in pygame we cant directly add text we have to convert it into an image)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) # converting text to image
    screen.blit(img, (x, y)) # image created added to the screen

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
        game_over = 0

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
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top) # creates a new bullet and put it at the coordinates
            Bullets_group.add(bullet) # and add it to the group.
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)  # this will remove the transparent rectangle behind the image and only when the bullet will hit the spaceship body only then the health will reduce

        # draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+2), self.rect.width, 8))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom+2), int(self.rect.width * (self.health_remaining/self.health_start)), 8))
            # 'int(self.rect.width * (self.health_remaining/self.health_start))' will adjust the green health bar according to health remaining
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over



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
            self.kill() # kills the bullet also when there is a collison btw alien and bullet
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


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
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask): # False = we dnt want the spaceship to get destroyed completely in just one bullet
            explosion2_fx.play()
            self.kill()
            # reduce spaceship health
            spaceship.health_remaining -= 1 # using spaceship object we are reducing health
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# create explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))

            # add the image to the list
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images)-1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete delete the explosion.
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

# create sprite groups
spaceship_group = pygame.sprite.Group()
Bullets_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
aliens_bullets_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

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

    if countdown == 0:
        # create random alien bullets
        # record current time
        time_now = pygame.time.get_ticks()

        # shoot
        if time_now - last_alien_shot > alien_cooldown and len(aliens_bullets_group) < 5 and len(aliens_group) > 0:
            attacking_alien = random.choice(aliens_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            aliens_bullets_group.add(alien_bullet)
            last_alien_shot = time_now

        # check if all the aliens has been killed
        if len(aliens_group) == 0:
            game_over = 1

        if game_over == 0:  # if the game is not over
            # update spaceship
            game_over = spaceship.update()  # if spaceship is destroyed agme_over == -1

            # update sprite groups
            Bullets_group.update()
            aliens_group.update()
            aliens_bullets_group.update()
        else:
            if game_over == -1:
                draw_text("GAME OVER", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text("YOU WIN", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

    if countdown > 0:
        draw_text("GET READY", font40, white, int(screen_width/2 - 110), int(screen_height/2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width/2 - 10), int(screen_height/2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    # update explosion group
    explosion_group.update()

    # draw sprite group
    spaceship_group.draw(screen)
    Bullets_group.draw(screen)
    aliens_group.draw(screen)
    aliens_bullets_group.draw(screen)
    explosion_group.draw(screen)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # cross 'x' button on top right when clicked game terminates
            run = False     # condition becomes false and gets out of loop and game stops

    pygame.display.update()  # for automatic background updation we use it

pygame.quit()







