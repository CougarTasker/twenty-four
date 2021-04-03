import random,math
from vect import Vector
from ln import Line
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Camera:
	"""docstring for Camera"""
	WIDTH = 800
	HEIGHT = 800
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
				walls = []
				for wall in stage:
					intersection = wall.dist(line)
					d = intersection[0]*line.norm.dot(direction)# / (direction.length() * line.norm.length())
					walls.append([d,wall,intersection[1]])#distance to wall, the wall and the real x value 
				walls.sort(key = self.wallsorting)
				out = []
				
				for wall in walls:
					if wall[0] > 0:
						out.insert(0,wall)
						if not wall[1].t:
							break

				for wall in out:
					p = self.vline(wall[0],wall[1].height,wall[1].y)
					l = wall[1].norm.copy().rotate(90).dot(wall[1].pos-self.pos)<0
					wall[1].drawWall(canvas,Vector(Camera.WIDTH,Camera.HEIGHT),wall[2],x*self.WIDTH/self.rays,self.WIDTH/self.rays,p,l)
				x+=1
	def project(self,pos,y=0):
		cpos = pos-self.pos
		y = y - self.height
		cpos.rotate(-self.rot)
		wid = self.zoom*math.tan(self.fov*math.pi/360)
		hig = wid*self.HEIGHT/self.WIDTH
		cx = cpos.y*self.zoom/2/cpos.x/ wid * Camera.WIDTH
		cy = y *self.zoom/2/cpos.x/hig * Camera.HEIGHT
		return (cx+Camera.WIDTH/2,-cy+Camera.HEIGHT/2)
	def wallsorting(self,a):
		return a[0]
	def boundry(self):
		return self.zoom/math.cos(self.fov/360*math.pi)
	def colides(self,stage):
		col = []
		for wall in stage:
			if (wall.minDist(self.pos)< self.boundry()):
				col.append(wall)
		for wall in col:
			c = wall.closestPoint(self.pos)
			self.pos = (self.pos-c).normalize()*(self.boundry()+1)+c

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

	def vline(self,dist,wallheight,y):
		ph = self.zoom*math.tan(self.fov*math.pi/360)*self.HEIGHT/self.WIDTH
		va = (Vector(self.zoom,ph)).rotate(self.vrot)
		vb = (Vector(self.zoom,-ph)).rotate(self.vrot)
		plane = Line(va,vb)
		top = Line(Vector(),Vector(dist,y+wallheight-self.height))
		bottom = Line(Vector(),Vector(dist,y-self.height))

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
