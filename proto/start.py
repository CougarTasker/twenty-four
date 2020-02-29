from vect import Vector
from keyboard import Keyboard 
from player import Player
from background import Background as Bg
from fish import School
from rod import Rod
from hearts import Hearts

import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)

class Interaction:
   def __init__(self,dimensions, kbd):
      self.lastFrameTime = time.time()
      self.dimensions = dimensions
      self.back = Bg(dimensions)
      self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))
      self.player = Player(dimensions)
      self.hearts = Hearts(dimensions)
      self.keyboard = kbd
      self.rod = Rod(self.player,CANVAS_HEIGHT)
      

   def update(self):
      global org
      self.rod.catch_fish(self.fish,self.player)
      if self.player.inBounds():
         if self.keyboard.right:
             if self.rod.direction == 0:
                self.player.addVel(Vector(1,0))
         elif self.keyboard.left:
             if self.rod.direction == 0:
                self.player.addVel(Vector(-1,0))
         elif self.keyboard.down:
            self.rod.down()
         elif self.keyboard.up:
            if self.rod.pos.y < 4:
                self.rod.swing = True
                org = True
            if not org:
                self.rod.pos.add(Vector(0,-5))
      else:
         self.player.set()
          
   def draw(self, canvas):
      self.update()
      self.player.update()
      delta = time.time()-self.lastFrameTime
      self.lastFrameTime = time.time()
      self.back.draw(canvas)
      self.fish.draw(canvas,delta)
      self.player.draw(canvas)
      self.rod.draw(canvas,self.player,org)
      self.hearts.update(canvas, self.player)

kbd = Keyboard()
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),kbd)
org = True

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT,0)


frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
