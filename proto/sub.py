from vect import Vector
from background import Background
from carol import Carol
from pearl import Pearl
from bubble import bubblesheet
import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

class Interaction:
	def __init__(self,dimensions,pearl, carol):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.background = Background(dimensions)
		self.perl = pearl
		self.carol = carol
	def update(self):
		pass
	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		self.background.draw(canvas)
		self.carol.draw_canvas(canvas)
		self.perl.draw_canvas(canvas)



pearl = Pearl(Vector(417,383))
carol = Carol(Vector(136,331))
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),pearl,carol)

#bubble1 = bubblesheet(Vector())
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()