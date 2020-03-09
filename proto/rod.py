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

class Rod:
	def __init__(self,player,windowheight,time):
			self.time = time
			addr = os.getcwd()
			self.hook = simplegui.load_image("file:///"+addr+"/images/hook.png")
			#self.radius = 50
			self.swing = True
			self.player = player
			self.pos = Vector()
			self.rnorm = 120
			self.r = self.rnorm
			self.direction = 0
			position = Vector(player.getPos().x+65,player.getPos().y-70) + self.pos
			self.rmax = windowheight-(position).y-50/2
			self.courtFish = []
			self.flyingFish = []
			self.lastFrameTime = self.time.time()
			self.moved = False
	def playermoved(self):
		if not self.moveable():
			self.moved = True
			for fish in self.flyingFish:
					fish.anim.rodmoved()
			self.flyingFish=[]
			for fish in self.courtFish:
				fish.release()
			self.courtFish = []
			if self.direction != 0:
				self.up()
		else:
			self.moved = False

	def down(self):
		if self.direction == 0:
			self.direction = 1
	def up(self):
		#print("up")
		self.direction = -1
	def moveable(self):
		return len(self.courtFish) ==0 and len(self.flyingFish) ==0 and self.direction == 0
	def catch(self,fish):
		if fish in self.flyingFish:
			self.flyingFish.remove(fish)
	def catch_fish(self,school):
		if self.moveable():
			self.moved = False
		if self.direction != 0:
			if not self.moved:
				self.courtFish = self.mergerlist(self.courtFish,school.touching_fish(self.hookpos()[0],10))
			school.move_fish(self.hookpos()[0],self.courtFish,self.hookvel())
		else:
			for fish in self.courtFish:
				fish.animstart(self.player.getPos()-Vector(30,-25))
				self.flyingFish.append(fish)
			self.courtFish = []
	def mergerlist(self,a,b):
		for item in b:
			if not item in a:
				self.up()
				a.append(item)
		return a
	def hookpos(self):
		frequency = 3

		ang = math.sin(((self.lastFrameTime)%frequency)/frequency * math.pi*2)*30/((self.r-self.rnorm)/60+1)+90
		endPos = (polar(ang,self.r)+self.rodpos())

		return [endPos+Vector(15,-5).rotate(ang),endPos,(ang-90)*math.pi/180]
	def rodpos(self):
		return Vector(self.player.getPos().x+65,self.player.getPos().y-70) + self.pos
	def hookvel(self):
		direction = self.hookpos()[0] - self.rodpos()
		return self.direction * direction.normalize()
	def update_length(self,delta):
		self.r += self.direction * delta * 80
		if(self.r< self.rnorm):
			self.r = self.rnorm
			self.direction = 0
		if(self.r > self.rmax):
			self.r = self.rmax
			self.direction = -1
	def draw(self,canvas):
		delta = self.time.time()-self.lastFrameTime
		self.lastFrameTime = self.time.time()
		self.update_length(delta)

		hookpos = self.hookpos()
		canvas.draw_line(self.rodpos().get_p(),hookpos[1].get_p(), 1, 'Black')

		source_centre = (self.hook.get_width() / 2, self.hook.get_height() / 2)
		source_size = (self.hook.get_width(), self.hook.get_height())
		dest_size = (50,50)

		canvas.draw_image(self.hook,
						source_centre,
						source_size,
						hookpos[0].get_p(),
						dest_size,hookpos[2])


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
