try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from enum import Enum
import os
from spritesheet import SpriteSheet as SS
from vect import Vector
class Overlay:
	def __init__(self,kbd,inter,dimensions):
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
	def draw(self,canvas):
		self.checkKbd()
		if self.state == State.START:
			canvas.draw_text("press space to start", (self.dimensions[0]/2,self.dimensions[1]*0.8), 30, "red")
		if self.state == State.PLAYING:
			canvas.draw_text("press p to pause", (self.dimensions[0]/2,self.dimensions[1]*0.8), 30, "red")
		if self.state == State.PAUSED:
			canvas.draw_text("press p to play", (self.dimensions[0]/2,self.dimensions[1]*0.8), 30, "red")
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

