try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from vect import Vector

##class to draw the hearts onto the screen for the player lives

class Hearts:
	def __init__(self, dimensions,time,die):
		self.die = die
		self.canvas_dim = dimensions
		addr = os.getcwd()
		self.time = time
		self.img_full = simplegui.load_image("file:///"+addr+"/images/fullheart.png")
		self.img_empty = simplegui.load_image("file:///"+addr+"/images/emptyheart.png")
		self.dim = (51,42)
		self.cen = (self.dim[0]/2, self.dim[1]/2)
		self.draw_dim = (self.dim[0]/2, self.dim[1]/2)
		self.pos = Vector(self.dim[0]/2, self.dim[1]/2)
		self.offset = 25
		self.lives_max = 3
		self.lives = self.lives_max
	def resetLives(self):
		self.lives = self.lives_max
	def getLives(self):
		return self.lives
	def loseLife(self):
		self.lives -= 1 
		if self.lives <= 0:
			self.die.gameover()
		

	def draw(self,canvas):
		for i in range(0,self.lives):
			self.drawheart(canvas, self.img_full, self.offset*i)
		for i in range(0, self.lives_max-self.lives):
			self.drawheart(canvas, self.img_empty, self.offset *(2-i))
	def drawheart(self,canvas,img,offset):
		canvas.draw_image(img, self.cen, self.dim, (self.pos.get_p()[0] +offset,self.pos.get_p()[1]),self.draw_dim)
		
		
