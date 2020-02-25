import random, math, os
from  vect import Vector
from keyboard import Keyboard 
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def polar(x,y,ang):
    pX = 40 * math.cos(ang * (math.pi / 180)) + x - 10
    pY = 40 * math.sin(ang * (math.pi / 180)) + y - 10
    return [round(pX),round(pY)]

class Rod:
    def __init__(self,player):
            addr = os.getcwd()
            self.hook = simplegui.load_image("file:///"+addr+"/images/hook.png")
            #self.radius = 50
            self.swing = True
            self.playerPos = player.getPos()
            self.pos = Vector()

    def draw(self,canvas,player,org):
        global ang, left, right

        if self.swing:
            org = True
            if ang == 180:
                left = True
                right = False
            elif ang == 0:
                left = False
                right = True

            if left:
                ang -= 2
            elif right:
                ang += 2

        position = Vector(player.getPos().x+100,player.getPos().y-10) + self.pos
        canvas.draw_line([player.getPos().x + 65, player.getPos().y- 70],polar(position.x, position.y, ang), 1, 'Black')

        source_centre = (self.hook.get_width() / 2, self.hook.get_height() / 2)
        source_size = (self.hook.get_width(), self.hook.get_height())
        dest_size = (50,50)
        position = Vector(player.getPos().x+105,player.getPos().y+12) + self.pos

        canvas.draw_image(self.hook,
                        source_centre,
                        source_size,
                        polar(position.x, position.y, ang),
                        dest_size)

ang = 0
left = False
right = True
#org = True
#hookRotate = 0
#kbd = Keyboard()

#addr = os.getcwd()
#rod = Rod("file:///"+addr+"/images/hook.png", "file:///"+addr+"/images/colouredBoth.png")



#inter = Interaction(rod, kbd)

#def draw(canvas):
    #inter.update()
    #rod.draw_handler(canvas)

#frame = simplegui.create_frame('Testing', 1980, 1080)
#frame.set_draw_handler(draw)
#frame.set_keydown_handler(kbd.keyDown)
#frame.set_keyup_handler(kbd.keyUp)
#frame.set_canvas_background("white")

#frame.start()
