import random,math,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS
class School:
	def __init__(self,count,dim):
		self.fish = []
		random.seed(time.time()) 
		self.imgr = SS("file:///"+addr+"/images/right.png",(2,2),time=400,scale=0.2)
		self.imgl = SS("file:///"+addr+"/images/left.png",(2,2),time=400,scale=0.2)
		for i in range(count):
			self.fish.append(Fsh(V(random.random()*dim[0],random.random()*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgr,self.imgl))
	def draw(self,canvas,delta):
		for fish in self.fish:
			fish.update(delta,self.fish)
			fish.draw(canvas)
class Fsh:
	def __init__(self,pos,bounds,imgr,imgl):
		self.bounds = bounds
		self.max_vel = 75
		self.imgr = imgr 
		self.imgl = imgl
		self.size = 25
		self.per = self.size*3
		self.pos = pos
		angle = random.random()*math.pi*2
		self.vel = V(math.cos(angle),math.sin(angle)) * 20
	def draw(self,canvas):
		#canvas.draw_circle(self.pos.get_p(),4,1,"red","red")
		
		a = self.vel.angle(V(0,1))
		if self.vel.x > 0: 
			a *= -1 
			img = self.imgr
			a += math.pi/2
		else:
			a -= math.pi/2
			img = self.imgl
		
		img.pos = self.pos
		img.draw(canvas,rotation=a)
		#canvas.draw_line(self.pos.get_p(),(self.pos+self.vel).get_p(),2,"blue")
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
			if  distance < minDistance and distance != 0:
				numClose += 1
				distsum += (boid.pos-self.pos)/distance**2

		if numClose == 0:
			return V()

		return  (-distsum/numClose).normalize()
	def update(self,delta,fish):
		self.vel += self.allign(fish)* self.max_vel/50
		self.vel += self.cohesion(fish)* self.max_vel/50
		self.vel += self.seperation(fish,self.per*3/5) * self.max_vel/30
		self.vel = self.vel.normalize() * self.max_vel
		self.vel.rotate((random.random()*2-1)*delta*20)
		self.pos += self.vel * delta
		self.pos = self.bounds.correct(self)

class Bounds:
	def __init__(self,pos,dim):
		self.pos = pos
		self.dim = dim
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

