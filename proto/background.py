import random,math,time,os
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
		self.bubbles = SS("file:///"+addr+"/images/Bubble1.png",(6,5),time=1250,scale=0.22,timehand = self.time)
		self.carol = SS("file:///"+addr+"/images/carol.png",(5,1),time=800,scale=0.22,timehand = self.time)
		self.perl = SS("file:///"+addr+"/images/pearl.png",(3,3),time=3000,scale=0.22,looping=False,timehand = self.time)
		#self.floor = simplegui.load_image()
	def background(self,canvas,pollycount,wavecount,frequency,height,waveheight,color):
		path = [(0,self.dimensions[1])]
		offset = self.lastFrameTime%(1/frequency)*frequency
		for x in range(pollycount+1):
			ang = x/pollycount*wavecount + offset
			ang *= 2*math.pi
			path.append((x/pollycount*self.dimensions[0],((math.sin(ang)*waveheight/2+height)*self.dimensions[1])))
		path.append((self.dimensions[0],0))
		path.append((0,0))
		canvas.draw_polygon(path,1,color,color)
	def draw_wave_parts(self,canvas,poly,color):
		for path in poly:
			if len(path) > 2:
				canvas.draw_polygon(path,1,color,color)
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
		drawing = False # keeps track if we are addign more points to the loop
		forward = []
		backward = []
		for x in range(len(a)):
			if a[x][1] <= b[x][1]: #for each point if a does extend futher than b 
				if not drawing:# if this is the fist point 
					drawing = True #reset the loop varibles
					forward = []
					backward = []
					if x>0: # if there is a previus point then there must be a intersection 
						forward.append(self.intersection(a[x-1],a[x],b[x-1],b[x]))
						#add the intersection
				forward.append(a[x])#add the points for moving forward and backwards along this loop
				backward.append(b[x])
			elif drawing:# if this doesnt extend futether but we were drawing points then we are done
				forward.append(self.intersection(a[x-1],a[x],b[x-1],b[x]))
				#add the closing intersection between the forwad and backwards part of the loop
				drawing = False#we arent drawing more of the loop now
				backward.reverse()# reverse the backward part so it is in the right direction
				paths.append(forward+backward)#add the forwars and backwads par to create a full loop and add this to the output
		if drawing: #if still drawign anfter the end of the loop close off the end section 
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
	def draw_sun(self,canvas,height):
		canvas.draw_image(self.sun,(250,250),(500,500),(self.dimensions[0]-self.dimensions[1]*height/2,self.dimensions[1]*height/2),(self.dimensions[1]*height,self.dimensions[1]*height))
	def looping_clouds(self,canvas,frequency,height):
		offset = self.lastFrameTime%(1/frequency)*frequency
		dim = (2400,300)
		cen = (1200,150)
		width = math.floor(dim[0]/dim[1]*height*self.dimensions[1])
		canvas.draw_image(self.clouds, cen, dim,(width/2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
		canvas.draw_image(self.clouds, cen, dim,(width/2+width*2-offset*width,height*self.dimensions[1]/2),(width,height*self.dimensions[1]))
	def draw_carol(self,canvas,x=0.5):
		self.carol.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.carol.adim[1]*self.carol.scale/2))
		self.bubbles.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.bubbles.adim[1]*self.bubbles.scale/2))
	def draw_perl(self,canvas,x = 0.5):
		self.perl.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.perl.adim[1]*self.perl.scale/2))
	def draw_water_world(self,canvas,top = 0.25):
    		canvas.draw_image(self.water_world,(997/2,647/2),(997,647),(self.dimensions[0]/2,(top+(1-top)/2)*self.dimensions[1]),(self.dimensions[0],self.dimensions[1]*(1-top)))
	def draw(self, canvas):
		#delta = self.time.time()-self.lastFrameTime
		self.lastFrameTime = self.time.time()
		#if delta !=0:
			#print("fps: "+ str(1/delta))
		self.draw_water_world(canvas)#draw the large background image
		self.draw_carol(canvas,0.2)#draw the animating fetures at the bottom of the screen
		self.draw_carol(canvas,0.7)
		self.draw_perl(canvas,0.5)
		pollycount = 35
		self.background(canvas,pollycount,2,0.2,0.3,0.05,"rgb(0,0,250)")#draw the bacground wave

		big = self.poly(pollycount,2,0.2,0.3,0.05) #rgb(0,0,250)
		middle = self.poly(pollycount,3,-0.6,0.3,0.04) # rgb(0,0,150)
		small = self.poly(pollycount,4,1,0.3,0.03) #rgb(0,0,100)


		middles = self.sub(middle,big) #subtract the bigger wave from the middle size one
		smalls = self.sub(small,self.max(middle,big)) # subtract the combined top wave from the smallest one
		self.draw_wave_parts(canvas,middles,"rgb(0,0,150)")#draw these wave sections
		self.draw_wave_parts(canvas,smalls,"rgb(0,0,100)")
		
		self.looping_clouds(canvas,0.05,0.2)#draw the parlax clouds and the sun element in the sky 
		self.draw_sun(canvas,0.3)
		self.looping_clouds(canvas,0.03,0.25)
		
