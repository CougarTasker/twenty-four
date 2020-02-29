from vect import Vector
from hook import Hook
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math


class Line:
    def __init__(self,max_length,begin, width,hook):
        self.max_length = max_length
        self.begin = begin
        self.width = width
        self.hook = hook
        self.end = (self.hook.pos.get_p()[0]+110*self.hook.ratio, self.hook.pos.get_p()[1]-787/2*self.hook.ratio)
        self.color = 'Black'
        self.static = True
        self.catchfish = False
    def draw_line(self,canvas):
        canvas.draw_line(self.begin,self.end,self.width,self.color)
