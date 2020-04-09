from vect import Vector
from timehandel import TimeHandler
import random,math,time
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class SpriteSheet(object):
	"""SpriteSheet class used to handle animation of spritesheets
        param for init: image, size of sheet, position on canvas, framecount, time, scale, loop=true/false, timeHandeler object
        return: draws next relevant iteration of spritesheet"""
	def __init__(self, url,size=(1,1),pos = Vector(),framecount = -1,time = 1000,scale = 1,looping=True,timehand=TimeHandler()):
		if framecount == -1:
			framecount = size[0]*size[1]
		self.timehand = timehand
		self.framecount = framecount
		self.url = url
		self.size = size
		self.looping = looping
		self.img = simplegui.load_image(url)
		self.bdim = Vector(self.img.get_width(),self.img.get_height()) # before dimensions
		self.adim = (self.bdim.x/self.size[0],self.bdim.y/self.size[1]) # after dimensions
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
                        ##muse of modulus ensures it loops once it reaches the 'end' of the spritesheet			
		else:
			self.fno = round(abs((self.timehand.time()%(self.time/1000))/(self.time/1000)-0.5)*2*(self.framecount-1))
		x = self.fno  % self.size[0]
		y = (self.fno - x)/self.size[0]
		if center[0] < 0:
			center = self.pos.get_p()
		if size[0] <0:
			size =(self.adim[0]*self.scale,self.adim[1]*self.scale)
		loc = Vector(x*self.adim[0],y*self.adim[1])

                ##draw sprite image to canvas 		
		canvas.draw_image(self.img,(self.cent+loc).get_p(),self.adim,center,size,rotation)
		
		

	


		
