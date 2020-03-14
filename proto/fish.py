import random,math,time,os
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS
class School:
	def __init__(self,count,dim,time,die):
		self.fish = []
		self.time = time
		self.lastFrameTime = self.time.time()
		random.seed(time.time()) 
		addr = os.getcwd()
		self.imgr = SS("file:///"+addr+"/images/right.png",(2,2),time=400,scale=0.2,timehand = self.time)
		self.imgl = SS("file:///"+addr+"/images/left.png",(2,2),time=400,scale=0.2,timehand = self.time)
		for i in range(int(count/2)):
			self.fish.append(Fsh(V(random.random()*dim[0],(random.random()*0.675+0.325)*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr,time,die))
		self.shrl = SS("file:///"+addr+"/images/Sharkleft.png",(5,1),time=600,scale=1,timehand = self.time)
		self.shrr = SS("file:///"+addr+"/images/Sharkright.png",(5,1),time=600,scale=1,timehand = self.time)
		self.fish.append(Shark(V(random.random()*dim[0],(random.random()*0.675+0.325)*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.shrl,self.shrr,time,die))
		self.fish.append(Shark(V(random.random()*dim[0],(random.random()*0.675+0.325)*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.shrl,self.shrr,time,die))
		self.fish.append(Shark(V(random.random()*dim[0],(random.random()*0.675+0.325)*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.shrl,self.shrr,time,die))
		for i in range(int(count/2)):
			self.fish.append(Fsh(V(random.random()*dim[0],(random.random()*0.675+0.325)*dim[1]),Bounds(V(0,0.325*dim[1]),V(dim[0],dim[1]*0.675)),self.imgl,self.imgr,time,die))
	def draw(self,canvas,playerx = 0):
		delta = self.time.time()-self.lastFrameTime
		self.lastFrameTime = self.time.time()
		for fish in self.fish:
			if self.time.isPlaying():
				fish.update(delta,self.fish)
			fish.draw(canvas,playerx,fish=self.fish)
	def restart(self):
		for fish in self.fish:
			fish.restart()
	def touching_fish(self,pos,r):
		out = []
		for boid in self.fish:
			if (boid.pos- pos).length() < (boid.size+r):
				out.append(boid)
		return out
	def move_fish(self,pos,fish,vel = None):
		for boid in fish:
			boid.fixed = True
			boid.pos = pos
			if not vel is None:
				boid.vel = vel
class Anim:
	def __init__(self,fsh,time,bounds):
		self.bounds = bounds
		self.g = V(0,120)
		self.time = time
		self.timel = 2 + random.random()
		self.startt = 0  
		self.fsh = fsh
		self.startp = V()
		self.startv = V()
		self.anim = False
		self.endscale = 0.5
		self.movedscale = 0.1
		self.moved = False
		self.movedt = 0
	def rodmoved(self):
		self.moved = True
		self.movedt = self.time.time()
	def scale(self):
		if self.moved:
			t = self.movedt*2 - self.time.time()
			s = self.endscale + (self.startt+self.timel-t)/self.timel * (1-self.endscale)
			if s >1:
				s = 1
			return s
		return self.endscale + (self.startt+self.timel- self.time.time())/self.timel * (1-self.endscale)
	def start(self,end):
		if not self.anim:		
			self.moved= False
			self.startt = self.time.time()
			self.startp = self.fsh.pos
			self.startv = ((end - self.startp)-1/2 * self.g * self.timel**2)/self.timel
			self.anim = True
	def stop(self):
		self.anim = False
	def isAnim(self):
		if self.anim:
			if (self.time.time() -self.startt > self.timel and not self.moved) or (self.bounds.contains(self.pos(),self.fsh.size) and self.moved):
				self.anim = False
				if self.moved:
					self.fsh.release()
				else:
					self.fsh.court()
		return self.anim
	def pos(self):
		t = self.time.time() - self.startt
		return self.startp + self.startv * t + 0.5 * self.g * t**2
	def vel(self):
		t = self.time.time() - self.startt
		return self.startv + self.g *t

class Fsh:
	def __init__(self,pos,bounds,imgl,imgr,time,die):
		self.die = die
		self.bounds = bounds
		self.max_vel = 75
		self.imgr = imgr
		self.imgl = imgl
		self.time = time
		self.size = 25
		self.scale = 1
		self.per = self.size*3
		self.fixed = False
		self.g = V(0,100)
		self.pos = pos
		angle = random.random()*math.pi*2
		self.vel = V(math.cos(angle),math.sin(angle)) * 20
		self.anim =Anim(self,time,bounds)
		
	def release(self):
		self.scale = 1
		self.fixed = False
	def restart(self):
		if self.anim.anim:
			self.anim.stop()
			self.reset()
	def reset(self):
		self.bounds.random_start(self)
		self.scale = 1
		self.fixed = False
	def court(self):
		self.die.catch(self)
		self.reset()
	def animstart(self,end):
		self.anim.start(end)
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
		old = img.scale
		img.scale = old * self.scale
		img.draw(canvas,rotation=a)
		img.scale = old
		#

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
		elif self.anim.isAnim():
			self.vel = self.anim.vel()
			self.pos = self.anim.pos()
			self.scale = self.anim.scale()

class Shark(Fsh):
	def __init__(self,pos,bounds,imgl,imgr,time,die):
		super().__init__(pos,bounds,imgl,imgr,time,die)
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
		

class Bounds:
	def __init__(self,pos,dim):
		self.pos = pos
		self.dim = dim
	def contains(self,pos,size):
		x = pos.x-size >= self.pos.x and pos.x+size < self.dim.x + self.pos.x
		y = pos.y-size >= self.pos.y and pos.y+size < self.dim.y + self.pos.y
		return x and y
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

