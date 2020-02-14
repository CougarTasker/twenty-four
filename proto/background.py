import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Background:
	def __init__(self,dimensions):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.clouds = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/background_clouds.png")
		self.sun = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/sun.png")
		self.water_world = simplegui.load_image("underwater-seamless-landscape-cartoon-background-vector-7524975.png")
		#self.floor = simplegui.load_image()
	def background(self,canvas,pollycount,wavecount,frequency,height,waveheight,color):
		path = [(0,self.dimensions[1])]
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*self.dimensions[0],((math.sin(ang)*waveheight/2+height)*self.dimensions[1])))
		path.append((self.dimensions[0],self.dimensions[1]))
		path.append((0,self.dimensions[1]))
		canvas.draw_polygon(path,1,color,color)
	def draw_sun(self,canvas,height):
		canvas.draw_image(self.sun,(250,250),(500,500),(self.dimensions[0]-self.dimensions[1]*height/2,self.dimensions[1]*height/2),(self.dimensions[1]*height,self.dimensions[1]*height))
	def looping_clouds(self,canvas,frequency,height):
		offset = self.lastFrameTime%(1/frequency)*frequency
		dim = (2400,300)
		cen = (1200,150)
		width = dim[0]/dim[1]*height*self.dimensions[1]
		canvas.draw_image(self.clouds, cen, dim,(width/2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
	def draw_water_world(self,canvas):
    		canvas.draw_image(self.water_world,(997/2,647/2),(997,647),(self.dimensions[0]/2,2*self.dimensions[1]/3),(self.dimensions[0],2*self.dimensions[1]/3))
	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		self.looping_clouds(canvas,0.05,0.2)
		self.draw_sun(canvas,0.3)
		self.looping_clouds(canvas,0.03,0.25)
		self.draw_water_world(canvas)
		self.background(canvas,20,4,1,0.3,0.03,"rgb(0,0,100)")
		self.background(canvas,20,3,-0.6,0.3,0.04,"rgb(0,0,150)")
		self.background(canvas,20,2,0.2,0.3,0.05,"rgb(32,178,170)")
		