import random,math
from vect import Vector
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def randCol():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'
# Constants are written in capital letters
WIDTH = 200
HEIGHT = 200
class Ball():
	def __init__(self,pos):
		self.pos = pos
		self.r = random.randrange(10, 50)
		self.color = randCol()
		self.vel = Vector.polar(random.random()*math.pi,random.randrange(10,20))
	def update(self,time):
		self.pos +=self.vel * time
	def draw(self,canvas):
		if(self.r == 0):
			self.r ==0.001
		canvas.draw_circle(self.pos.tuple(),self.r/2,self.r,self.color)


# Handler to draw on canvas :
# this function is called 60 times per second
b = Ball(Vector(WIDTH/2,HEIGHT/2))
def draw(canvas):
    b.update(1/60)
    b.draw(canvas)
    b.r-=0.01
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()