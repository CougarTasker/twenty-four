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
	def __init__(self,dimensions, kbd,frame):
		self.frame = frame
		self.time = TimeHandeler()
		self.lastFrameTime = self.time.time()
		self.dimensions = dimensions
		self.back = Bg(dimensions,self.time)
		self.fish = School(30,dimensions,self.time,self)
		self.keyboard = kbd
		self.overlay = Overlay(kbd,self,dimensions,self.frame)
		self.start()
	def start(self): #separte method tos and reset the game without calling init
		self.player = Player(self.dimensions,self.time)
		self.hearts = Hearts(self.dimensions,self.time,self.overlay)
		self.score = Score(self.time,self.dimensions,self.overlay,self.frame)
		self.rod = Rod(self.player,self.dimensions[1],self.time)
		self.time.pause()
	def update(self):
		self.rod.catch_fish(self.fish)
		if self.player.inBounds():
			if self.keyboard.right:
				self.player.addVel(Vector(1,0)*40)
			elif self.keyboard.left:
				self.player.addVel(Vector(-1,0)*40)
			elif self.keyboard.down:
				self.rod.down()
		else:
			self.player.set()
		if self.player.vel.length() > 1:
			self.rod.playermoved()
		self.player.update()
	def catch(self,fish):
		if type(fish) == Shark:
			self.hearts.loseLife()
		else:
			self.score.incScore(10)
		self.rod.catch(fish)
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