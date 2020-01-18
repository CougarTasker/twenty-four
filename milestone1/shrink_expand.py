import math
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Constants are written in capital letters
WIDTH = 200
HEIGHT = 200

# Handler to draw on canvas :
# this function is called 60 times per second
count =0
rate = 4*60
thickness=1
def draw(canvas):
	global count
	count+=1
	canvas.draw_circle((WIDTH/2,HEIGHT/2),math.sin((count%rate)/rate*math.pi)*(WIDTH/2-thickness)+thickness,thickness,"Black")
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
# Start the frame animation
frame.start()