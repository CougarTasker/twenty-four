from vect import Vector
from snd import Snd
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#class used to manage player score 
class Score:
    def __init__(self,time,dim,die,frame):
        self.score = 0
        self.time = time
        self.maxtime = 99.999
        self.starttime = self.time.time()
        self.scoreh = 30
        self.timeh = 20
        self.padding = 5
        self.size = Vector(frame.get_canvas_textwidth("Score: "+'{:04d}'.format(self.score), self.scoreh,"sans-serif")+self.padding*2,self.padding*2+self.scoreh+self.timeh)
        self.pos = Vector(((Vector(dim[0],dim[1]) - self.size)/2).x,0)

        #reference to overlay class for if game ends
        self.die = die
        self.sound = Snd(self.time,"point.ogg",0.5)
        
    def timeleft(self):
        t = self.maxtime - (self.time.time() - self.starttime)
        #checks if any time left and otherwise sets time to zero to avoid negative
        if t <= 0:
            t = 0
            self.die.gameOver()
         #when timer reaches zero self.die.gameover calls the method in overlay to change to gameover state

        #return time left to user
        return t

    #set score to zero when user restarts
    def resetScore(self):
        self.score = 0

    #score goes up when fish caught 
    def incScore(self,score):
        self.sound.play()
        self.score+= score

    #draw score and time to screen
    def draw(self,canvas):
        canvas.draw_polygon((self.pos.get_p(),(self.pos+self.size.x*Vector(1,0)).get_p(),(self.pos+self.size).get_p(),(self.pos+self.size.y*Vector(0,1)).get_p()),1,"rgba(255,255,255,0)","rgba(50,50,50,0.7)")
        canvas.draw_text("Score: "+'{:04d}'.format(self.score), (self.pos+Vector(self.padding,self.scoreh)).get_p(), self.scoreh, "orange","sans-serif")
        canvas.draw_text("Time: "+'{:02.3f}'.format(self.timeleft()), (self.pos+Vector(self.padding,self.scoreh+self.padding+self.timeh)).get_p(), 25, "yellow","sans-serif")
