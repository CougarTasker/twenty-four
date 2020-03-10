
import os
from vect import Vector
from rod import Rod
from fish import Shark
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Player:
	def __init__(self, dimensions,time):
		self.time = time
		self.canvas_dim = dimensions
		addr = os.getcwd()
		##image info + dimensions (constants)
		self.img = simplegui.load_image("file:///"+addr+"/images/Boat2.png")
		self.dim = (4096, 4096)
	
		self.cen = (self.dim[0]/2, self.dim[1]/2)
		self.draw_dim = (140, 160)
		self.y_offset = 80
		#self.x_offset

	  ##player position and other attrbutes (variables)
		self.pos = Vector(self.draw_dim[0]/2,self.draw_dim[1]/5+self.canvas_dim[1]*0.3-self.y_offset)
		self.vel = Vector(0,0)
	  #self.rod = Rod(radius, "file:///"+addr+"/images/hook.png", "file:///"+addr+"/images/colouredBoth.png")


	def getPos(self):
		return self.pos
	def setPos(self, newPos):
		self.pos = newPos

	def getVel(self):
		return self.vel
	def addVel(self, velocity):
		self.vel.add(velocity)
	def update(self):
		self.pos.add(self.vel)
		self.vel.multiply(0.85)
		#print(self.pos.get_p())
	  
	def inBounds(self):
		return ((self.draw_dim[0]/2 <= self.pos.x) and (self.canvas_dim[0] - self.draw_dim[0]/2 >= self.pos.x))

	def set(self):
		self.vel *= -1
		if (self.pos.get_p()[0]< self.canvas_dim[0]/2):
			self.pos = Vector(self.draw_dim[0]/2+1,self.pos[1])
		else:
			self.pos = Vector(self.canvas_dim[0]-self.draw_dim[0]/2-1,self.pos[1])
	def draw(self,canvas):
		canvas.draw_image(self.img, self.cen, self.dim, self.pos.get_p(), self.draw_dim)
		#canvas.draw_circle((self.getPos()-Vector(30,-25)).get_p(),3,3,"red","red")
						
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