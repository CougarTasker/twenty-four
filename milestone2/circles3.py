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
WIDTH = 500
HEIGHT = 500
class Rect():
	def __init__(self,pos: Vector,width,height):
		self.min = pos
		self.max = pos + Vector(width,height)
		self.width = width
		self.height = height
class Ball():
	def __init__(self,pos):
		self.pos = pos
		self.r = random.randrange(10, 50)
		self.color = randCol()
		self.acc = Vector()
		self.vel = Vector.polar(random.random()*math.pi*2,random.randrange(50,100))
	def update(self,time):
		self.pos +=self.vel * time + 0.5*self.acc*
	def update(self,time,atractor):
		self.pos +=self.vel * time
	def draw(self,canvas):
		if(self.r <= 0):
			self.r=0.1
		canvas.draw_circle(self.pos.tuple(),self.r/2,self.r,self.color)
	def collides(self,rect: Rect):
		dx = min(abs(self.pos.x-rect.min.x),abs(self.pos.x-rect.max.x))
		dy = min(abs(self.pos.y-rect.min.y),abs(self.pos.y-rect.max.y))
		mid = (rect.max-rect.min)/2+rect.min-self.pos
		return not(dx*dx+dy*dy<self.r*self.r or (dx<self.r or dy<self.r) or (abs(mid.x)<rect.width/2 and abs(mid.y)<rect.height/2))

#stage = Rect(Vector(10,10),WIDTH-20,HEIGHT-20)
stage = Rect(Vector(0,0),WIDTH,HEIGHT)
def addball():
	global balls
	balls.append(Ball(Vector(WIDTH/2,HEIGHT/2)))
# Handler to draw on canvas :
# this function is called 60 times per second
balls = []
def draw(canvas):
	x=0
	while x<len(balls):
		balls[x].update(1/60)
		if balls[x].collides(stage):
			balls.pop(x)
		else:
			balls[x].draw(canvas)
			balls[x].r-=0.1
			x+=1
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT,0)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100,addball)
timer.start()
# Start the frame animation
frame.start()