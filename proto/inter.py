from background import Background as Bg
from fish import School
from rod import Rod
from player import Player
from keyboard import Keyboard
from hearts import Hearts 
from vect import Vector
from timehandel import TimeHandeler
from overlay import Overlay
import random,math,time,os
from fish import Shark
from score import Score
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Interaction:
	def __init__(self,dimensions, kbd):
		self.time = TimeHandeler()
		self.lastFrameTime = self.time.time()
		self.dimensions = dimensions
		self.back = Bg(dimensions,self.time)
		self.fish = School(30,dimensions,self.time)
		self.keyboard = kbd
		self.overlay = Overlay(kbd,self,dimensions)
		self.start()

	def start(self): #separte method tos and reset the game without calling init
		self.player = Player(self.dimensions,self.time)
		self.hearts = Hearts(self.dimensions,self.time,self.overlay)
		self.score = Score(self.time,Vector(self.hearts.getWidth(),0),self.overlay)
		self.rod = Rod(self.player,self.dimensions[1],self.time,self)
		self.time.pause()
	def update(self):
		self.rod.catch_fish(self.fish)
		if self.player.inBounds():
			if self.keyboard.right:
				if self.rod.direction == 0:
					self.player.addVel(Vector(1,0))
			elif self.keyboard.left:
				if self.rod.direction == 0:
					self.player.addVel(Vector(-1,0))
			elif self.keyboard.down:
				self.rod.down()
		else:
			self.player.set()

		self.player.update()
	def catch(self,courtFish):
		count = 0
		for fish in courtFish:
			if type(fish) == Shark:
				self.hearts.loseLife()
			else:
				count+=1
		self.score.incScore(count*10)
	def draw(self, canvas):	
		if self.time.isPlaying():
			self.update()	
		self.back.draw(canvas)
		self.fish.draw(canvas)
		self.player.draw(canvas)
		self.rod.draw(canvas)
		self.hearts.draw(canvas)
		self.score.draw(canvas)
		self.overlay.draw(canvas)
			# canvas.draw_text('Score:',(15,50),30,'rgb(237,28,0)')
			# canvas.draw_text(str(self.player.points),(15,80),30,'rgb(237,28,0)')
			# canvas.draw_text('Time:',(90,50),30,'rgb(40,237,0)','serif')
			# canvas.draw_text(str(self.gametime),(90,80),30,'rgb(40,237,0)','serif')
			# canvas.draw_text('Goal Score:',(self.dimensions[0]/2,30),20,'rgb(149,26,237)','serif')
			# canvas.draw_text(str(self.overscore),(self.dimensions[0]/2,50),20,'rgb(149,26,237)','serif')
			#self.over.draw(canvas)