import random, math, os,time
from fish import Shark
from  vect import Vector
from keyboard import Keyboard 
from snd import Snd
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
			self.lastFrameTime = self.time.time()
			addr = os.getcwd()

			#image and sound resources
			self.hook = simplegui.load_image("file:///"+addr+"/images/hook.png")
                        self.sound = Snd(self.time,"splash.ogg")

                        #main attributes for calculating the rods positioning 
			self.swing = True
			self.player = player
			self.pos = Vector()
			self.rnorm = 120
			self.r = self.rnorm
			self.direction = 0
			position = Vector(player.getPos().x+65,player.getPos().y-70) + self.pos
			self.rmax = windowheight-(position).y-50/2

			self.courtFish = []#stores the fish attached to the hook
			self.flyingFish = []#stores the fish in the air (between sea and bucket)
			self.moved = False#used to check if the player has moved before fish have reached the bucket
			
	#check if player has moved while attempting to catch fish
	def playermoved(self):
		if not self.moveable():
			self.moved = True
			for fish in self.flyingFish:
				if type(fish) != Shark:
					fish.anim.rodmoved()
					self.flyingFish.remove(fish)
			for fish in self.courtFish:
				if type(fish) != Shark:
					fish.release()
					self.courtFish.remove(fish)
			if self.direction != 0:
				self.up()
		else:
			self.moved = False

	def down(self):
		if self.direction==0 and self.player.vel.length() < 5:
			self.sound.play()
			self.direction = 1
	def up(self):
		
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
				if type(fish) != Shark:
					fish.animstart(self.player.getPos()-Vector(30,-25))
				else:
					fish.animstart(self.player.getPos()+Vector(8,-25))
				self.flyingFish.append(fish)
			self.courtFish = []
	def mergerlist(self,a,b):
		for item in b:
			if not item in a:
				self.up()
				a.append(item)
		return a

	#calculates the position of the hook 
	def hookpos(self):
		frequency = 3

		ang = math.sin(((self.lastFrameTime)%frequency)/frequency * math.pi*2)*30/((self.r-self.rnorm)/60+1)+90
		endPos = (polar(ang,self.r)+self.rodpos())

		return [endPos+Vector(15,-5).rotate(ang),endPos,(ang-90)*math.pi/180]

	#calculates where the top of the rod is (where rod meets player sprite)
	def rodpos(self):
		return Vector(self.player.getPos().x+65,self.player.getPos().y-70) + self.pos

        #calculate hook velocity based on hook/rod position
	def hookvel(self):
		direction = self.hookpos()[0] - self.rodpos()
		return self.direction * direction.normalize()


	def update_length(self,delta):
		self.r += self.direction * delta * 150
		if(self.r< self.rnorm):
			self.r = self.rnorm
			self.direction = 0
			self.moved = False
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



