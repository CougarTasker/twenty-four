import random,math
from vect import Vector
from ln import Line
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Camera:
	"""docstring for Camera"""
	WIDTH = 512
	HEIGHT = 512
	def __init__(self,pos=Vector(),fov=90,zoom=10,rotation=0,height=50,rays=256,vrot=0):
		if pos == Vector():
			pos = Vector(self.WIDTH/2,self.HEIGHT/2)
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
			a = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom+self.pos
			b = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom+self.pos
			Line(a,b).draw(canvas,"green")
		else:			
			stage = self.culling(stage)
			lines = self.lines()
			direction = Vector(1,0).rotate(self.rot)
			a = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom+self.pos
			b = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom+self.pos

			x = 0
			for line in lines:
				smallest = 10000000
				for wall in stage:
					intersection = wall.dist(line)
					d = intersection[0]*line.norm.dot(direction)# / (direction.length() * line.norm.length())
					if d < smallest and d > 0:
						smallest = d
						wll = wall
						realx = intersection[1]
				if smallest < 10000000:
					p = self.vline(smallest,wll.height)
					wll.drawWall(canvas,Vector(Camera.WIDTH,Camera.HEIGHT),realx,x*self.WIDTH/self.rays,self.WIDTH/self.rays,p)
				x+=1
	def lines(self):
		out = []
		a = Vector(1,0).rotate(self.rot-self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom
		b = Vector(1,0).rotate(self.rot+self.fov/2)/math.cos(self.fov*math.pi/360)*self.zoom
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
	def move(self,direction):
		if direction.length()>0:

			direction.normalize();
			direction.rotate(self.rot)
			direction *= 3
			self.pos+= direction
	def insidefov(self,line):
		return self.insidefovp(line.pos) or self.insidefovp(line.end) or line.dist(Line(self.pos,Vector(1,0).rotate(self.rot),False))[0]>0
	def insidefovp(self,point):
		return abs(self.ang(point))<= self.fov/2
	def ang(self,point):
		return (point-self.pos).angle(Vector(1,0).rotate(self.rot))*180/math.pi

	def vline(self,dist,wallheight):
		ph = self.zoom*math.tan(self.fov*math.pi/360)*self.HEIGHT/self.WIDTH
		va = (Vector(self.zoom,ph)).rotate(self.vrot)
		vb = (Vector(self.zoom,-ph)).rotate(self.vrot)
		plane = Line(va,vb)
		top = Line(Vector(),Vector(dist,wallheight-self.height))
		bottom = Line(Vector(),Vector(dist,-self.height))

		bd = plane.dist(bottom,False)
		td = plane.dist(top,False)
		if (bd[0] == -1 or td[0] == -1):
			return [-1,-1] 
		return [bd[1]/(2*ph)*self.HEIGHT,td[1]/(2*ph)*self.HEIGHT]
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
