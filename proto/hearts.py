try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from vect import Vector

##class to draw the hearts onto the screen for the player lives

class Hearts:
    def __init__(self,dimensions,time,die):
        self.die = die
        self.canvas_dim = dimensions
        addr = os.getcwd()
        self.time = time
        self.img_full = simplegui.load_image("file:///"+addr+"/images/fullheart.png")
        self.img_empty = simplegui.load_image("file:///"+addr+"/images/emptyheart.png")
        self.dim = (51,42)
        self.size = 0.65
        self.cen = (self.dim[0]/2, self.dim[1]/2)
        self.draw_dim = (self.dim[0]*self.size, self.dim[1]*self.size)
        self.pading = 5
        self.pos = Vector(self.dim[0]*self.size/2, self.dim[1]*self.size/2)
        self.offset = Vector(self.draw_dim[0],0)
        self.lives_max = 3
        self.lives = self.lives_max
        self.sound = simplegui.load_sound("file:///"+addr+"/sounds/bite2.ogg")
    def resetLives(self):
        self.lives = self.lives_max
    def getLives(self):
        return self.lives
    def loseLife(self):
        self.sound.play()
        self.lives -= 1 
        if self.lives <= 0:
            self.die.gameOver()
    def getHeight(self):
        return self.draw_dim[1] + self.pading*2
    def getWidth(self):
        return self.draw_dim[0]*self.lives_max + self.pading*2
    def draw(self,canvas):
        if self.lives < 0:
            self.lives = 0
        for i in range(0,self.lives):
            self.drawheart(canvas, self.img_full, i)
        for i in range(self.lives, self.lives_max):
            self.drawheart(canvas, self.img_empty,i)
    def drawheart(self,canvas,img,i):
        canvas.draw_image(img, self.cen, self.dim, (self.pos+Vector(self.pading,self.pading)+self.offset*i).get_p(),self.draw_dim)
        
        
