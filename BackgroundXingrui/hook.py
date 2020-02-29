from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

class Hook:
    def __init__(self,pos):
        self.pos = pos
        self.url = "https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/Fishing%20hook.jpeg"
        self.img = simplegui.load_image(self.url)
        self.ratio = 1/46
        self.vel = Vector()
        #self.ang = 0
    def draw(self,canvas):
        canvas.draw_image(self.img,(460/2,758/2),(459,757),self.pos.get_p(),(10,17))
    def update(self):
        self.pos.add(self.vel)
    #def status(self,boat):#You need to justice the boat speed
        #return boat.vel == Vector()
    #def swing(self,boat):
        #if not self.status(boat):
            