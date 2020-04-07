import os
from vect import Vector
from fish import Shark
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Player:
	def __init__(self, dimensions,time):
		self.time = time
		self.lastFrameTime = self.time.time()
		self.canvas_dim = dimensions

		#address needed to gain local directory to access images folder below
		addr = os.getcwd()
		
		##image info + dimensions (constants)
		self.img = simplegui.load_image("file:///"+addr+"/images/boat2.png")
		self.dim = (4096, 4096)
		self.cen = (self.dim[0]/2, self.dim[1]/2)
		self.draw_dim = (140, 160)
		self.y_offset = 80
		
                ##player position and velocity
		self.pos = Vector(self.draw_dim[0]/2,self.draw_dim[1]/5+self.canvas_dim[1]*0.3-self.y_offset)
		self.vel = Vector(0,0)

	def getPos(self):
		return self.pos
	def setPos(self, newPos):
		self.pos = newPos

	def getVel(self):
		return self.vel

	#setter for velocity not needed, so replaced by add velocity method
	def addVel(self, velocity):
		self.vel.add(velocity)

	#updates position based on velocity and frame rate	
	def update(self):
		delta = self.time.time()-self.lastFrameTime
		self.lastFrameTime = self.time.time()
		self.pos.add(self.vel*delta)
		self.vel.multiply(0.85)

	#checks whether the user is within the horizontal bounds of the screen  
	def inBounds(self):
		return ((self.draw_dim[0]/2 <= self.pos.x) and (self.canvas_dim[0] - self.draw_dim[0]/2 >= self.pos.x))

        #sets users positions when they are reaching outer bounds
	def set(self):
		self.vel *= -1
		if (self.pos.get_p()[0]< self.canvas_dim[0]/2):
			self.pos = Vector(self.draw_dim[0]/2+1,self.pos.y)
		else:
			self.pos = Vector(self.canvas_dim[0]-self.draw_dim[0]/2-1,self.pos.y)

        #draws player ship sprite to canvas
	def draw(self,canvas):
		canvas.draw_image(self.img, self.cen, self.dim, self.pos.get_p(), self.draw_dim)
								
