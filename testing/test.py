import random,math
from vect import Vector
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500
class Line():
	def __init__(self,pos,end,is_segment = True):
		if(is_segment):
			self.pos = pos
			self.end = end
			self.norm = self.end - self.pos
			self.norm.normalize()
		else:
			self.pos = pos
			self.end = pos + end
			self.norm = end
		self.len = (self.end-self.pos).length()
		self.m = self.norm.y/self.norm.x
		self.c = self.pos.y - self.m*self.pos.x
	def dist(self,line):
		x = (line.c - self.c)/(self.m -line.m)
		y = self.m * x + self.c
		pos = (x-self.pos.x)/self.norm.x
		if pos<0 or pos>self.len:
			return -1
		else:
			return (Vector(x,y)-line.pos).length()

	@staticmethod
	def fromstring(string):
		vals = string[1:len(string)-1].rsplit(",")
		return Line(Vector.fromstring(vals[0]),Vector.fromstring(vals[1]))
	
	@staticmethod
	def fromstrings(string):
		out= []
		vals = string.rsplit(" ")
		for v in vals:
			out.append(Line.fromstring(v))
		return out
	def draw(self,canvas):
		canvas.draw_line(self.pos.tuple(),self.end.tuple(),2,"Blue")
	@staticmethod
	def tostrings(lst):
		out = ""
		for l in lst:
			out+=str(l)+" "
		return out

	def __str__(self):
		return "(" + str(self.pos) + "," + str(self.end) + ")"
lines = []
last = None
def mouse(pos):
	print("click")
	global lines,last
	if len(lines)==0:
		if last is None:
			last = Vector.fTuple(pos)
		else:
			lines.append(Line(last,Vector.fTuple(pos)))
			last = Vector.fTuple(pos)
	else:
		lines.append(Line(last,Vector.fTuple(pos)))
		last = Vector.fTuple(pos)
		#print(Line.tostrings(lines))
class Rect():
	def __init__(self,pos: Vector,width,height):
		self.min = pos
		self.max = pos + Vector(width,height)
		self.width = width
		self.height = height
	def draw(self,canvas):
		canvas.draw_line(self.min.tuple(),self.max.tuple(),10,"Blue")

def draw(canvas):
	for i in lines:
		i.draw(canvas)


stage = Rect(Vector(0,0),200,200)

frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
# pos the frame animation
frame.set_mouseclick_handler(mouse)
frame.start()