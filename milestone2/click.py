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
	def __init__(self,stat = False,pos = Vector(-20,-20)):
		if stat:
			self.r = 20
			self.vel = Vector()
			self.color = "Red"
		else:
			self.r = random.randrange(10, 50)
			self.color = randCol()
			self.vel = Vector.polar(random.random()*math.pi*2,random.uniform(30,70))
		self.pos = pos
		self.acc = Vector()
	def update(self,time):
		self.pos +=self.vel * time
	def draw(self,canvas):
		if(self.r <= 0):
			self.r=0.1
		canvas.draw_circle(self.pos.tuple(),self.r/2,self.r,self.color)
	def within(self,pos):
		return (Vector.fTuple(pos)-self.pos).mag()<=self.r
	def collides(self,rect: Rect):
		dx = min(abs(self.pos.x-rect.min.x),abs(self.pos.x-rect.max.x))
		dy = min(abs(self.pos.y-rect.min.y),abs(self.pos.y-rect.max.y))
		mid = (rect.max-rect.min)/2+rect.min-self.pos
		return not(dx*dx+dy*dy<self.r*self.r or (dx<self.r or dy<self.r) or (abs(mid.x)<rect.width/2 and abs(mid.y)<rect.height/2))

#stage = Rect(Vector(10,10),WIDTH-20,HEIGHT-20)
stage = Rect(Vector(0,0),WIDTH,HEIGHT)
ball = Ball(True)
def draw(canvas):
	ball.update(1/60)
	ball.draw(canvas)
def mouse(position):
	global ball
	if ball.within(position):
		ball=Ball(True)
	else:
		ball = Ball(True,Vector.fTuple(position))
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT,0)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse)
# Start the frame animation
frame.start()