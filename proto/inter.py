from background import Background as Bg
from fish import School
from rod import Rod
from player import Player
from keyboard import Keyboard
from hearts import Hearts 
from vect import Vector
from timehandel import TimeHandler
from overlay import Overlay
import random,math,time,os
from fish import Shark
import cProfile, pstats, io
from score import Score
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
	
class Interaction:
	def __init__(self,dimensions, kbd,frame):
		self.frame = frame
		self.time = TimeHandler()
		self.time.pause()
		self.lastFrameTime = self.time.time()
		self.dimensions = dimensions
		self.back = Bg(dimensions,self.time)
		#creates a school of 30 fish
		self.fish = School(30,dimensions,self.time,self)
		
		self.keyboard = kbd
		self.overlay = Overlay(kbd,self,dimensions,self.frame)
		self.start(False)

	#separte method to start and reset the game without calling init
	def start(self,resetFish = True): 
		self.player = Player(self.dimensions,self.time)
		if resetFish:
			self.fish.restart()
		self.hearts = Hearts(self.dimensions,self.time,self.overlay)
		self.score = Score(self.time,self.dimensions,self.overlay,self.frame)
		self.rod = Rod(self.player,self.dimensions[1],self.time)
		self.time.pause()
		
        #called by draw method to check user in bounds and if fish caught
	def update(self):
		self.back.update()
		#self.fish.update()
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
		if self.player.vel.length() > 5:
                        #checks whether player has moved and so fish would be released
			self.rod.playermoved()
		self.player.update()
		
	#updates hearts and score when fish/shark caught
	def catch(self,fish):
		if type(fish) == Shark:
			self.hearts.loseLife()
		else:
			self.score.incScore(10)
		self.rod.catch(fish)

	#calls draw method on all objects to draw to the canvas	
	def debugfps(self):
			delta = self.time.time()-self.lastFrameTime #calcuralte the amount of time that has passed
			self.lastFrameTime = self.time.time()
			if(delta != 0):
				print("fps: "+str(1/delta))
	def draw(self, canvas):	
		#profiling code
		
		# pr = cProfile.Profile()
		# pr.enable()
		self.debugfps()

		if self.time.isPlaying():
			self.update()
		self.time.prove_running()
		self.back.draw(canvas)
		self.fish.draw(canvas)
		self.player.draw(canvas)
		self.rod.draw(canvas)
		self.hearts.draw(canvas)
		self.score.draw(canvas)
		self.overlay.draw(canvas)

		# pr.disable()
		# s = io.StringIO()
		# sortby = 'cumulative'
		# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		# ps.print_stats()
		# print(s.getvalue())
