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
G = 100
class Rect():
	def __init__(self,pos: Vector,width,height):
		self.min = pos
		self.max = pos + Vector(width,height)
		self.c = (self.max-self.min)/2 + self.min
		self.width = width
		self.height = height
class Ball():
	def __init__(self,pos,stat = False):
		if stat:
			self.r = 20
			self.vel = Vector()
			self.color = "Red"
		else:
			self.r = random.randrange(10, 50)
			self.color = randCol()
			self.vel = Vector.polar(random.random()*math.pi*2,random.uniform(escVel()*0.5,escVel()*2))
		self.pos = pos
		self.acc = Vector()
	def update(self,time):
		maxv = escVel()
		v = self.vel+self.acc*time
		if self.vel.mag()>maxv:
			self.vel *= maxv/self.vel.mag()
		if v.mag()>maxv:
			v*= maxv/v.mag()
		self.pos +=(self.vel + v)*time/2
		self.vel = v
	def grav(self,sorce):
		self.acc = sorce.pos - self.pos
		t = self.acc.mag()
		self.acc *= 1/t
		self.acc *= G*(self.r**2)*(sorce.r**2)/(t**2)
	def draw(self,canvas):
		if(self.r <= 0):
			self.r=0.1
		canvas.draw_circle(self.pos.tuple(),self.r/2,self.r,self.color)
	def collides(self,rect,sorce):
		dx = min(abs(self.pos.x-rect.min.x),abs(self.pos.x-rect.max.x))
		dy = min(abs(self.pos.y-rect.min.y),abs(self.pos.y-rect.max.y))
		mid = (rect.max-rect.min)/2+rect.min-self.pos
		return not(dx*dx+dy*dy<self.r*self.r or (dx<self.r or dy<self.r) or (abs(mid.x)<rect.width/2 and abs(mid.y)<rect.height/2)) or (self.pos-sorce.pos).mag()<sorce.r

stage = Rect(Vector(0,0),WIDTH,HEIGHT)
#stage = Rect(Vector(10,10),WIDTH-20,HEIGHT-20)
def addball():
	global balls
	balls.append(Ball(Vector(WIDTH/2,HEIGHT/2)))
# Handler to draw on canvas :
# this function is called 60 times per second
balls = []
source = Ball(Vector(),True)
def escVel():
	return math.pow(2*(source.r**2)*G/(stage.c-source.pos).mag(),0.5)*10
def mouse(position):
	global source
	source = Ball(Vector.fTuple(position),True)
def draw(canvas):
	x=0
	while x<len(balls):
		balls[x].grav(source)
		balls[x].update(1/60)
		if balls[x].collides(stage,source):
			balls.pop(x)
		else:
			balls[x].draw(canvas)
			balls[x].r -= 0.03
			x+=1
	source.draw(canvas)
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT,0)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse)
timer = simplegui.create_timer(100,addball)
timer.start()
# Start the frame animation
frame.start()