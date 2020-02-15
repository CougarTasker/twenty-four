from vect import Vector
# from carol import Carol
# from pearl import Pearl
# from bubble import bubblesheet

#from player import Player
from background import Background as Bg
from fish import School

import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)

class Interaction:
	def __init__(self,dimensions):#,pearl, carol):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		# self.perl = pearl
		# self.carol = carol
		self.back = Bg(dimensions)
		self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))

	def update(self):
		pass
	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		self.back.draw(canvas)
		# self.carol.draw_canvas(canvas)
		# self.perl.draw_canvas(canvas)
		self.fish.draw(canvas,delta)


#pearl = Pearl(Vector(417,383))
#carol = Carol(Vector(136,331))
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT))#,pearl,carol)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT,0)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()