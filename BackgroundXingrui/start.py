from vect import Vector
# from carol import Carol
# from pearl import Pearl
# from bubble import bubblesheet

from keyboard import Keyboard 
from player import Player
from background import Background as Bg
from fish import School

import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)

class Interaction:
   def __init__(self,dimensions, kbd):#,pearl, carol):
      self.lastFrameTime = time.time()
      self.dimensions = dimensions
      # self.perl = pearl
      # self.carol = carol
      self.back = Bg(dimensions)
      self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))
      self.player = Player(dimensions)
      self.keyboard = kbd

   def update(self):
      if self.player.inBounds():
         if self.keyboard.right:
            self.player.addVel(Vector(1,0))
         elif self.keyboard.left:
            self.player.addVel(Vector(-1,0))
      else:
         self.player.set()
          
   def draw(self, canvas):
      self.update()
      self.player.update()
      
      delta = time.time()-self.lastFrameTime
      self.lastFrameTime = time.time()
      self.back.draw(canvas)
      # self.carol.draw_canvas(canvas)
      # self.perl.draw_canvas(canvas)
      self.fish.draw(canvas,delta)
      self.player.draw(canvas)


#pearl = Pearl(Vector(417,383))
#carol = Carol(Vector(136,331))

kbd = Keyboard()
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),kbd)#,pearl,carol)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT,0)


frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
