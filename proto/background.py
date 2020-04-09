import random,math,time,os,threading
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS

class Background:
	def __init__(self,dimensions,time):
		addr = os.getcwd()
		self.time = time
		self.lastFrameTime = self.time.time()
		self.dimensions = dimensions
		self.clouds = simplegui.load_image("file:///"+addr+"/images/background_clouds.png")
		self.sun = simplegui.load_image("file:///"+addr+"/images/sun.png")
		self.water_world = simplegui.load_image("file:///"+addr+"/images/underwater-seamless-landscape-cartoon-background-vector-7524975.png")

				#establish background elements as spritesheet objects with their spritesheet image
		self.bubbles = SS("file:///"+addr+"/images/Bubble1.png",(6,5),time=1250,scale=0.22,timehand = self.time)
		self.carol = SS("file:///"+addr+"/images/carol.png",(5,1),time=800,scale=0.22,timehand = self.time)
		self.perl = SS("file:///"+addr+"/images/pearl.png",(3,3),time=3000,scale=0.22,looping=False,timehand = self.time)
		self.bWaveParts = []
		self.mWaveParts = []
		self.sWaveParts = []
		self.pollycount = 35
		t = threading.Thread(target=self.update,args=())
		t.start()

	#draw a wave's polygons to the screen
	def draw_wave_parts(self,canvas,poly,color):
		for path in poly:
			if len(path) > 2:
				canvas.draw_polygon(path,1,color,color)
				
	#make paths for background waves
	def poly(self,pollycount,wavecount,frequency,height,waveheight):
		path = []
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*self.dimensions[0],((math.sin(ang)*waveheight/2+height)*self.dimensions[1])))
		return path
	def sub(self,a,b):#returns the loops of the polygon a that extend further than b
		paths = []
		drawing = False # keeps track if we are adding more points to the loop
		forward = []
		backward = []
		for x in range(len(a)):
			if a[x][1] <= b[x][1]: #for each point if a does extend further than b 
				if not drawing:# if this is the first point 
					drawing = True #reset the loop varibles
					forward = []
					backward = []
					if x>0: # if there is a previous point then there must be a intersection 
						forward.append(self.intersection(a[x-1],a[x],b[x-1],b[x]))
						#add the intersection
				forward.append(a[x])#add the points for moving forward and backwards along this loop
				backward.append(b[x])
			elif drawing:# if this doesn't extend further but we were drawing points then we are done
				forward.append(self.intersection(a[x-1],a[x],b[x-1],b[x]))
				#add the closing intersection between the forward and backwards part of the loop
				drawing = False#we arent drawing more of the loop now
				backward.reverse()# reverse the backward part so it is in the right direction
				paths.append(forward+backward)#add the forwards and backwards part to create a full loop and add this to the output
		if drawing: #if still drawing after the end of the loop close off the end section 
			drawing = False
			backward.reverse()
			paths.append(forward+backward)
		return paths#return the output
	
	def max(self,a,b):#this returns the max of a and b polygons 
		out = []
		for x in range(len(a)):
			if a[x][1] <= b[x][1]:
				out.append(a[x])
			else:
				out.append(b[x])
		return out

	#used by sub method to determine where an intersection occurs when determining wave polygon points
	def intersection(self,a,b,c,d):
		a = V(a[0],a[1])
		b = V(b[0],b[1])
		c = V(c[0],c[1])
		d = V(d[0],d[1])
		cd = d-c
		ab = b-a
		u = (a.cross(ab)-c.cross(ab))/cd.cross(ab)
		l = (c.cross(cd)-a.cross(cd))/ab.cross(cd)
		if u>=0 and u<= 1 and l >= 0 and l <= 1:
			return (u * cd + c).get_p()	        
		else:
			return (0,1000)

	#draw static sun image to screen
	def draw_sun(self,canvas,height):
		canvas.draw_image(self.sun,(250,250),(500,500),(self.dimensions[0]-self.dimensions[1]*height/2,self.dimensions[1]*height/2),(self.dimensions[1]*height,self.dimensions[1]*height))

		#draws clouds animation to sky 
	def looping_clouds(self,canvas,frequency,height):
		offset = self.lastFrameTime%(1/frequency)*frequency
		dim = (2400,300)
		cen = (1200,150)
		width = math.floor(dim[0]/dim[1]*height*self.dimensions[1])
		canvas.draw_image(self.clouds, cen, dim,(width/2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width*2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))

		#drawing background elements through the spritesheet object draw handler
	def draw_carol(self,canvas,x=0.5):
		self.carol.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.carol.adim[1]*self.carol.scale/2))
		self.bubbles.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.bubbles.adim[1]*self.bubbles.scale/2))
	def draw_perl(self,canvas,x = 0.5):
		self.perl.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.perl.adim[1]*self.perl.scale/2))
	def draw_water_world(self,canvas,top = 0.25):
			canvas.draw_image(self.water_world,(997/2,647/2),(997,647),(self.dimensions[0]/2,(top+(1-top)/2)*self.dimensions[1]),(self.dimensions[0],self.dimensions[1]*(1-top)))

		#draw method to call above 3 methods as well as generate the background waves and call methods to draw clouds/sun
	def update(self):
		while self.time.check_running(): #while the game is running
			#establish 3 different wave paths
			self.lastFrameTime = self.time.time()
			big = self.poly(self.pollycount,2,0.2,0.3,0.05) #rgb(0,0,250)
			middle = self.poly(self.pollycount,3,-0.6,0.3,0.04) # rgb(0,0,150)
			small = self.poly(self.pollycount,4,1,0.3,0.03) #rgb(0,0,100)
			
			self.mWaveParts = self.sub(middle,big) #subtract the bigger wave from the middle size one
			self.sWaveParts = self.sub(small,self.max(middle,big)) # subtract the combined top wave from the smallest one


			big.append((self.dimensions[0],0))
			big.append((0,0))#add the points so that the background is coverd and complet the loop

			self.bWaveParts = [big]
			time.sleep(max(1/30-(self.time.time()-self.lastFrameTime),0))
			#if running faster than 30hz sleep the correct amount of time
	def draw(self, canvas):
		self.draw_water_world(canvas)#draw the large background image
		self.draw_carol(canvas,0.2)#draw the animating features at the bottom of the screen
		self.draw_carol(canvas,0.7)
		self.draw_perl(canvas,0.5)

		#drawing the background waves
		
		self.draw_wave_parts(canvas,self.bWaveParts,"rgb(0,0,250)")#draws the front wave as a full polygon  			big
		self.draw_wave_parts(canvas,self.mWaveParts,"rgb(0,0,150)")#draw these wave sections on behind main polygon  	medium 
		self.draw_wave_parts(canvas,self.sWaveParts,"rgb(0,0,100)")#draw the smaller waves sections   					small

		#draw the clouds and the sun element in the sky 
		self.looping_clouds(canvas,0.05,0.2)
		self.draw_sun(canvas,0.3)
		self.looping_clouds(canvas,0.03,0.25)
		
