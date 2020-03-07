from keyboard import Keyboard 
from inter import Interaction
import random,math,os
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)
		

kbd = Keyboard()


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT,0)
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),kbd,frame)

frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
