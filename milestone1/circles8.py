import random
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

def fill_circle(self,point,radius,color):
		self.draw_circle(point,radius/2,radius,color)

# Constants are written in capital letters
WIDTH = 200
HEIGHT = 200

# Handler to draw on canvas :
# this function is called 60 times per second
def randCol():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'

# Drawing handler :
# this function is called 60 times per second
count = 0
a='black'
b="white"
def draw(canvas):
	global count
	global a
	global b
	if(count%60 == 0):
		a = randCol()
		b = randCol()
	fill_circle(canvas,(100, 100), 100, a)
	fill_circle(canvas,(70, 70), 30, b)
	count+=1
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()