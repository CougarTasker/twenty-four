import math
import time
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

def fill_circle(self,point,radius,color):
	radius += 0.01
	self.draw_circle(point,radius/2,radius,color)
def size():
	return math.pow(WIDTH*WIDTH+HEIGHT*HEIGHT,0.5)*1.01
# Constants are written in capital letters
WIDTH = 200
HEIGHT = 200

# Handler to draw on canvas :
# this function is called 60 times per second
count =0
rate = 4*60
thickness=5
forground=True
forg="Black"
bacg="White"
def draw(canvas):
	global count,forg,bacg
	count+=1
	if(count%rate==0):
		tmp = forg
		forg = bacg
		bacg = tmp
	canvas.draw_line((0,0),(WIDTH,0),HEIGHT*2,bacg)
	fill_circle(canvas,(WIDTH/2,HEIGHT/2),(count%rate)/rate*size()/2,forg)


# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()