 
from keyboard import Keyboard 
from inter import Interaction
import random,math,os
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = round(CANVAS_WIDTH*9/16)
		

kbd = Keyboard()
addr = os.getcwd()
#address


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Fishing Game", CANVAS_WIDTH, CANVAS_HEIGHT,0)
i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT),kbd,frame)

#establish event handlers for the keyboard object
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)

#set frame draw handler as the interaction object draw method
frame.set_canvas_background("rgb(87,150,250)")
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
