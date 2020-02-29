from vect import Vector 
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Player:
   def __init__(self, dimensions):
      self.canvas_dim = dimensions

      ##image info + dimensions (constants)
      self.img = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/boatman.png")
      self.dim = (4096, 3790)
      self.cen = (self.dim[0]/2, self.dim[1]/2)
      self.draw_dim = (140, 140)

      ##player position and other attributes (variables)
      self.pos = Vector(self.draw_dim[0]/2,self.draw_dim[1]/2+65)
      self.vel = Vector(0,0)
      self.lives = 3
      self.points = 0
      #self.rod = Rod(xxx)


   def getPos(self):
      return self.pos
   def setPos(self, newPos):
      self.pos = newPos

   def getVel(self):
      return self.vel
   def addVel(self, velocity):
      self.vel.add(velocity)
      print(self.vel)

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
      print(self.pos.get_p())
      
   def inBounds(self):
      return ((0 <= self.pos.get_p()[0]) and (self.canvas_dim[0] >= self.pos.get_p()[0]))

   
   def set(self):
      if (0 > self.pos.get_p()[0]):
         self.pos = Vector(1,self.draw_dim[1]/2+ 65)
         print("updated")
      else:
         self.pos = Vector(self.canvas_dim[0]-1,self.draw_dim[1]/2+65)
         print("updated")
      
        
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
