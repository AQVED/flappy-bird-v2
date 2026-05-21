from pygame import *
from random import *
import numpy #new 
import sounddevice as sd #new
init()

window_size = 1200,800
running = True
lose = False
FPS = 60

sr = 16000
block = 256
mic_level = 0.0
screen = display.set_mode(window_size)
clock = time.Clock()

class Bird:
    def __init__(self,x,y,img=None):
        self.x = x
        self.y = y
        self.img = img
        if self.img:
            self.rect = self.img.get_rect()
        else:
            self.rect = Rect(x,y,100,100)

    def move(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= 5
        if keys[K_DOWN]:
            self.rect.y += 5

    def update(self,screen):
        if self.img:
            screen.blit(self.img, (self.rect.x,self.rect.y))
        else:
            draw.rect(screen, 'yellow',self.rect)


class Tube:
    def __init__(self,x,y,width = 100, height = 800, img = None):
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.img = img
        if self.img:
            self.rect = self.img.get_rect()
        else:
            self.rect = Rect(self.x, self.y, self.width, self.height)
    
    def move(self):
        self.rect.x -= 8

    def update(self,screen):
        if self.img:
            screen.blit(self.img, (self.rect.x,self.rect.y))
        else:
            draw.rect(screen, 'yellow',self.rect)


def generete_tubes(count):
    xcor = 1200
    tubes = list()

    for i in range(count):
        ycor = randint(-600,-300)
        top_tube = Tube(xcor, ycor)
        bottom_tube = Tube(xcor,ycor + 800 + 250)
        tubes.extend([top_tube, bottom_tube])
        xcor += 600

    return tubes


def audio_cb(indata, frames,time,status ):
    global mic_level
    if status:
        return
    rms = float(numpy.sqrt(numpy.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

tubes = generete_tubes(150)

player = Bird(100,500)

y_vel = 0.0
gravity = 0.6
THRESH = 0.001
IMPULSE = -8.0

with sd.InputStream(samplerate=sr, channels=1, blocksize= block, callback=audio_cb):
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        
        screen.fill("skyblue")
        
        # player.move()

        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player.rect.y += int(y_vel)



        player.update(screen)
####
        for t in tubes:
            if not lose:
                t.move()
            t.update(screen)
            
            if t.rect.right < 0:
                tubes.remove(t)
                #score += 0.5
            
            if player.rect.colliderect(t.rect):
                lose = True
        
        if len(tubes) < 8:
            tubes += generete_tubes(150)
            


        display.flip()
        clock.tick(FPS)