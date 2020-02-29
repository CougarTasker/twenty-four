from hook import Hook
from fishline import Line
from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

class IT:
    def __init__(self):
        self.hook = Hook(Vector(250,250))
        self.line = Line(200,(251,100),2,self.hook)
        self.length = math.sqrt((self.line.begin[0]-self.line.end[0])*(self.line.begin[0]-self.line.end[0])+(self.line.begin[1]-self.line.end[1])*(self.line.begin[1]-self.line.end[1]))
    def draw(self,canvas):
        self.iteration()
        self.hook.update()
        self.hook.draw(canvas)
        self.line.draw_line(canvas)
    def addspeed(self):
        self.hook.vel = Vector(0,1)
    def subtractspeed(self):
        self.hook.vel = Vector(0,-1)
    def iteration(self):
        if self.length <= 20:
            self.addspeed()
        if self.length >= 100:
            self.subtractspeed()


it = IT()

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", 500, 500)

frame.set_draw_handler(it.draw)
# Start the frame animation
frame.start()
        