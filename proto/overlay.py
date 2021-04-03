try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import os
from spritesheet import SpriteSheet as SS
from timehandel import TimeHandler
from vect import Vector
from snd import Snd

class Overlay:
	def __init__(self,kbd,inter,dim,frame):
		self.time = TimeHandler()
		self.frame = frame
		self.dim = dim
		self.kbd = kbd
		self.inter = inter
		#establishing states as screen objects
		self.start = Screen(self.time,self.dim,self.frame,Snd(self.time,"start.ogg",0.1,97),"press space to start","start.png",offset=(-30,30))
		self.playing = Screen(self.time,self.dim,self.frame,Snd(self.time,"waves.ogg",0.05,47),"press p to pause",autohide=True)
		self.paused = Screen(self.time,self.dim,self.frame,Snd(self.time,"paused.ogg",0.5,58),"press p to play","pause.png")
		self.gameover = Screen(self.time,self.dim,self.frame,Snd(self.time,"gameover.ogg",0.5,99),"press space to try again","game_over.png")

		self.state = self.start#the first state is the start state
		self.state.show()#show the start overlay
		
	

	def swapState(self,now):
		if now != self.state:#only swap if trasitioning to a new state
			self.state.hide(now)#sets old state to hidden so is not visible to user
			#the old state will show "now" once it is hidden
			self.state = now#updates the current state
	#state transtitons below	
	#separate method required when user reaches gameover since it isn't a keybord input 
	def gameOver(self):
		self.swapState(self.gameover)
		self.inter.time.pause()
    #checks for keyboard interaction which would cause a change of state
	def checkKbd(self):
		if self.state == self.start:
			if self.kbd.space:#check each key
				self.swapState(self.playing)#swap the state where nessary
				self.inter.start()#reset the game
				self.inter.time.play()#play
				self.kbd.space = False
				# set the key to up once the transition has been made
				# so each transition takes one key press
		if self.state == self.playing:
			if self.kbd.p:
				self.swapState(self.paused)
				self.inter.time.pause()#pause the game
				self.kbd.p = False
		if self.state == self.paused:
			if self.kbd.p:
				self.swapState(self.playing)
				self.inter.time.play()#resume the game
				self.kbd.p = False
		if self.state == self.gameover:
			if self.kbd.space:
				self.swapState(self.playing)
				self.inter.start()#reset the game 
				self.inter.time.play()
				self.kbd.space = False

	def draw(self,canvas):
		self.checkKbd()
		self.start.draw(canvas)
		self.playing.draw(canvas)
		self.paused.draw(canvas)
		self.gameover.draw(canvas)
        #calls all draw methods, but only one state is visible


class Screen:
	def __init__(self,time,dim,frame,sound=None,text="",img="",offset=(0,0),autohide = False):
		self.sound = sound
		self.frame = frame
		self.showing = False
		self.imgoff = offset
		self.length = 0.8
		self.autohide = autohide
		self.time = time
		self.start = time.time()-self.length*2
		addr = os.getcwd()
		if img == "":
			self.img = None
		else:
			self.img = simplegui.load_image("file:///"+addr+"/images/"+img)
			#used to generate local image directory if image is provided in argument
		self.text = text
		self.dim = dim
		self.swap = None

        #sets the original start state, called by overlay __init__ method with start object
	def show(self,swap=None):
		self.swap = swap
		if not self.showing:
			if not self.sound is None:
				self.sound.play()
			self.showing = True
			self.start = self.time.time()

	
	def state(self):# 0 fully hidden 1= showing
		s = (self.time.time() - self.start)/self.length
		if s > 1:
			if self.autohide and s > 5 and self.showing:
				self.hide()
				return self.state()
			s = 1
			if not self.swap is None:
				if self.showing:
					self.swap.hide()
				else:
					self.swap.show()
					if not self.sound is None:
						self.sound.pause()
				self.swap = None
		if not self.showing:
			s = 1-s
		if not self.sound is None and (not self.swap is None or self.showing):
			self.sound.setVol(s) #fade the source_centrend in an out 
		return 3*s**2-2*s**3

        #method to draw the image argument, e.g. start.png
	def drawImg(self,canvas,s):
		height = (self.dim[1] - 45*2)*0.95
		if self.img != None and self.img.get_height() > 0 and s*height>1:
			source_centre = (self.img.get_width() / 2, self.img.get_height() / 2)
			source_size = (self.img.get_width(), self.img.get_height())
			dest_size = (height*s*self.img.get_width()/self.img.get_height(),height*s)
			dest_centre = (self.dim[0]/2+self.imgoff[0] *s,self.dim[1]/2 +self.imgoff[1]*s)
			canvas.draw_image(self.img,
				source_centre,
				source_size,
				dest_centre,
				dest_size)
	#used to draw string onto screen, e.g. 'press p to pause'
	def drawString(self,canvas,s):
		if self.text != "":
			h=30
			p=5
			top = h + 3*p
			offset = (1-s) * top
			w = self.frame.get_canvas_textwidth(self.text, h,"sans-serif")
			pos =((self.dim[0]-w)/2,self.dim[1]-h/2-p+offset)
			self.back(canvas,(self.dim[0]/2,self.dim[1]-(h+p*2)/2-p+offset),w+p*2,h+p*2)
			canvas.draw_text(self.text,pos, h, "yellow","sans-serif")
			
	#sets background for text drawn to screen, called in drawString() method
	def back(self,canvas,pos,w,h):
		pos = (pos[0]-w/2,pos[1]-h/2)
		dim = (w+pos[0],h+pos[1])
		canvas.draw_polygon((pos,(pos[0],dim[1]),dim,(dim[0],pos[1])),1,"rgba(255,255,255,0)","rgba(50,50,50,0.7)")
	def draw(self,canvas):
		s = self.state()
		if s > 0:
			self.drawString(canvas,s)
			self.drawImg(canvas,s)

        #sets a state to hidden so user no longer sees it
	def hide(self,swap = None):
		self.swap = swap
		if self.showing:
			self.showing = False
			self.start = self.time.time()
