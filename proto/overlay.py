try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from enum import Enum
import os
from spritesheet import SpriteSheet as SS
from vect import Vector
class Overlay:
    def __init__(self,kbd,inter,dimensions,frame):
        self.frame = frame
        self.dimensions = dimensions
        self.kbd = kbd
        self.inter = inter
        self.state = State.START
        self.pressSpace = SS("file:///"+os.getcwd()+"/images/press_space.png",(1,8),time=800,scale=1,pos=Vector(dimensions[0]/2,dimensions[1]*0.8),looping=False)
    def gameover(self):
        self.state = State.GAMEOVER
        self.inter.time.pause()
    def checkKbd(self):
        if self.state == State.START:
            if self.kbd.space:
                self.state = State.PLAYING
                self.inter.start()
                self.inter.time.play()
                self.kbd.space = False
        if self.state == State.PLAYING:
            if self.kbd.p:
                self.state = State.PAUSED
                self.inter.time.pause()
                self.kbd.p = False
        if self.state == State.PAUSED:
            if self.kbd.p:
                self.state = State.PLAYING
                self.inter.time.play()
                self.kbd.p = False
        if self.state == State.GAMEOVER:
            if self.kbd.space:
                self.state = State.PLAYING
                self.inter.start()
                self.inter.time.play()
                self.kbd.space = False
    def centerString(self,canvas,text):
        w = self.frame.get_canvas_textwidth(text, 30)
        canvas.draw_text(text, ((self.dimensions[0]-w)/2,self.dimensions[1]*0.8), 30, "red")
    def pausescreen(self,canvas):
        addr = os.getcwd()
        img = simplegui.load_image("file:///"+addr+"/images/pause.png")
        source_centre = (img.get_width() / 2, img.get_height() / 2)
        source_size = (img.get_width(), img.get_height())
        dest_size = (300,300)
        dest_centre = (500,300)
        canvas.draw_image(img,
            source_centre,
            source_size,
            dest_centre,
            dest_size)
    def draw(self,canvas):
        self.checkKbd()
        if self.state == State.START:
            self.centerString(canvas,"press space to start")
        if self.state == State.PLAYING:
            self.centerString(canvas,"press p to pause")
        if self.state == State.PAUSED:
            self.pausescreen(canvas)
            self.centerString(canvas,"press p to play")
        if self.state == State.GAMEOVER:
            addr = os.getcwd()
            img = simplegui.load_image("file:///"+addr+"/images/game_over.png")
            source_centre = (img.get_width() / 2, img.get_height() / 2)
            source_size = (img.get_width(), img.get_height())
            dest_size = (500,500)
            dest_centre = (self.dimensions[0]/2,self.dimensions[1]/2)
            canvas.draw_image(img,
                    source_centre,
                    source_size,
                    dest_centre,
                    dest_size)
            self.pressSpace.draw(canvas)

class State(Enum):
    START = 0
    PLAYING = 1
    PAUSED = 2
    GAMEOVER = 3

