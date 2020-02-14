import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
class Background:
	def __init__(self,dimensions):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.clouds = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/background_clouds.png")
		self.sun = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/sun.png")
		self.water_world = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/underwater-seamless-landscape-cartoon-background-vector-7524975.png")

		#self.floor = simplegui.load_image()
	def background(self,canvas,pollycount,wavecount,frequency,height,waveheight,color):
		path = [(0,self.dimensions[1])]
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*self.dimensions[0],((math.sin(ang)*waveheight/2+height)*self.dimensions[1])))
		path.append((self.dimensions[0],0))
		path.append((0,0))
		canvas.draw_polygon(path,1,color,color)
	def draw_wave_parts(self,canvas,poly,color):
		for path in poly:
			if len(path) > 2:
				canvas.draw_polygon(path,1,color,color)
	def poly(self,pollycount,wavecount,frequency,height,waveheight):
		path = []
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*self.dimensions[0],((math.sin(ang)*waveheight/2+height)*self.dimensions[1])))
		return path
	def sub(self,pollycount,a,b,c):
		paths = []
		drawing = False
		forward = []
		backward = []
		for x in range(pollycount+1):
			if a[x][1] <= b[x][1] and a[x][1] <= c[x][1]:
				if not drawing:
					drawing = True
					forward = []
					if x>0:
						bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
						cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
						if bint[1] < cint[1]:
							forward.append(bint)
						else:
							forward.append(cint)
						
					backward = []
				forward.append(a[x])
				if b[x][1]<c[x][1]:
					backward.append(b[x])
				else:
					backward.append(c[x])
			else:
				if drawing:
					bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
					cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
					if bint[1] < cint[1]:
						forward.append(bint)
					else:
						forward.append(cint)

					drawing = False
					backward.reverse()
					paths.append(forward+backward)

		if drawing: 
			drawing = False
			backward.reverse()
			paths.append(forward+backward)
		return paths

	def intersection(self,a,b,c,d):
		a = V(a[0],a[1])
		b = V(b[0],b[1])
		c = V(c[0],c[1])
		d = V(d[0],d[1])
		cd = d-c
		ab = b-a
		u = (a.cross(ab)-c.cross(ab))/cd.cross(ab)
		l = (c.cross(cd)-a.cross(cd))/ab.cross(cd)
		if u>=0 and u<= 1 and l >= 0 and l <= 1:
			return (u * cd + c).get_p()	
		else:
			return (0,1000)
	def draw_sun(self,canvas,height):
		canvas.draw_image(self.sun,(250,250),(500,500),(self.dimensions[0]-self.dimensions[1]*height/2,self.dimensions[1]*height/2),(self.dimensions[1]*height,self.dimensions[1]*height))
	def looping_clouds(self,canvas,frequency,height):
		offset = self.lastFrameTime%(1/frequency)*frequency
		dim = (2400,300)
		cen = (1200,150)
		width = dim[0]/dim[1]*height*self.dimensions[1]
		canvas.draw_image(self.clouds, cen, dim,(width/2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))

	def draw_water_world(self,canvas,top = 0.25):
    		canvas.draw_image(self.water_world,(997/2,647/2),(997,647),(self.dimensions[0]/2,(top+(1-top)/2)*self.dimensions[1]),(self.dimensions[0],self.dimensions[1]*(1-top)))

	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()

		
		# self.background(canvas,20,4,1,0.3,0.03,"rgb(0,0,100)")
		# self.background(canvas,20,3,-0.6,0.3,0.04,"rgb(0,0,150)")
		self.draw_water_world(canvas)
		self.background(canvas,20,2,0.2,0.3,0.05,"rgb(0,0,250)")
		big = self.poly(40,2,0.2,0.3,0.05) #rgb(0,0,250)
		middle = self.poly(40,3,-0.6,0.3,0.04) # rgb(0,0,150)
		small = self.poly(40,4,1,0.3,0.03) #rgb(0,0,100)
		middles = self.sub(40,middle,big,big)
		smalls = self.sub(40,small,middle,big)
		self.draw_wave_parts(canvas,middles,"rgb(0,0,150)")
		self.draw_wave_parts(canvas,smalls,"rgb(0,0,100)")

		self.looping_clouds(canvas,0.05,0.2)
		self.draw_sun(canvas,0.3)
		self.looping_clouds(canvas,0.03,0.25)

