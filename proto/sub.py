from vect import Vector
#from player import Player
from background import Background as Bg
from fish import School

import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

class Interaction:
	def __init__(self,dimensions):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.back = Bg(dimensions)
		self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))
	def update(self):
		pass
	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		self.back.draw(canvas)
		self.fish.draw(canvas,delta)

i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT))

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)

frame.set_canvas_background("rgb(120,120,256)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
