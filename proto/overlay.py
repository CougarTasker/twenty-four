try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from enum import Enum
import os
from spritesheet import SpriteSheet as SS
from timehandel import TimeHandeler
from vect import Vector
class Overlay:
	def __init__(self,kbd,inter,dim,frame):
		self.time = TimeHandeler()
		self.frame = frame
		self.dim = dim
		self.kbd = kbd
		self.inter = inter
		
		self.start = Screen(self.time,self.dim,self.frame,"press space to start")
		self.playing = Screen(self.time,self.dim,self.frame,"press p to pause")
		self.paused = Screen(self.time,self.dim,self.frame,"press p to play","pause.png")
		self.gameover = Screen(self.time,self.dim,self.frame,"press space to try again","game_over.png")

		self.state = self.start
		self.start.show()
	def gameOver(self):
		self.swapState(self.gameover)
		self.inter.time.pause()
	def swapState(self,now):
		if now != self.state:
			self.state.hide()
			self.state = now
			now.show()
	def checkKbd(self):
		if self.state == self.start:
			if self.kbd.space:
				self.swapState(self.playing)
				self.inter.start()
				self.inter.time.play()
				self.kbd.space = False
		if self.state == self.playing:
			if self.kbd.p:
				self.swapState(self.paused)
				self.inter.time.pause()
				self.kbd.p = False
		if self.state == self.paused:
			if self.kbd.p:
				self.swapState(self.playing)
				self.inter.time.play()
				self.kbd.p = False
		if self.state == self.gameover:
			if self.kbd.space:
				self.swapState(self.playing)
				self.inter.start()
				self.inter.time.play()
				self.kbd.space = False
	def draw(self,canvas):
		self.checkKbd()
		self.start.draw(canvas)
		self.playing.draw(canvas)
		self.paused.draw(canvas)
		self.gameover.draw(canvas)


class State(Enum):
	START = 0
	PLAYING = 1
	PAUSED = 2
	GAMEOVER = 3
class Screen:
	def __init__(self,time,dim,frame,text="",img=""):
		self.frame = frame
		self.showing = False
		self.length = 1
		
		self.time = time
		self.start = time.time()
		addr = os.getcwd()
		if img == "":
			self.img = None
		else:
			self.img = simplegui.load_image("file:///"+addr+"/images/"+img)
		self.text = text
		self.dim = dim
	def show(self):
		if not self.showing:
			self.showing = True
			self.start = self.time.time()
	def state(self):# 0 fully hidden 1= showing
		s = (self.time.time() - self.start)/self.length
		if self.showing:
			s -= 1
			if s < 0:
				s = 0
		if s > 1:
			s = 1
		if not self.showing:
			s = 1-s
		return 3*s**2-2*s**3

	def drawImg(self,canvas):
		s = self.state()
		height = 300
		if self.img != None and s*height>1:
			source_centre = (self.img.get_width() / 2, self.img.get_height() / 2)
			source_size = (self.img.get_width(), self.img.get_height())
			dest_size = (height*s*self.img.get_width()/self.img.get_height(),height*s)
			dest_centre = (self.dim[0]/2,self.dim[1]/2)
			canvas.draw_image(self.img,
				source_centre,
				source_size,
				dest_centre,
				dest_size)
	def drawString(self,canvas):
		if self.text != "":
			h=30
			p=5
			top = h + 3*p
			offset = (1-self.state()) * top
			w = self.frame.get_canvas_textwidth(self.text, h)
			pos =((self.dim[0]-w)/2,self.dim[1]-h/2-p+offset)
			self.back(canvas,(self.dim[0]/2,self.dim[1]-(h+p*2)/2-p+offset),w+p*2,h+p*2)
			canvas.draw_text(self.text,pos, h, "red")
	def back(self,canvas,pos,w,h):
		pos = (pos[0]-w/2,pos[1]-h/2)
		dim = (w+pos[0],h+pos[1])
		canvas.draw_polygon((pos,(pos[0],dim[1]),dim,(dim[0],pos[1])),1,"rgba(255,255,255,0)","rgba(100,100,100,0.5)")
	def draw(self,canvas):
		self.drawString(canvas)
		self.drawImg(canvas)

	def hide(self):
		if self.showing:
			self.showing = False
			self.start = self.time.time()
