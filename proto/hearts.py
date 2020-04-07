try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from vect import Vector
from snd import Snd

##class to draw the hearts onto the screen for the player lives
class Hearts:
    def __init__(self,dimensions,time,die):
        self.die = die
        #die attribute references overlay class to allow state to be changed to gameover 

        self.canvas_dim = dimensions
        addr = os.getcwd()
        self.time = time
        
        self.img_full = simplegui.load_image("file:///"+addr+"/images/fullheart.png")
        self.img_empty = simplegui.load_image("file:///"+addr+"/images/emptyheart.png")

        #image info so both empty heart/full heart images are drawn same size
        self.dim = (51,42)
        self.size = 0.65
        self.cen = (self.dim[0]/2, self.dim[1]/2)
        self.draw_dim = (self.dim[0]*self.size, self.dim[1]*self.size)
        self.pading = 5
        self.pos = Vector(self.dim[0]*self.size/2, self.dim[1]*self.size/2)
        self.offset = Vector(self.draw_dim[0],0)
        
        #user lives in game is 3
        self.lives_max = 3
        self.lives = self.lives_max
        self.sound = Snd(self.time,"bite2.ogg")

    #method called when user restarts game 
    def resetLives(self):
        self.lives = self.lives_max

    def getLives(self):
        return self.lives

    #when shark caught user loses life
    def loseLife(self):
        self.sound.play() #shark 'chomp' sound
        self.lives -= 1 
        if self.lives <= 0:
            self.die.gameOver()
        #when user reaches zero self.die.gameover calls the method in overlay to change to gameover state


    #methods for drawing hearts to screen
    def draw(self,canvas):
        #prevents negative lives
        if self.lives < 0:
            self.lives = 0
        #draws full then empty hearts dependant on lives
        for i in range(0,self.lives):
            self.drawheart(canvas, self.img_full, i)
        for i in range(self.lives, self.lives_max):
            self.drawheart(canvas, self.img_empty,i)

    def drawheart(self,canvas,img,i):
        canvas.draw_image(img, self.cen, self.dim, (self.pos+Vector(self.pading,self.pading)+self.offset*i).get_p(),self.draw_dim)
        
        
