from vect import Vector
from keyboard import Keyboard 
from player import Player
from background import Background as Bg
from fish import School
from rod import Rod
from hearts import Hearts

import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)

class Interaction:
	def __init__(self,dimensions, kbd):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.back = Bg(dimensions)
		self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))
		self.player = Player(dimensions)
		self.hearts = Hearts(dimensions)
		self.keyboard = kbd
		self.rod = Rod(self.player,CANVAS_HEIGHT)
		self.gametime = 120
		self.count = 1
		self.overscore = 100 #* numberoflevel
		self.playing = True
	def time(self):
		self.count += 1
		if self.count % 33 == 0:
			self.gametime -= 1
	def play(self):
		self.playing = True 
		self.back.play()
		self.back.play()
	def pause(self):
		self.playing = False
		self.back.pause()
		self.fish.pause()
	def alt(self):
		self.playing = not self.playing
		self.back.alt()
		self.fish.alt()
	def update(self):
		self.time()
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
		self.player.loseheart(self.rod)
		self.player.calculatescore(self.rod)
		self.rod.updatecatch()
		
	def draw(self, canvas):
		if self.keyboard.p:
			self.alt()
			self.keyboard.p = False
		self.back.draw(canvas)
		self.fish.draw(canvas)
		if self.playing:
			self.update()
			self.player.update()
			self.player.draw(canvas)
			self.rod.draw(canvas)
			self.hearts.update(canvas, self.player)
			canvas.draw_text('Score:',(15,50),30,'rgb(237,28,0)')
			canvas.draw_text(str(self.player.points),(15,80),30,'rgb(237,28,0)')
			canvas.draw_text('Time:',(90,50),30,'rgb(40,237,0)','serif')
			canvas.draw_text(str(self.gametime),(90,80),30,'rgb(40,237,0)','serif')
			canvas.draw_text('Goal Score:',(CANVAS_WIDTH/2,30),20,'rgb(149,26,237)','serif')
			canvas.draw_text(str(self.overscore),(CANVAS_WIDTH/2,50),20,'rgb(149,26,237)','serif')

			#self.over.draw(canvas)
kbd = Keyboard()
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),kbd)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT,0)


frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
