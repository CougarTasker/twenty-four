import random,math,time
from vect import Vector
from cam import Camera
from ln import Line
try:
	import simplegui
except ImportError :
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Keyboard:
	def __init__(self):
		self.right = False
		self.left = False
		self.w = False
		self.a = False
		self.s = False
		self.d = False
		self.up = False
		self.down = False
		self.border = False
		self.draw = True
	def keyDown(self, key):
		if key == simplegui.KEY_MAP['right']:
			self.right = True
		if key == simplegui.KEY_MAP['left']:
			self.left = True
		if key == simplegui.KEY_MAP['w']:
			self.w = True
		if key == simplegui.KEY_MAP['a']:
			self.a = True
		if key == simplegui.KEY_MAP['s']:
			self.s = True
		if key == simplegui.KEY_MAP['d']:
			self.d = True
		if key == simplegui.KEY_MAP['up']:
			self.up = True
		if key == simplegui.KEY_MAP['down']:
			self.down = True
		if key == simplegui.KEY_MAP['x']:
			self.border = not self.border
		if key == simplegui.KEY_MAP['z']:
			self.draw = not self.draw

	def keyUp(self, key):
		if key == simplegui.KEY_MAP['right']:
			self.right = False
		if key == simplegui.KEY_MAP['left']:
			self.left = False
		if key == simplegui.KEY_MAP['w']:
			self.w = False
		if key == simplegui.KEY_MAP['a']:
			self.a = False
		if key == simplegui.KEY_MAP['s']:
			self.s = False
		if key == simplegui.KEY_MAP['d']:
			self.d = False
		if key == simplegui.KEY_MAP['up']:
			self.up = False
		if key == simplegui.KEY_MAP['down']:
			self.down = False

lines = []
last = None
wallImg = simplegui.load_image("file:///C:/Users/Couga/Documents/repos/twenty-four/testing/wall.png")
def mouse(pos):
	#print("click")
	global lines,last

	if kbd.border and ((last is None) or  (last != Vector.fTuple(pos))):
		
		if last is None:
			last = Vector.fTuple(pos)
		else:
			if kbd.up:
				lines.append(Line(last,Vector.fTuple(pos),True,wallImg,height = 40,transparent= True,y=60))
			if kbd.down:
				lines.append(Line(last,Vector.fTuple(pos),True,wallImg,height = 40,transparent= True))
			if not kbd.up and not kbd.down:
				lines.append(Line(last,Vector.fTuple(pos),True,wallImg))
			last = Vector.fTuple(pos)
			#print(Line.tostrings(lines)
	else:
		cam.pos = Vector.fTuple(pos)

class Rect():
	def __init__(self,pos,width,height):
		self.min = pos
		self.max = pos + Vector(width,height)
		self.width = width
		self.height = height
	def draw(self,canvas):
		canvas.draw_line(self.min.tuple(),self.max.tuple(),10,"Blue")
lasttime = time.time()
def draw(canvas):
	global lasttime,t
	if (time.time() - lasttime) > 1/50:
		if cam.rays>Camera.WIDTH/10:
			cam.rays -=1
	elif(time.time() - lasttime) < 1/60:
		if cam.rays < Camera.WIDTH:
			cam.rays +=1
	lasttime = time.time()
	#cam.rot +=0.2
	cam.draw(canvas,lines,kbd.draw)
	if kbd.draw:
		for i in lines:
			if cam.insidefov(i):
				i.draw(canvas)
			else:
				i.draw(canvas,"red")
	else:
		canvas.draw_circle(cam.project(Vector(300,100)),5,2,"blue","blue")
		canvas.draw_circle(cam.project(Vector(300,200)),5,2,"blue","blue")
		#canvas.draw_point(i.closestPoint(cam.pos).tuple())
	
def pysloop():
	if kbd.left:
		cam.rot -=1.5
	if kbd.right:
		cam.rot +=1
	mv = Vector()
	if kbd.a:
		mv.y -= 1
	if kbd.d:
		mv.y += 1
	if kbd.w:
		mv.x += 1
	if kbd.s:
		mv.x -= 1
	if kbd.up:
		cam.rays +=1
	if kbd.down:
		cam.rays -=1
	cam.move(mv)
	cam.colides(lines)

lines.append(Line(Vector(300,100),Vector(300,200),True,wallImg))
cam = Camera()
kbd = Keyboard()
physloop = simplegui.create_timer(1000/60,pysloop)
frame = simplegui.create_frame("Points", Camera.WIDTH , Camera.HEIGHT,0)
frame.set_draw_handler(draw)
frame.set_canvas_background("White")
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
# pos the frame animation
frame.set_mouseclick_handler(mouse)
physloop.start()
frame.start()
