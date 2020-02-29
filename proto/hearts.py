try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from vect import Vector

##class to draw the hearts onto the screen for the player lives

class Hearts:
        def __init__(self, dimensions):
                self.canvas_dim = dimensions
                addr = os.getcwd()

                self.img_full = simplegui.load_image("file:///"+addr+"/images/fullheart.png")
                self.img_empty = simplegui.load_image("file:///"+addr+"/images/emptyheart.png")
                self.dim = (51,42)
                self.cen = (self.dim[0]/2, self.dim[1]/2)
                self.draw_dim = (self.dim[0]/2, self.dim[1]/2)
                self.pos = Vector(self.dim[0]/2, self.dim[1]/2)
                self.offset = 25

        def update(self,canvas, player):
                lives = player.getLives()
                for i in range(0,lives):
                        self.draw(canvas, self.img_full, self.offset*i)
                for i in range(0, 3-lives):
                        self.draw(canvas, self.img_empty, self.offset *(2-i))

        def draw(self,canvas, img, offset):
                canvas.draw_image(img, self.cen, self.dim, (self.pos.get_p()[0] +offset,self.pos.get_p()[1]),self.draw_dim)
                
                
