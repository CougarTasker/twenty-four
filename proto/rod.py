import random, math, os,time
from  vect import Vector
from keyboard import Keyboard 
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def polar(ang,r):
	pX = r * math.cos(ang * (math.pi / 180))
	pY = r * math.sin(ang * (math.pi / 180))
	return Vector(round(pX),round(pY))

ltime = time.time()
class Rod:
	def __init__(self,player,windowheight):
			addr = os.getcwd()
			self.hook = simplegui.load_image("file:///"+addr+"/images/hook.png")
			#self.radius = 50
			self.swing = True
			self.playerPos = player.getPos()
			self.pos = Vector()
			self.rnorm = 150
			self.r = self.rnorm
			self.direction = 0
			position = Vector(player.getPos().x+65,player.getPos().y-70) + self.pos
			self.rmax = windowheight-(position).y-50/2
			self.courtFish = []
	def down(self):
		self.direction = 1
	def up(self):
		self.direction = -1
	def catch_fish(self,school,player):
		if self.direction != 0:
			self.courtFish = self.mergerlist(self.courtFish,school.touching_fish(self.hookpos(player),10))
		else:
			for fish in self.courtFish:
				fish.reset()
			self.courtFish = []
		school.move_fish(self.hookpos(player),self.courtFish)
		if self.direction == 1 and len(self.courtFish)>0:
			self.up()
	def mergerlist(self,a,b):
		for item in b:
			if not item in a:
				a.append(item)
		return a
	def hookpos(self,player):
		global ltime
		delta = time.time()-ltime
		ltime = time.time()

		frequency = 3
		ang = math.sin((ltime%frequency)/frequency * math.pi*2)*30/((self.r-self.rnorm)/60+1) +90
		position = Vector(player.getPos().x+65,player.getPos().y-70) + self.pos
		endPos = (polar(ang,self.r)+position)

		return endPos+Vector(15,-5).rotate(ang)
	def update_length(self,delta):
		self.r += self.direction * delta * 80
		if(self.r< self.rnorm):
			self.r = self.rnorm
			self.direction = 0
		if(self.r > self.rmax):
			self.r = self.rmax
			self.direction = -1
	def draw(self,canvas,player,org):
		global ltime
		delta = time.time()-ltime
		ltime = time.time()

		frequency = 3
		self.update_length(delta)
		ang = math.sin((ltime%frequency)/frequency * math.pi*2)*30/((self.r-self.rnorm)/60+1) +90
		position = Vector(player.getPos().x+65,player.getPos().y-70) + self.pos
		endPos = (polar(ang,self.r)+position)
		canvas.draw_line(position.get_p(),endPos.get_p(), 1, 'Black')

		source_centre = (self.hook.get_width() / 2, self.hook.get_height() / 2)
		source_size = (self.hook.get_width(), self.hook.get_height())
		dest_size = (50,50)

		canvas.draw_image(self.hook,
						source_centre,
						source_size,
						(endPos+Vector(15,-5).rotate(ang)).get_p(),
						dest_size,(ang-90)*math.pi/180)


#org = True
#hookRotate = 0
#kbd = Keyboard()

#addr = os.getcwd()
#rod = Rod("file:///"+addr+"/images/hook.png", "file:///"+addr+"/images/colouredBoth.png")



#inter = Interaction(rod, kbd)

#def draw(canvas):
	#inter.update()
	#rod.draw_handler(canvas)

#frame = simplegui.create_frame('Testing', 1980, 1080)
#frame.set_draw_handler(draw)
#frame.set_keydown_handler(kbd.keyDown)
#frame.set_keyup_handler(kbd.keyUp)
#frame.set_canvas_background("white")

#frame.start()
