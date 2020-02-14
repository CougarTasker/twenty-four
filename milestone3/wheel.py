from vect import Vector
import random,math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500
scroll = Vector(0,0)
class Image:
    def __init__(self,wheel):
        self.img = simplegui.load_image("file:///C:/Users/Couga/Documents/repos/twenty-four/milestone3/coach_wheel-512.png")
        self.cen = (256, 256)
        self.dim = (512, 512)
        self.rot = 0
        self.wheel = wheel
    def draw(self,canvas):
        canvas.draw_image(self.img, self.cen, self.dim, self.wheel.pos.tuple(),(self.wheel.radius*2,self.wheel.radius*2), self.wheel.rot)
        canvas.draw_image(self.img, self.cen, self.dim, (self.wheel.pos+Vector(WIDTH,0)).tuple(),(self.wheel.radius*2,self.wheel.radius*2), self.wheel.rot)
        canvas.draw_image(self.img, self.cen, self.dim, (self.wheel.pos+Vector(-WIDTH,0)).tuple(),(self.wheel.radius*2,self.wheel.radius*2), self.wheel.rot)

class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'
        self.rot = 0
        self.on_ground = True

    def draw(self, canvas):
        Image(self).draw(canvas)

    def jump(self):
        if self.on_ground:
            self.vel.add(Vector(0,-40))
            self.on_ground = False
    def update(self):
        global scroll
        self.pos.add(self.vel)
        scroll.add(self.vel)
        self.vel.x *= 0.85
        self.rot = self.pos.x/(self.radius)
        if self.pos.x<0:
            self.pos.add(Vector(WIDTH,0))
        elif self.pos.x>WIDTH:
            self.pos.add(Vector(-WIDTH,0))
        if not self.on_ground:
            self.vel.add(Vector(0,2))
            if self.pos.y+self.radius>HEIGHT:
                self.pos.y = HEIGHT-self.radius
                self.vel.y *= -0.6
                if self.vel.length()<10:
                    self.on_ground =True
                    self.vel.y =0
class Background:
    def __init__(self,factor):
        self.img = simplegui.load_image("file:///C:/Users/Couga/Documents/repos/twenty-four/milestone3/background_clouds.png")
        self.cen = (1200,150)
        self.dim = (2400, 300)
        self.factor = factor
        self.o = random.random()*2400
    def draw(self,canvas):
        offset = scroll.x*self.factor +self.o
        while offset<0:
            offset+=self.dim[0]
        while offset >= self.dim[0]:
            offset-=self.dim[0]
        canvas.draw_image(self.img, self.cen, self.dim, (self.cen[0]-offset,HEIGHT/4),(self.dim[0],HEIGHT/2))
        canvas.draw_image(self.img, self.cen, self.dim, (self.cen[0]-offset-self.dim[0],HEIGHT/4),(self.dim[0],HEIGHT/2))
        canvas.draw_image(self.img, self.cen, self.dim, (self.cen[0]-offset+self.dim[0],HEIGHT/4),(self.dim[0],HEIGHT/2))

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False

class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1,0))
        if self.keyboard.up:
           self.wheel.jump()

kbd = Keyboard()
wheel = Wheel(Vector(WIDTH/2, HEIGHT-40), 40)
inter = Interaction(wheel, kbd)
backa = Background(0.5)
backb = Background(0.7)
backc = Background(0.9)
def draw(canvas):
    inter.update()
    wheel.update()
    backa.draw(canvas)
    backb.draw(canvas)
    backc.draw(canvas)
    wheel.draw(canvas)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_canvas_background("blue")
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
