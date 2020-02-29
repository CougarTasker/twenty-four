from user305_o32FtUyCKk_0 import Vector
from user305_lfCjyroK6r_12 import Background

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
        self.back = Background(dimensions)
    def update(self):
        pass
    def draw(self, canvas):
        delta = time.time()-self.lastFrameTime
        self.lastFrameTime = time.time()
        self.back.draw(canvas)

i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT))

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Background", CANVAS_WIDTH, CANVAS_HEIGHT)

frame.set_canvas_background("rgb(87,221,255)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()