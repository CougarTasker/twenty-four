from vect import Vector#
from timehandel import TimeHandeler
import random,math,time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500

class SpriteSheet(object):
	"""docstring for SpriteSheet"""
	def __init__(self, url,size=(1,1),pos = Vector(),framecount = -1,time = 1000,scale = 1,looping=True,timehand=TimeHandeler()):
		if framecount == -1:
			framecount = size[0]*size[1]
		self.timehand = timehand
		self.framecount = framecount
		self.url = url
		self.size = size
		self.looping = looping
		self.img = simplegui.load_image(url)
		self.bdim = Vector(self.img.get_width(),self.img.get_height()) # before dimentions
		self.adim = (self.bdim.x/self.size[0],self.bdim.y/self.size[1]) # after dimaentions
		self.cent = Vector(self.adim[0]/2,self.adim[1]/2)
		self.fno = 0
		self.time = time
		self.pos = pos
		self.scale =scale
	def done(self):
		return self.fno == self.framecount-1
	def draw(self,canvas,center=(-1,-1),size=(-1,-1),rotation=0):
		if self.looping:
			self.fno = round((self.timehand.time()%(self.time/1000))/(self.time/1000)*(self.framecount-1))
		else:
			self.fno = round(abs((self.timehand.time()%(self.time/1000))/(self.time/1000)-0.5)*2*(self.framecount-1))
		x = self.fno  % self.size[0]
		y = (self.fno - x)/self.size[0]
		if center[0] < 0:
			center = self.pos.get_p()
		if size[0] <0:
			size =(self.adim[0]*self.scale,self.adim[1]*self.scale)
		loc = Vector(x*self.adim[0],y*self.adim[1])
		canvas.draw_image(self.img,(self.cent+loc).get_p(),self.adim,center,size,rotation)
		

	


		
