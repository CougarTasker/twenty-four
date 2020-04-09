import random, math, os,time
from fish import Shark
from  vect import Vector
from keyboard import Keyboard 
from snd import Snd
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def polar(ang,r):#method for creating a vector from polar coordinates
	pX = r * math.cos(ang * (math.pi / 180))
	pY = r * math.sin(ang * (math.pi / 180))
	return Vector(round(pX),round(pY))

class Rod:
	def __init__(self,player,windowheight,time):
		#sync the class with the time
		self.time = time
		self.lastFrameTime = self.time.time()
		addr = os.getcwd()

		#image and sound resources
		self.hook = simplegui.load_image("file:///"+addr+"/images/hook.png")
		self.sound = Snd(self.time,"splash.ogg")

		#main attributes for calculating the rods positioning 
		self.hook_size = (50,50)#size of the when drawn
		self.player = player#the player that is holding the rod
		self.rnorm = 120#the normal lenth of the string. this is the smallest it will ever be
		self.r = self.rnorm# r = the lenth of the string. it begins at the normal length
		self.direction = 0#what direction is the hok moving in 0 no direction 1 is down and -1 is up
		self.rmax = windowheight-self.rodpos().y-self.hook_size[1]/2
		
		#the max length of the rope is the distance from the top of the rod to the bottom of the screen 
		#subract half the hight of the image
		
		self.hookspeed = 150

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

	def down(self):#send the hook down
		if self.direction==0 and self.player.vel.length() < 5:
		#you can only do this if the player is stationary and isnt already moving
			self.moved =False
			self.sound.play()
			self.direction = 1
	def up(self):
		if self.direction == 1:#if the hook is moving downwards it can move upwards
			self.direction = -1
	def moveable(self):#should the user move the boat. false if the user is cathing fish 
		return len(self.courtFish) ==0 and len(self.flyingFish) ==0 and self.direction == 0

#remove the fish that have landed in the bucket from the fish that the rod is keeping track of
	def catch(self,fish):
		if fish in self.flyingFish:
			self.flyingFish.remove(fish)

#this method is run to catch any fish the hook may touch and to move them with the hook
	def catch_fish(self,school):
		if self.moveable():
			self.moved = False#check wether the boat can be moved
		if self.direction != 0:
			#if the hook is moving through the water 
			if not self.moved:
				#catch the fish if allowed 
				self.courtFish = self.mergerlist(self.courtFish,school.touching_fish(self.hookpos()[0],10))
			#move the fish to the new hook position
			school.move_fish(self.hookpos()[0],self.courtFish,self.hookvel())
		else:
			#if the hook is stationary and has realed in fish
			for fish in self.courtFish:
				if type(fish) != Shark:
					#animate each fish to the bucket
					fish.animstart(self.player.getPos()-Vector(30,-25))
				else:
					fish.animstart(self.player.getPos()+Vector(8,-25))
				self.flyingFish.append(fish)#move the fish to the flying fish list to keep track of them
			self.courtFish = []#remove all fish from the hook. 
			#becuase you can leave the fish on the hook and put them in the bucket

	#the list isnt a set so to merge witout duplicate this method is used
	def mergerlist(self,a,b):
		for item in b:
			if not item in a:
				self.up()
				a.append(item)
		return a

	#calculates the position of the hook 
	def hookpos(self):
		frequency = 3#speed at witch the hook moves
		#calcuate the angle of the hook
		ang = math.sin(((self.lastFrameTime)%frequency)/frequency * math.pi*2)*30/((self.r-self.rnorm)/60+1)+90
		endPos = (polar(ang,self.r)+self.rodpos())#calculate the end position from the angle and length using the polar method

		return [endPos+Vector(15,-5).rotate(ang),endPos,(ang-90)*math.pi/180]
		#the hook has a center as well as an attachment point t
                #he first argument is the center the second is the attachment point
		#the third component is the angle as its needed elswhere and there is no point in calculating it twice
		#it is rotated and converted to radians as that is what simplegui uses 

	#calculates where the top of the rod is (where rod meets player sprite)
	def rodpos(self):
		return Vector(self.player.getPos().x+65,self.player.getPos().y-70)
                #calculates based on player position 

	#calculate hook velocity based on hook/rod position
	def hookvel(self):
		direction = self.hookpos()[0] - self.rodpos()
		return self.direction * direction.normalize()


	def update_length(self,delta):
	#change the length of the string each frame
		self.r += self.direction * delta * self.hookspeed
		if(self.r< self.rnorm):
			self.r = self.rnorm
			self.direction = 0
			self.moved = False
		if(self.r > self.rmax):
			self.r = self.rmax
			self.direction = -1
			
	def draw(self,canvas):
		#draw the string and hook to the screen

		delta = self.time.time()-self.lastFrameTime
		self.lastFrameTime = self.time.time()

		#make the strign the correct length
		self.update_length(delta)

		#calcute where the hook should be
		hookpos = self.hookpos()

		#draw the string from the rod to hook position
		canvas.draw_line(self.rodpos().get_p(),hookpos[1].get_p(), 1, 'Black')

		#the hook image propites
		source_centre = (self.hook.get_width() / 2, self.hook.get_height() / 2)
		source_size = (self.hook.get_width(), self.hook.get_height())

		#draw the hook 
		canvas.draw_image(self.hook,
						source_centre,
						source_size,
						hookpos[0].get_p(),
						self.hook_size,hookpos[2])



