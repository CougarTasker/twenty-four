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
shrinkrate = 11*60
rotaterate = 7*60
thickness=5
def polar(ang,mag):
	return(math.cos(ang)*mag+WIDTH/2,math.sin(ang)*mag+HEIGHT/2)
def draw(canvas):
	global count
	count+=1
	rad = math.sin((count%shrinkrate)/shrinkrate*math.pi)*(WIDTH/2-thickness)+thickness
	canvas.draw_circle((WIDTH/2,HEIGHT/2),rad,thickness,"Black")12
	canvas.draw_line(polar((count%rotaterate)/rotaterate*math.pi*2,rad),polar((count%rotaterate)/rotaterate*math.pi*2+math.pi,rad),thickness,"Black")
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
# Start the frame animation
frame.start()