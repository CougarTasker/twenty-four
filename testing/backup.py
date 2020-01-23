import random,math
from vect import Vector
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500
class Camera:
	"""docstring for Camera"""
	def __init__(self,pos=Vector(WIDTH/2,HEIGHT/2),fov=60,zoom=10,rotation=0,height=50,rays=50,vrot=0):
		self.fov = fov
		self.height = height
		self.rays = rays
		self.vrot = vrot 
		self.pos = pos
		self.rot = rotation
		self.zoom = zoom
	def draw(self,canvas,stage,old = True):
		if old:
			all = self.scaledLines(stage)
			for i in all:
				i.draw(canvas)
			a = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov/2)*self.zoom+self.pos
			b = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov/2)*self.zoom
			Line(a,b).draw(canvas,"green")
		else:			
			stage = self.culling(stage)
			lines = self.lines()
			x = 0
			a = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov/2)*self.zoom+self.pos
			b = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov/2)*self.zoom+self.pos
			plane = Line(a,b)
			for line in lines:
				smallest = 10000000
				for wall in stage:
					d = wall.dist(line)[0] + plane.dist(line)[0]
					if d < smallest and d > 0:
						smallest = d
						wll = wall
				if smallest < 10000000:
					p = self.vline(smallest,wll.height)
					canvas.draw_line((x*10+5,p[0]),(x*10+5,p[1]),10,"green")
				x+=1
	def lines(self):
		out = []
		a = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov/2)
		b = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov/2)
		rays = 5
		mov = (b-a)/self.rays
		for x in range(self.rays):
			out.append(Line(self.pos,a+mov*x,False))
		return out
	def culling(self,stage):
		out = []
		for i in stage:
			if self.insidefov(i):
				out.append(i)
		return out
	def insidefov(self,line):
		return self.insidefovp(line.pos) or self.insidefovp(line.end) or line.dist(Line(self.pos,Vector(1,0).rotate(self.rot),False))[0]>0
	def insidefovp(self,point):
		return abs(self.ang(point))<= self.fov/2
	def ang(self,point):
		return (point-self.pos).angle(Vector(1,0).rotate(self.rot))*180/math.pi

	def vline(self,dist,wallheight):
		print(dist)
		ph = self.zoom*math.tan(self.fov)*HEIGHT/WIDTH
		va = (Vector(self.zoom,ph)).rotate(self.vrot)
		vb = (Vector(self.zoom,-ph)).rotate(self.vrot)
		plane = Line(vb,va)
		top = Line(Vector(),Vector(dist,wallheight-self.height))
		bottom = Line(Vector(),Vector(dist,-self.height))
		return [plane.dist(top,False)[1]/(2*ph)*HEIGHT,plane.dist(bottom,False)[1]/(2*ph)*HEIGHT]
	def scaledLines(self,stage):
		lines = self.lines()
		stage = self.culling(stage)
		for line in lines:
			smallest = 10000000
			for wall in stage:
				d = wall.dist(line)[0]
				if d < smallest and d > 0:
					smallest = d
			line.end = line.norm * smallest + line.pos
		return lines

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.border = False
        self.draw = True
    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['x']:
            self.border = not self.border
        if key == simplegui.KEY_MAP['z']:
            self.draw = not self.draw

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
class Line():
	def __init__(self,pos,end,is_segment = True,height=100):
		if(is_segment):
			self.pos = pos
			self.end = end
			self.norm = self.end - self.pos
		else:
			self.pos = pos
			self.end = pos + end
			self.norm = end
		self.height = height
		self.norm.normalize()
		self.len = (self.end-self.pos).length()

	def closestPoint(self,point):
		e = self.end-self.pos	
		f= point-self.pos
		c = (f).dot(e)/e.dot(e)
		if(c<0):
			return self.pos
		elif(c>1):
			return self.end
		else:
			return self.pos + e*c
	def dist(self,line,check=True):
		spos = (line.pos-self.pos).cross(line.norm)/self.norm.cross(line.norm)
		if spos<0 or spos>self.len and check:
			return [-1,0]
		else:
			return [(self.pos-line.pos).cross(self.norm)/line.norm.cross(self.norm),spos]
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
	def draw(self,canvas,c = "Blue"):
		canvas.draw_line(self.pos.tuple(),self.end.tuple(),2,c)
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
	#print("click")
	global lines,last
	if kbd.border:
		if len(lines)==0:
			if last is None:
				last = Vector.fTuple(pos)
			else:
				lines.append(Line(last,Vector.fTuple(pos)))
				last = Vector.fTuple(pos)
		else:
			lines.append(Line(last,Vector.fTuple(pos)))
			last = Vector.fTuple(pos)
			#print(Line.tostrings(lines)
	else:
		cam.pos = Vector.fTuple(pos)

class Rect():
	def __init__(self,pos: Vector,width,height):
		self.min = pos
		self.max = pos + Vector(width,height)
		self.width = width
		self.height = height
	def draw(self,canvas):
		canvas.draw_line(self.min.tuple(),self.max.tuple(),10,"Blue")

def draw(canvas):
	#cam.rot +=0.2
	if kbd.left:
		cam.rot +=0.5
	if kbd.right:
		cam.rot -=0.5
	
	for i in lines:
		if cam.insidefov(i):
			i.draw(canvas)
		else:
			i.draw(canvas,"red")
		#canvas.draw_point(i.closestPoint(cam.pos).tuple())
	cam.draw(canvas,lines,kbd.draw)


cam = Camera()
stage = Rect(Vector(0,0),200,200)
kbd = Keyboard()
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
# pos the frame animation
frame.set_mouseclick_handler(mouse)
frame.start()