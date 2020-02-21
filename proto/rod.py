import random, math, os
from  vect import Vector
from keyboard import Keyboard 
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def polar(x,y,ang):
    pX = radius * math.cos(ang * (math.pi / 180)) + x
    pY = radius * math.sin(ang * (math.pi / 180)) + y
    return [round(pX),round(pY)]

class Rod:
    def __init__(self,radius,hook_url, rod_url):
            self.hook = simplegui.load_image(hook_url)
            self.rod = simplegui.load_image(rod_url)
            self.radius = radius
            self.swing = True
            self.rodX = 300 #90 340
            self.rodY = 250	#140
            self.pos = Vector(self.rodX + 100,self.rodY + 10)

    def draw_handler(self,canvas):
        global ang, count, left, right, org, x, y

        x = self.rodX + 90
        y = self.rodY + 160

        if self.swing:
            org = True
            count += 1
            if ang == 180:
                left = True
                right = False
            elif ang == 0:
                left = False
                right = True

            if left:
                ang -= 1
            elif right:
                ang += 1

        source_centre = (self.rod.get_width() / 2, self.rod.get_height() / 2)
        source_size = (self.rod.get_width(), self.rod.get_height())
        dest_size = (200,200)

        canvas.draw_image(self.rod,
                        source_centre,
                        source_size,
                        (self.rodX,self.rodY),
                        dest_size)

        canvas.draw_line([self.rodX + 90, self.rodY - 90],polar(self.pos.x,self.pos.y, ang), 1, 'Black')

        source_centre = (self.hook.get_width() / 2, self.hook.get_height() / 2)
        source_size = (self.hook.get_width(), self.hook.get_height())
        dest_size = (100,100)

        canvas.draw_image(self.hook,
                        source_centre,
                        source_size,
                        polar(self.pos.x + 9, self.pos.y + 45, ang),
                        dest_size)


        print(ang)

class Interaction:
    def __init__(self, rod, keyboard):
        self.rod = rod
        self.keyboard = keyboard

    def update(self):
        global org
        if self.keyboard.down:
            self.rod.swing = False
            self.rod.pos.add(Vector(0,2))
            org = False
        elif self.keyboard.up:
            if self.rod.pos.y < 10 + self.rod.rodY:
                self.rod.swing = True
                org = True
            if not org:
                self.rod.pos.add(Vector(0,-2))

x = 0
y = 0
radius = 50
ang = 0
count = 0
left = False
right = True
org = True
hookRotate = 0
kbd = Keyboard()

addr = os.getcwd()
rod = Rod(radius, "file:///"+addr+"/images/hook.png", "file:///"+addr+"/images/colouredBoth.png")



inter = Interaction(rod, kbd)

def draw(canvas):
    inter.update()
    rod.draw_handler(canvas)

frame = simplegui.create_frame('Testing', 1980, 1080)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.set_canvas_background("white")

frame.start()
