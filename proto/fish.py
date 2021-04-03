import random,math,time,os,threading
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS
class School:
        #handles all the fish and shark objects 
	def __init__(self,count,dim,time,die):
		self.fish = [] # a list containing all the fish objects in this school of fish
		self.time = time# a time object to control when the fish are paused
		self.lastFrameTime = self.time.time()
		random.seed(time.time()) 
		addr = os.getcwd()
		
		#the left and right sprite sheet of the fish to be shared across them to improve performance and fix transparency issue
		self.imgr = SS("file:///"+addr+"/images/right.png",(2,2),time=400,scale=0.2,timehand = self.time)
		self.imgl = SS("file:///"+addr+"/images/left.png",(2,2),time=400,scale=0.2,timehand = self.time)

		#create half of the fish that will be beneanth the sharks -- thanks dave cohen for this idea
		for i in range(int(count/2)):
			self.fish.append(Fsh(Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr,time,die))
		self.shrl = SS("file:///"+addr+"/images/Sharkleft.png",(5,1),time=600,scale=1,timehand = self.time)# the shark sprite sheets 
		self.shrr = SS("file:///"+addr+"/images/Sharkright.png",(5,1),time=600,scale=1,timehand = self.time)

                #create sharks
		for i in range(1):
			self.fish.append(Shark(Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.shrl,self.shrr,time,die))

		#the rest of the fish
		for i in range(int(count/2)):
			self.fish.append(Fsh(Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr,time,die))
		t = threading.Thread(target=self.update,args=())
		t.start()
	def draw(self,canvas):#draw all the fish
		for fish in self.fish:
			fish.draw(canvas)#draw the fish
			
	def restart(self):#if the game needs to restart the fish this is quicker than recreating all the fish
		for fish in self.fish:
			fish.restart()
			
	def touching_fish(self,pos,r):#this method is used by the rod class but it returns all the fish that are touching a particular circle (ie hook)
		out = []
		for boid in self.fish:
			if (boid.pos- pos).length() < (boid.size+r):
				out.append(boid)
		return out
	
	def move_fish(self,pos,fish,vel = None):#this moves a group of fish to a position
		for boid in fish:
			boid.fixed = True#make sure the boid algorithm won't move the fish
			boid.pos = pos
			if not vel is None:
				boid.vel = vel
	def update(self):
		while self.time.check_running():#while the game is running
			delta = self.time.time()-self.lastFrameTime #calcuralte the amount of time that has passed
			self.lastFrameTime = self.time.time()
			for fish in self.fish:#draw all of the fish
				if self.time.isPlaying():#if the game isnt paused do the physics on the fish
					fish.update(delta,self.fish)
			time.sleep(max(1/30-(self.time.time()-self.lastFrameTime),0))
			#if running faster than 60hz sleep the correct amount of time

class Anim:#this is used to control the fish while it is animating 
	def __init__(self,fsh,time,bounds):
		self.bounds = bounds#the bounds of the water it might fall into 
		self.g = V(0,120)#the gravity the fish will fall under
		self.time = time
		self.timel = 2 + random.random()#the length of the animation
		self.startt = 0 #the time the animation starts
		self.fsh = fsh#the fish that will be animated
		self.startp = V()#the start position and velocity 
		self.startv = V()
		self.anim = False#is the fish currently being animated
		self.endscale = 0.5#the size of the fish at the end of the animation
		self.moved = False#has the boat been moved
		self.movedt = 0#the time when the boat has been moved
		
        #called when the rod is moved but the fish is in the animation
	def rodmoved(self):
		self.moved = True
		self.movedt = self.time.time()
		
	def scale(self):#calculate the scale the fish should be at
		if self.moved:# if the fish has been moved make the fish get bigger again to the full size
			t = self.movedt*2 - self.time.time()
			s = self.endscale + (self.startt+self.timel-t)/self.timel * (1-self.endscale)
			if s >1:
				s = 1
			return s
		# the scale is a linear transformation from the start to end size
		return self.endscale + (self.startt+self.timel- self.time.time())/self.timel * (1-self.endscale)
	
	def start(self,end):#start the animation the end is the end postion
		if not self.anim:#only start the animation if the previous animation has stopped
			self.moved= False#it can't have moved if the animation has just started
			self.startt = self.time.time()#what is the time
			self.startp = self.fsh.pos#what is the old position of the fish
			self.startv = ((end - self.startp)-1/2 * self.g * self.timel**2)/self.timel
			#calculate the velocity needed to get the fish to the end position
			self.anim = True
	def stop(self):
		self.anim = False
		#stop the animation
	
	def isAnim(self):#check if the fish is being animated
		if self.anim:#if it is supposed to be animating is that still the case?
			if (self.time.time() -self.startt > self.timel and not self.moved) or (self.bounds.contains(self.pos(),self.fsh.size) and self.moved):
				#if the animation is over or it has hit the water
				self.anim = False#if it shoulnt be animating then stop it
				if self.moved:#if the boat has moved 
					self.fsh.release()#release the fish back into the water
				else:
					self.fsh.court()#let the user catch the fish
		return self.anim#return if the fish is being animated
	
	def pos(self):#get the position of the fish
		t = self.time.time() - self.startt
		return self.startp + self.startv * t + 0.5 * self.g * t**2
	
	def vel(self):#get the velocity of the fish
		t = self.time.time() - self.startt
		return self.startv + self.g *t

class Fsh:#this is all of the details of the individual fish
	def __init__(self,bounds,imgl,imgr,time,die):
		self.die = die#keep a reference of what to call when the fish dies e.g. its been caught
		self.bounds = bounds#what are the boundaries of the water
		self.max_vel = 75#what is the max speed of the fish
		self.imgr = imgr#what images 
		self.imgl = imgl
		self.time = time#keep track of the time
		self.size = 25#what is the size of the fish
		self.scale = 1#what is the scale of the fish image
		self.per = self.size*3#how far can the fish see 
		self.fixed = False#is the position of the fish fixed
		self.pos = V(random.random()*bounds.dim.x+bounds.pos.x,random.random()*bounds.dim.y+bounds.pos.y)#set the position of the fish
		angle = random.random()*math.pi*2#angle the fish randomle 
		self.vel = V(math.cos(angle),math.sin(angle)) * 20#set the velocity in the angle of the direction of the fish
		self.anim =Anim(self,time,bounds)#add the animation handler
		
	def release(self):
		self.scale = 1#set the fish back to the correct scale
		self.fixed = False#let it move on its own accord
	def restart(self):
		if self.anim.anim:#if the fish is animating 
			self.anim.stop()#stop it 
		self.reset()#reset the fish
	def reset(self):
		self.bounds.random_start(self)#rest the position to something random
		self.scale = 1#set the fish back to the correct scale
		self.fixed = False#let it move on its own accord
	def court(self):
		self.die.catch(self)#let the game know this fish has been caught
		self.reset()#reset the fish as if it didn't die
	def animstart(self,end):
		self.anim.start(end)#start the animation handeler
	def draw(self,canvas):
		#calculate the angle of the fish from the direction of the velocity
		a = self.vel.angle(V(0,1))
		if self.vel.x > 0: 
			img = self.imgr#if moving right use the right image 
			a = math.pi/2 -a
		else:
			a -= math.pi/2
			img = self.imgl#if moving left use the left image 
		
		img.pos = self.pos#set the image position to the fish position
		old = img.scale#set the scale of the image
		img.scale = old * self.scale
		img.draw(canvas,rotation=a)#draw the image
		img.scale = old
		
		##used to debug the fish
		#canvas.draw_line(self.pos.get_p(),(self.pos+self.vel).get_p(),2,"blue")
		#canvas.draw_circle(self.pos.get_p(),self.size,1,"black")

	#align the velocity with the average of the fish it can see
	def allign(self,fish):
		if len(fish) < 1:
			return V()#if there is no fish you can't align to them
		# calculate the average velocities of the other boids
		avg = V()#store the average velocity
		count = 0#number of fish around
		for boid in fish:
			#count each fish if they are close enough and aren't the original fish
			if(boid.pos - self.pos).length()<self.per and not self is boid:
				count+=1
				avg += boid.vel
		if count>0:#check for divide by zero error
			avg /= count#take the mean
			#move our velocity towards the others
			return (avg).normalize()#normalize it so only the direction matters
		else:
			return V()

	# try to move to the center of mass of the fish around it
	def cohesion(self,fish):
		if len(fish) < 1:
			return V()#if there is no fish then you can't be attracted to them
		# calculate the average distances from the other boids
		com = V()
		count = 0
		for boid in fish:
			#count each fish if they are close enough and arent the original fish
			if (boid.pos - self.pos).length()<self.per and not self is boid:
				com += (boid.pos - self.pos)# add the vector to this new position
				count+=1
		if count>0 and com != V():#check for divide by zero error
			com /= count#take the mean
			# move our velocity towards the centre of mass
			return com.normalize()#normalize it so only the direction matter
		else:
			return V()

	# try to avoid coliding and moving towared any other fish		
	def seperation(self,fish, minDistance):#avoid touching other fish
		if len(fish) < 1:# if there are no fish can't move away from them
			return V()
		count = 0
		distsum = V()
		distance = 0
		for boid in fish:
			#count each fish if they are close enough and aren't the original fish
			distance =(self.pos-boid.pos).length()
			if distance < minDistance and not self is boid and distance != 0:
				count += 1

				distsum += (boid.pos-self.pos)/distance**2
				#add the distance with more ephasis on fish that are closer
		if count == 0:#check for divide by zero error
			return V()
		return  (-distsum/count).normalize()#move away from where the average is
	
	def sharkawarness(self,fish):#avoid the sharks it can see
		if len(fish) < 1:
			return V()
		distance = 0
		numClose = 0
		distsum = V()
		for boid in fish:
			distance = (self.pos-boid.pos).length()
			if distance < self.per*2 and distance != 0 and isinstance(boid,Shark):
				numClose += 1
				distsum += (boid.pos-self.pos)/distance**2

		if numClose == 0:
			return V()

		return  (-distsum/numClose).normalize()
	
	def update(self,delta,fish):#update the positon of the fish
		if not self.fixed:#if the fish is free to move
			self.vel += self.allign(fish) * 1
			self.vel += self.cohesion(fish) * 6
			self.vel += self.seperation(fish,self.per*3/5) * 7
			self.vel += self.sharkawarness(fish) * 4
			self.vel += self.bounds.repel(self) * 6
      
      #try not to hit the top or bottom of the water
			self.vel = self.vel.normalize() * self.max_vel#make sure fish is moving at the same velocity
			self.vel.rotate((random.random()*2-1)*delta*20)
			#add a random factor so the movement isn't completely predictable and boring
			
			self.pos += self.vel * delta#move the position by the velocity and the amount of time that has passed
			self.pos = self.bounds.correct(self)#fix the position so it doesn't leave the screen
			
		elif self.anim.isAnim():#if the fish is animating 
			self.vel = self.anim.vel()#set the position velocity and scale aproprately
			self.pos = self.anim.pos()
			self.scale = self.anim.scale()

class Shark(Fsh):
	def __init__(self,bounds,imgl,imgr,time,die):#shark is like a fish but has slightly different behviour
		super().__init__(bounds,imgl,imgr,time,die)
		self.size = 40#it is bigger and it moves faster and can see further
		self.max_vel = 150
		self.per = self.size*3
	def update(self,delta,fish):
		if not self.fixed:
			self.vel += self.allign(fish)* -self.max_vel/50#it is also attracted to the fish
			self.vel += self.cohesion(fish)* self.max_vel/20
			self.vel += self.seperation(fish,self.per*3/5) * self.max_vel/30
			self.vel += self.bounds.repel(self)*self.max_vel * 0.4
			self.vel = self.vel.normalize() * self.max_vel# it is not scared of other sharks  
			self.vel.rotate((random.random()*2-1)*delta*20)
			self.pos += self.vel * delta
			self.pos = self.bounds.correct(self)
		elif self.anim.isAnim():
			self.vel = self.anim.vel()
			self.pos = self.anim.pos()
			self.scale = self.anim.scale()
	def seperation(self,fish, minDistance):
		if len(fish) < 1:
			return V()
		distance = 0
		numClose = 0
		distsum = V()
		for boid in fish:
			distance = (self.pos-boid.pos).length()
			if distance < minDistance and distance != 0:
				numClose += 1
				distsum += (boid.pos-self.pos)/distance**2

		if numClose == 0:
			return V()

		return  (-distsum/numClose).normalize()
		

class Bounds:#this is for dealing with keeping everything in the water
	def __init__(self,pos,dim):
		self.pos = pos
		self.dim = dim
	def contains(self,pos,size):#does the bounds fully contain the fish? 
		x = pos.x-size >= self.pos.x and pos.x+size < self.dim.x + self.pos.x
		y = pos.y-size >= self.pos.y and pos.y+size < self.dim.y + self.pos.y
		return x and y
	def random_start(self,fish):
	#move a fish to a random position from off the screen this means it can swim on without anyone noticing 
		if random.random() > 0.5:
			fish.pos = self.pos + V(self.dim.x+fish.size,0)
			fish.pos.y = self.dim.y * random.random()
		else:
			fish.pos = self.pos - V(fish.size,0)
			fish.pos.y = self.dim.y * random.random()
	def correct(self,fish):
		#correct the fishes position if it goes out of the bounds of the water.
		return V(self.cord(self.pos.x,self.pos.x+self.dim.x,fish),self.cora(self.pos.y,self.pos.y+self.dim.y,fish))
	def cord(self,mn,mx,val):
		if val.pos.x+val.size<mn:
			return mx+val.size
		if val.pos.x-val.size>mx:
			return mn-val.size
		return val.pos.x
	def cora(self,mn,mx,val):
		if val.pos.y-val.size<mn:
			val.vel.y *= -1
			return mn+val.size
		if val.pos.y+val.size>mx:
			val.vel.y *= -1
			return mx-val.size
		return val.pos.y
	def repel(self,fish):#repel fish from the top and bottom so they don't hit the boundary as much
		a = self.pos.y + fish.size
		b = self.pos.y + self.dim.y - fish.size
		r = (b-a)/2
		p = -(fish.pos.y-r-a)/r
		safe = 0.8
		if abs(p) < safe:
			p = 0
		else:
			if p >0:
				p -=safe
			else:
				p +=safe
			
			p *= 1/(1-safe) 
		return V(0,p)
