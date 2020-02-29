import random,math,time
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
	def draw(self,canvas):
		canvas.draw_line(self.min.tuple(),self.max.tuple(),10,"Blue")


class Ball():


	def __init__(self,stat = False,pos = Vector(-20,-20)):
		if stat:
			self.r = 50
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
		#canvas.draw_circle(self.pos.tuple(),self.r/2,self.r,self.color)
		canvas.draw_image(image, (512/2,512/2), (512,512), self.pos.tuple(), (self.r*2, self.r*2))


	def within(self,pos):
		return (Vector.fTuple(pos)-self.pos).mag()<=self.r


	def collides(self,rect: Rect):
		dx = min(abs(self.pos.x-rect.min.x),abs(self.pos.x-rect.max.x))
		dy = min(abs(self.pos.y-rect.min.y),abs(self.pos.y-rect.max.y))
		mid = (rect.max-rect.min)/2+rect.min-self.pos
		touching_corner = dx*dx+dy*dy<self.r*self.r 
		touching_edge = (dx<self.r or dy<self.r)
		center_inside = (abs(mid.x)<rect.width/2 and abs(mid.y)<rect.height/2)
		return not(center_inside) or (touching_edge or touching_corner) 

	def closest(self,rect):
		x = self.c(rect.min.x,rect.max.x,self.pos.x)
		y = self.c(rect.min.y,rect.max.y,self.pos.y)
		top = self.pos.y < self.pos.x
		left = (rect.height -self.pos.y) < self.pos.x 
		if  self.pos.y == self.pos.x or (rect.height -self.pos.y) == self.pos.x:
			self.pos.x = x
			self.pos.y = y
			self.vel.x *= -1
			self.vel.y *= -1
		elif left ^ top:
			self.pos.y = y
			self.vel.y *= -1
		else:
			self.pos.x = x
			self.vel.x *= -1

			
	def c(self,a,b,c):
		if (c-a)>(b-a)/2:
			return b-self.r
		else:
			return a+self.r


#stage = Rect(Vector(20,20),WIDTH-40,HEIGHT-40)
stage = Rect(Vector(0,0),WIDTH,HEIGHT)
ball = Ball(True)
def draw(canvas):
	global count,last
	ball.update(1/60)
	if(ball.collides(stage)):

		ball.closest(stage)
		#ball.vel.reflect(c[1])c
	#stage.draw(canvas)
	ball.draw(canvas)
def mouse(position):
	global ball
	print("click")
	if ball.within(position):
		ball.vel = (Vector.fTuple(position)-ball.pos)*50
	else:
		ball = Ball(True,Vector.fTuple(position))
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT,0)
image = simplegui.load_image('file:///C:/Users/Couga/Documents/repos/twenty-four/milestone2/dvd.png')
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse)
# Start the frame animation
frame.start()