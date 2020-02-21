import os
from vect import Vector
from rod import Rod
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Player:
   def __init__(self, dimensions):
      self.canvas_dim = dimensions
      addr = os.getcwd()
      ##image info + dimensions (constants)

      self.img = simplegui.load_image("file:///"+addr+"/images/colouredBoth.png")
      self.dim = (4096, 4096)

      self.cen = (self.dim[0]/2, self.dim[1]/2)
      self.draw_dim = (140, 160)
      self.y_offset = 45
      #self.x_offset

      ##player position and other attributes (variables)
      self.pos = Vector(self.draw_dim[0]/2,self.draw_dim[1]/2+self.y_offset)
      self.vel = Vector(0,0)
      self.lives = 3
      self.points = 0
      #self.rod = Rod(radius, "file:///"+addr+"/images/hook.png", "file:///"+addr+"/images/colouredBoth.png")


   def getPos(self):
      return self.pos
   def setPos(self, newPos):
      self.pos = newPos

   def getVel(self):
      return self.vel
   def addVel(self, velocity):
      self.vel.add(velocity)

   def getLives(self):
      return self.lives
   def setLives(self, life):
      self.lives = life
   
   def setToZero(self):
      self.points = 0
   def setPoints(self, newP):
      self.points = newP
   def getPoints(self):
      return self.points

   def update(self):
      self.pos.add(self.vel)
      self.vel.multiply(0.85)
      #print(self.pos.get_p())
      
   def inBounds(self):
      return ((0 <= self.pos.get_p()[0]) and (self.canvas_dim[0] >= self.pos.get_p()[0]))

   
   def set(self):
      if (0 > self.pos.get_p()[0]):
         self.pos = Vector(1,self.draw_dim[1]/2+self.y_offset)
      else:
         self.pos = Vector(self.canvas_dim[0]-1,self.draw_dim[1]/2+self.y_offset)
      
        
   def draw(self,canvas):
       canvas.draw_image(self.img, self.cen, self.dim, self.pos.get_p(), self.draw_dim) 
                        
##def draw(canvas):
##    play = Player((900,400))
##
##    play.draw(canvas)
##
##frame = simplegui.create_frame("ship test", 600,400)
##
##
##frame.set_draw_handler(draw)
### Start the frame animation
##frame.start()
