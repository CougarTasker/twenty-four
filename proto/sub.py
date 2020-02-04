from vect import Vector
import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

class Interaction:
	def __init__(self,dimensions):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.clouds = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/background_clouds.png")
		self.sun = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/sun.png")
		#self.floor = simplegui.load_image()
	def update(self):
		pass
	def background(self,canvas,pollycount,wavecount,frequency,height,waveheight,color):
		path = [(0,CANVAS_HEIGHT)]
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*CANVAS_WIDTH,((math.sin(ang)*waveheight/2+height)*CANVAS_HEIGHT)))
		path.append((CANVAS_WIDTH,CANVAS_HEIGHT))
		path.append((0,CANVAS_HEIGHT))
		canvas.draw_polygon(path,1,color,color)
	def draw_sun(self,canvas,offset):
		canvas.draw_image(self.sun,(360,197),(360//2,197//2),(CANVAS_WIDTH-offset,offset),(360,197))
	def looping_clouds(self,canvas,frequency,height):
		offset = self.lastFrameTime%(1/frequency)*frequency
		dim = (2400,300)
		cen = (1200,150)
		canvas.draw_image(self.clouds, cen, dim,(cen[0]-offset*dim[0],height*CANVAS_HEIGHT/2),(dim[0],height*CANVAS_HEIGHT))
		canvas.draw_image(self.clouds, cen, dim,(cen[0]+dim[0]-offset*dim[0],height*CANVAS_HEIGHT/2),(dim[0],height*CANVAS_HEIGHT))
	def draw(self, canvas):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		self.looping_clouds(canvas,0.05,0.2)
		self.looping_clouds(canvas,0.03,0.25)#
		self.draw_sun(canvas,100)
		self.background(canvas,20,4,1,0.3,0.03,"rgb(0,0,100)")
		self.background(canvas,20,3,-0.6,0.3,0.04,"rgb(0,0,150)")
		self.background(canvas,20,2,0.2,0.3,0.05,"rgb(0,0,250)")
		
		






i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT))

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)

frame.set_canvas_background("rgb(120,120,256)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
