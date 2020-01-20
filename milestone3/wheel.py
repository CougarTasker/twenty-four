from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500

class Image:
    def init(url,dimentions,size,framecount)                
class Wheel:
    def __init__(self, pos, radius=10):
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        canvas.draw_circle((self.pos+Vector(WIDTH,0)).get_p(), self.radius, 1, self.colour, self.colour)
        canvas.draw_circle((self.pos+Vector(-WIDTH,0)).get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        if self.pos.x<0:
            self.pos.add(Vector(WIDTH,0))
        elif self.pos.x>WIDTH:
            self.pos.add(Vector(-WIDTH,0))
    
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False

class Interaction:
    def __init__(self, wheel, keyboard):
        self.wheel = wheel
        self.keyboard = keyboard

    def update(self):
        if self.keyboard.right:
            self.wheel.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.wheel.vel.add(Vector(-1,0))

kbd = Keyboard()
wheel = Wheel(Vector(WIDTH/2, HEIGHT-40), 40)
inter = Interaction(wheel, kbd)

def draw(canvas):
    inter.update()
    wheel.update()
    wheel.draw(canvas)

frame = simplegui.create_frame('Interactions', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
