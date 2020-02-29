from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math

class smallbubble(object):
    def __init__(self,pos):
        self.img_url = "SmallBubble.png"
        self.row = 1
        self.column = 5
        self.img = simplegui.load_image(self.img_url)
        self.bdim = Vector(self.img.get_width(),self.img.get_height())
        self.adim = (self.bdim.x/self.column, self.bdim.y/self.row)
        self.center = Vector(self.adim[0]/2, self.adim[1]/2)
        self.pos = pos
        self.ratio = 0.01
        self.frame_index = [1,0]
        self.count = 0
    def draw_canvas(self,canvas):
        self.count += 1
        if self.count % 50 == 0:
            self.frame_index = self.next_frame()
        canvas.draw_image(self.img,(self.center.get_p()[0]*(2*self.frame_index[1]-1),self.center.get_p()[1]*(2*self.frame_index[0]-1)),self.adim,self.pos.get_p(),(self.adim[0]*self.ratio,self.adim[1]*self.ratio))
    def next_frame(self):
        if self.frame_index[1] > self.column:
            self.frame_index[0] += 1
            self.frame_index[1] = 1
        if self.frame_index[0] > self.row:
            self.frame_index = [1,0]
        self.frame_index[1] += 1
        return self.frame_index