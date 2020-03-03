import random,math,time,os
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS
class School:
	def __init__(self,count,dim):
		self.fish = []
		self.lastFrameTime = time.time()
		random.seed(time.time()) 
		addr = os.getcwd()
		self.playing = True
		self.imgr = SS("file:///"+addr+"/images/right.png",(2,2),time=400,scale=0.2)
		self.imgl = SS("file:///"+addr+"/images/left.png",(2,2),time=400,scale=0.2)
		for i in range(int(count/2)):
			self.fish.append(Fsh(V(random.random()*dim[0],random.random()*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr))
		self.fish.append(Shark(V(random.random()*dim[0],random.random()*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675))))
		for i in range(int(count/2)):
			self.fish.append(Fsh(V(random.random()*dim[0],random.random()*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr))
	def draw(self,canvas,playerx = 0):
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		for fish in self.fish:
			if self.playing:
				fish.update(delta,self.fish)
			fish.draw(canvas,playerx,fish=self.fish)

	def touching_fish(self,pos,r):
		out = []
		for boid in self.fish:
			if (boid.pos- pos).length() < (boid.size+r):
				out.append(boid)
		return out
	def play(self):
		self.playing = True 
	def pause(self):
		self.playing = False
	def alt(self):
		self.playing = not self.playing
	def move_fish(self,pos,fish,vel = None):
		for boid in fish:
			boid.fixed = True
			boid.pos = pos
			if not vel is None:
				boid.vel = vel
class Fsh:
	def __init__(self,pos,bounds,imgl,imgr):
		self.bounds = bounds
		self.max_vel = 75
		self.imgr = imgr
		self.imgl = imgl
		self.size = 25
		self.per = self.size*3
		self.fixed = False
		self.pos = pos
		angle = random.random()*math.pi*2
		self.vel = V(math.cos(angle),math.sin(angle)) * 20

	def reset(self):
		self.bounds.random_start(self)
		self.fixed = False
	def draw(self,canvas,playerx =0,fish=[]):
		#canvas.draw_circle(self.pos.get_p(),4,1,"red","red")
		
		a = self.vel.angle(V(0,1))
		if self.vel.x > 0: 
			a *= -1 
			img = self.imgr
			a += math.pi/2
		else:
			a -= math.pi/2
			img = self.imgl
		
		img.pos = self.pos+V(-playerx,0)
		img.draw(canvas,rotation=a)
		canvas.draw_line(self.pos.get_p(),(self.pos+self.vel).get_p(),2,"blue")
		#canvas.draw_circle(self.pos.get_p(),self.size,1,"black")
	def allign(self,fish):
		if len(fish) < 1:
			return
		# calculate the average velocities of the other boids
		avg = V()
		count = 0
		for boid in fish:
			if(boid.pos - self.pos).length()<self.per:
				count+=1
				avg += boid.vel
		
		if count>0:
			avg /= count		
			# set our velocity towards the others
			return (avg).normalize()
		else:
			return V()
	def cohesion(self,fish):
		if len(fish) < 1:
			return

		# calculate the average distances from the other boids
		com = V()
		count = 0
		for boid in fish:
			if boid.pos == self.pos:
				continue
			elif (boid.pos - self.pos).length()<self.per:
				com += (self.pos - boid.pos)
				count+=1
		if count>0:
			com /= count
			return -com.normalize()
		else:
			return V()
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
	def sharkawarness(self,fish):
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
	def update(self,delta,fish):
		if not self.fixed:
			self.vel += self.allign(fish)* self.max_vel/50
			self.vel += self.cohesion(fish)* self.max_vel/50
			self.vel += self.seperation(fish,self.per*3/5) * self.max_vel/30
			self.vel += self.sharkawarness(fish) * self.max_vel*1.5
			self.vel += self.bounds.repel(self)*self.max_vel * 0.4
			self.vel = self.vel.normalize() * self.max_vel
			self.vel.rotate((random.random()*2-1)*delta*20)
			self.pos += self.vel * delta
			self.pos = self.bounds.correct(self)

class Shark(Fsh):
	def __init__(self,pos,bounds):
		addr = os.getcwd()
		super().__init__(pos,bounds,SS("file:///"+addr+"/images/Sharkleft.png",(5,1),time=600,scale=1),SS("file:///"+addr+"/images/Sharkright.png",(5,1),time=600,scale=1))
		self.size = 40
		self.max_vel = 150
		self.per = self.size*3
	def update(self,delta,fish):
		if not self.fixed:
			self.vel += self.allign(fish)* -self.max_vel/50
			self.vel += self.cohesion(fish)* self.max_vel/20
			self.vel += self.seperation(fish,self.per*3/5) * self.max_vel/30
			self.vel += self.bounds.repel(self)*self.max_vel * 0.4
			self.vel = self.vel.normalize() * self.max_vel  
			self.vel.rotate((random.random()*2-1)*delta*20)
			self.pos += self.vel * delta
			self.pos = self.bounds.correct(self)
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
		

class Bounds:
	def __init__(self,pos,dim):
		self.pos = pos
		self.dim = dim
	def random_start(self,fish):
		if random.random() > 0.5:
			fish.pos = self.pos + V(self.dim.x+fish.size,0)
			fish.pos.y = self.dim.y * random.random()
		else:
			fish.pos = self.pos - V(fish.size,0)
			fish.pos.y = self.dim.y * random.random()
	def correct(self,fish):
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
	def repel(self,fish):
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

