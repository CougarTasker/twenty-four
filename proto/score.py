from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
class Score:
    def __init__(self,time,dim,die,frame):
        self.score = 0
        self.time = time
        self.maxtime = 99
        self.starttime = self.time.time()
        self.scoreh = 30
        self.timeh = 20
        self.padding = 5
        self.size = Vector(frame.get_canvas_textwidth("Score: "+'{:04d}'.format(self.score), self.scoreh,"sans-serif")+self.padding*2,self.padding*2+self.scoreh+self.timeh)
        self.pos = Vector(((Vector(dim[0],dim[1]) - self.size)/2).x,0)
        self.die = die
        addr = os.getcwd()
        self.sound = simplegui.load_sound("file:///"+addr+"/sounds/point.ogg")
        self.sound.set_volume(0.5)
        
    def timeleft(self):
        t = self.maxtime - (self.time.time() - self.starttime)
        if t <= 0:
            t = 0
            self.die.gameOver()
        return t
    def resetScore(self):
        self.score = 0
    def incScore(self,score):
        self.sound.play()
        self.score+= score
    def draw(self,canvas):
        canvas.draw_polygon((self.pos.get_p(),(self.pos+self.size.x*Vector(1,0)).get_p(),(self.pos+self.size).get_p(),(self.pos+self.size.y*Vector(0,1)).get_p()),1,"rgba(255,255,255,0)","rgba(50,50,50,0.7)")
        canvas.draw_text("Score: "+'{:04d}'.format(self.score), (self.pos+Vector(self.padding,self.scoreh)).get_p(), self.scoreh, "orange","sans-serif")
        canvas.draw_text("Time: "+'{:02.3f}'.format(self.timeleft()), (self.pos+Vector(self.padding,self.scoreh+self.padding+self.timeh)).get_p(), 25, "yellow","sans-serif")
