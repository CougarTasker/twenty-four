import random,math
from vect import Vector
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Line():
	minSep = 15
	def __init__(self,pos,end,is_segment = True,img= None,height=100,y=0,transparent = False):
		if(is_segment):
			self.pos = pos
			self.end = end
			self.norm = self.end - self.pos
		else:
			self.pos = pos
			self.end = pos + end
			self.norm = end
		self.t = transparent
		self.y = y
		self.img = img
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
	def minDist(self,point):
		return (self.closestPoint(point)-point).length()
	def mindistance(self,point):
		e = self.end-self.pos	
		f= point-self.pos
		c = (f).dot(e)/e.dot(e)
		if(c<0):
			c = 0
		if c>1:
			c=1
		return (self.pos + e*c-point).length()

	def dist(self,line,check=True):
		m = Line.minSep
		if self.norm.cross(line.norm) ==0:
			return [-1,0]
		spos = (line.pos-self.pos).cross(line.norm)/self.norm.cross(line.norm)
		if(spos<0 or spos>self.len) and check:
			return [-1,0]
		else:
			if check:
				dst = (self.pos-line.pos).cross(self.norm)/line.norm.cross(self.norm)
				if dst<m and dst>0:
				 	dst = m
				return [dst,spos]
			else:
				return [m,spos]
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
	def drawWall(self,canvas,screendims,realx,screenx,rayWidth,p,backface=False):
		WIDTH = screendims.x
		HEIGHT = screendims.y
		if not(self.img	is None):
			if backface:
				canvas.draw_line((screenx+rayWidth/2,p[0]),(screenx+rayWidth/2,p[1]),math.ceil(rayWidth)+2,"green")
			else:
				c= (self.img.get_width()/WIDTH*rayWidth/2+realx/self.len*(self.img.get_width()*(1-rayWidth/WIDTH)),self.img.get_height()/2)
				canvas.draw_image(self.img,c,(self.img.get_width()/WIDTH*rayWidth,self.img.get_height()),(screenx+rayWidth/2,(p[0]-p[1])/2+p[1]),(math.ceil(rayWidth),p[0]-p[1]))
			
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