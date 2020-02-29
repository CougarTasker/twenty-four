import random,math,time
<<<<<<< HEAD
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vect import Vector as V
from spritesheet import SpriteSheet as SS

class Background:
	def __init__(self,dimensions):
		self.lastFrameTime = time.time()
		self.dimensions = dimensions
		self.clouds = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/background_clouds.png")
		self.sun = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/sun.png")
		self.water_world = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/underwater-seamless-landscape-cartoon-background-vector-7524975.png")
		self.bubbles = SS("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/Bubble1.png",(6,5),time=1250,scale=0.22)
		self.carol = SS("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/carol.png",(5,1),time=800,scale=0.22)
		self.perl = SS("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/pearl.png",(3,3),time=3000,scale=0.22,looping=False)
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
	def sub(self,pollycount,a,b,c):
		paths = []
		drawing = False
		forward = []
		backward = []
		for x in range(pollycount+1):
			if a[x][1] <= b[x][1] and a[x][1] <= c[x][1]:
				if not drawing:
					drawing = True
					forward = []
					if x>0:
						bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
						cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
						if bint[1] < cint[1]:
							forward.append(bint)
						else:
							forward.append(cint)
						
					backward = []
				forward.append(a[x])
				if b[x][1]<c[x][1]:
					backward.append(b[x])
				else:
					backward.append(c[x])
			else:
				if drawing:
					bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
					cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
					if bint[1] < cint[1]:
						forward.append(bint)
					else:
						forward.append(cint)

					drawing = False
					backward.reverse()
					paths.append(forward+backward)

		if drawing: 
			drawing = False
			backward.reverse()
			paths.append(forward+backward)
		return paths

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
		delta = time.time()-self.lastFrameTime
		self.lastFrameTime = time.time()
		print("fps: "+ str(1/delta))
		
		self.background(canvas,20,4,1,0.3,0.03,"rgb(0,0,100)")
		self.background(canvas,20,3,-0.6,0.3,0.04,"rgb(0,0,150)")
		self.draw_water_world(canvas)
		self.draw_carol(canvas,0.2)
		self.draw_carol(canvas,0.7)
		self.draw_perl(canvas,0.5)
		self.background(canvas,20,2,0.2,0.3,0.05,"rgb(0,0,250)")
		big = self.poly(40,2,0.2,0.3,0.05) #rgb(0,0,250)
		middle = self.poly(40,3,-0.6,0.3,0.04) # rgb(0,0,150)
		small = self.poly(40,4,1,0.3,0.03) #rgb(0,0,100)
		middles = self.sub(40,middle,big,big)
		smalls = self.sub(40,small,middle,big)
		self.draw_wave_parts(canvas,middles,"rgb(0,0,150)")
		self.draw_wave_parts(canvas,smalls,"rgb(0,0,100)")
		
		self.looping_clouds(canvas,0.05,0.2)
		self.draw_sun(canvas,0.3)
		self.looping_clouds(canvas,0.03,0.25)
=======
from vect import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Background:
    def __init__(self,dimensions):
        self.lastFrameTime = time.time()
        self.dimensions = dimensions
        self.carol1bubble = bubblesheet(Vector(200,680))
        self.carol2bubble = bubblesheet(Vector(690,680))
        self.pearl = Pearl(Vector(500,700))
        self.clouds = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/background_clouds.png")
        self.sun = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/sun.png")
        self.water_world = simplegui.load_image("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/underwater-seamless-landscape-cartoon-background-vector-7524975.png")
        self.carol = SpriteSheet("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/carol.png",(5,1),time=800,scale=0.2,pos=Vector(100,200))

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
    def sub(self,pollycount,a,b,c):
        paths = []
        drawing = False
        forward = []
        backward = []
        for x in range(pollycount+1):
            if a[x][1] <= b[x][1] and a[x][1] <= c[x][1]:
                if not drawing:
                    drawing = True
                    forward = []
                    if x>0:
                        bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
                        cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
                        if bint[1] < cint[1]:
                            forward.append(bint)
                        else:
                            forward.append(cint)
                        
                    backward = []
                forward.append(a[x])
                if b[x][1]<c[x][1]:
                    backward.append(b[x])
                else:
                    backward.append(c[x])
            else:
                if drawing:
                    bint = self.intersection(a[x-1],a[x],b[x-1],b[x])
                    cint = self.intersection(a[x-1],a[x],c[x-1],c[x])
                    if bint[1] < cint[1]:
                        forward.append(bint)
                    else:
                        forward.append(cint)

                    drawing = False
                    backward.reverse()
                    paths.append(forward+backward)

        if drawing: 
            drawing = False
            backward.reverse()
            paths.append(forward+backward)
        return paths

    def intersection(self,a,b,c,d):
        a = Vector(a[0],a[1])
        b = Vector(b[0],b[1])
        c = Vector(c[0],c[1])
        d = Vector(d[0],d[1])
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
    def draw_carol(self,canvas,x):
        self.carol.draw(canvas,center=(x*self.dimensions[0],self.dimensions[1]-self.carol.adim[1]*self.carol.scale/2))
    def draw_water_world(self,canvas,top = 0.25):
        canvas.draw_image(self.water_world,(997/2,647/2),(997,647),(self.dimensions[0]/2,(top+(1-top)/2)*self.dimensions[1]),(self.dimensions[0],self.dimensions[1]*(1-top)))

    def draw(self, canvas):
        delta = time.time()-self.lastFrameTime
        self.lastFrameTime = time.time()
        print("fps: "+ str(1/delta))
        
        self.background(canvas,20,4,1,0.3,0.03,"rgb(0,0,100)")
        self.background(canvas,20,3,-0.6,0.3,0.04,"rgb(0,0,150)")
        self.draw_water_world(canvas)
        self.pearl.draw_canvas(canvas)
        self.carol1bubble.draw_canvas(canvas)
        self.carol2bubble.draw_canvas(canvas)
        self.draw_carol(canvas,0.2)
        self.draw_carol(canvas,0.7)
        self.background(canvas,20,2,0.2,0.3,0.05,"rgb(0,0,250)")
        big = self.poly(40,2,0.2,0.3,0.05) #rgb(0,0,250)
        middle = self.poly(40,3,-0.6,0.3,0.04) # rgb(0,0,150)
        small = self.poly(40,4,1,0.3,0.03) #rgb(0,0,100)
        middles = self.sub(40,middle,big,big)
        smalls = self.sub(40,small,middle,big)
        self.draw_wave_parts(canvas,middles,"rgb(0,0,150)")
        self.draw_wave_parts(canvas,smalls,"rgb(0,0,100)")
        
        self.looping_clouds(canvas,0.05,0.2)
        self.draw_sun(canvas,0.3)
        self.looping_clouds(canvas,0.03,0.25)
        

class bubblesheet(object):
    
    def __init__(self,pos):
        self.img_url = "https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/Bubble1.png"
        self.row = 5
        self.column = 6
        self.img = simplegui.load_image(self.img_url)
        self.bdim = Vector(self.img.get_width(),self.img.get_height())
        self.adim = (self.bdim.x/self.column, self.bdim.y/self.row)
        self.center = Vector(self.adim[0]/2, self.adim[1]/2)
        self.pos = pos
        self.ratio = 0.15
        self.frame_index = [1,1]
        self.count = 0
    def draw_canvas(self,canvas):
        self.count += 1
        if self.count % 1 == 0:
            self.frame_index = self.next_frame()
        canvas.draw_image(self.img,(self.center.get_p()[0]*(2*self.frame_index[1]-1),self.center.get_p()[1]*(2*self.frame_index[0]-1)),self.adim,self.pos.get_p(),(self.adim[0]*self.ratio,self.adim[1]*self.ratio))
    def next_frame(self):
        self.frame_index[1] += 1
        if self.frame_index[1] > self.column:
            self.frame_index[0] += 1
            self.frame_index[1] = 1
        if self.frame_index[0] > self.row:
            self.frame_index = [1,1]
        return self.frame_index
    
class Pearl(object):
    def __init__(self,pos):
        self.img_url = "https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/pearl.png"
        self.row = 3
        self.column = 3
        self.img = simplegui.load_image(self.img_url)
        self.bdim = Vector(self.img.get_width(),self.img.get_height())
        self.adim = (self.bdim.x/self.column, self.bdim.y/self.row)
        self.center = Vector(self.adim[0]/2, self.adim[1]/2)
        self.pos = pos
        self.ratio = 0.2
        self.frame_index = [1,1]
        self.count = 0
        self.order = True
    def draw_canvas(self,canvas):
        self.count += 1
        if self.count % 10 == 0:
            self.frame_index = self.next_frame()
        canvas.draw_image(self.img,(self.center.get_p()[0]*(2*self.frame_index[1]-1),self.center.get_p()[1]*(2*self.frame_index[0]-1)),self.adim,self.pos.get_p(),(self.adim[0]*self.ratio,self.adim[1]*self.ratio))
    def next_frame(self):
        if self.order:
            self.frame_index[1] += 1
            if self.frame_index[1] > self.column:
                self.frame_index[0] += 1
                self.frame_index[1] = 1
        else:
            self.frame_index[1] -= 1
            if self.frame_index[1] == 0:
                self.frame_index[0]-=1
                self.frame_index[1] = self.column
        if self.frame_index == [3,3]:
            self.order = False
        elif self.frame_index == [1,1]:
            self.order = True
        return self.frame_index
    
class SpriteSheet(object):
    """docstring for SpriteSheet"""
    def __init__(self, url,size=(1,1),pos = Vector(),framecount = -1,time = 1000,scale = 1):
        if framecount == -1:
             framecount = size[0]*size[1]
        self.framecount = framecount
        self.url = url
        self.size = size
        self.img = simplegui.load_image(url)
        self.bdim = Vector(self.img.get_width(),self.img.get_height()) # before dimentions
        self.adim = (self.bdim.x/self.size[0],self.bdim.y/self.size[1]) # after dimaentions
        self.cent = Vector(self.adim[0]/2,self.adim[1]/2)
        self.fno = 0
        self.time = time
        self.pos = pos
        self.scale =scale
    def done(self):
        return self.fno == self.framecount-1
    def draw(self,canvas,center=(-1,-1),size=(-1,-1),rotation=0):
        self.fno = round((time.time()%(self.time/1000))/(self.time/1000)*(self.framecount-1))
        x = self.fno  % self.size[0]
        y = (self.fno - x)/self.size[0]
        if center[0] < 0:
            center = self.pos.get_p()
        if size[0] <0:
            size =(self.adim[0]*self.scale,self.adim[1]*self.scale)
        loc = Vector(x*self.adim[0],y*self.adim[1])
        canvas.draw_image(self.img,(self.cent+loc).get_p(),self.adim,center,size,rotation)


class School:
    def __init__(self,count,dim):
        self.fish = []
        random.seed(time.time()) 
        self.imgr = SpriteSheet("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/right.png",(2,2),time=400,scale=0.2)
        self.imgl = SpriteSheet("https://raw.githubusercontent.com/CougarTasker/twenty-four/master/proto/images/left.png",(2,2),time=400,scale=0.2)
        for i in range(count):
            self.fish.append(Fsh(Vector(random.random()*dim[0],random.random()*dim[1]),Bounds(Vector(0,0.325*dim[1]),Vector(dim[0],dim[1]*0.675)),self.imgr,self.imgl))
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
        self.vel = Vector(math.cos(angle),math.sin(angle)) * 20
    def draw(self,canvas):
        #canvas.draw_circle(self.pos.get_p(),4,1,"red","red")
        
        a = self.vel.angle(Vector(0,1))
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
        avg = Vector()
        count = 0
        for boid in fish:
            if(boid.pos - self.pos).length()<self.per:
                count+=1
                avg += boid.vel
        
        if count>0:
            avg = avg.divide(count)		
            # set our velocity towards the others
            return (avg).normalize()
        else:
            return Vector()
    def cohesion(self,fish):
        if len(fish) < 1:
            return

        # calculate the average distances from the other boids
        com = Vector()
        count = 0
        for boid in fish:
            if boid.pos == self.pos:
                continue
            elif (boid.pos - self.pos).length()<self.per:
                com += (self.pos - boid.pos)
                count+=1
        if count>0:
            com = com.divide(count)
            return -com.normalize()
        else:
            return Vector()
    def seperation(self,fish, minDistance):
        if len(fish) < 1:
            return Vector()

        distance = 0
        numClose = 0
        distsum = Vector()
        for boid in fish:
            distance = (self.pos-boid.pos).length()
            if  distance < minDistance and distance != 0:
                numClose += 1
                distsum += (boid.pos-self.pos).divide(distance**2)

        if numClose == 0:
            return Vector()

        return  (-distsum.divide(numClose)).normalize()
    def update(self,delta,fish):
        self.vel = self.vel.add(self.allign(fish).multiply(self.max_vel/50))
        self.vel = self.vel.add(self.cohesion(fish).multiply(self.max_vel/50))
        self.vel = self.vel.add(self.seperation(fish,self.per*3/5).multiply(self.max_vel/30))
        self.vel = self.vel.normalize().multiply(self.max_vel)
        self.vel.rotate((random.random()*2-1)*delta*20)
        self.pos = self.pos.add(self.vel * delta)
        self.pos = self.bounds.correct(self)

class Bounds:
    def __init__(self,pos,dim):
        self.pos = pos
        self.dim = dim
    def correct(self,fish):
        return Vector(self.cord(self.pos.x,self.pos.x+self.dim.x,fish),self.cora(self.pos.y,self.pos.y+self.dim.y,fish))
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

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 750

class Interaction:
    def __init__(self,dimensions):#,pearl, carol):
        self.lastFrameTime = time.time()
        self.dimensions = dimensions
        self.back = Background(dimensions)
        self.fish = School(30,(CANVAS_WIDTH, CANVAS_HEIGHT))

    def update(self):
        pass
    def draw(self, canvas):
        delta = time.time()-self.lastFrameTime
        self.lastFrameTime = time.time()
        self.back.draw(canvas)
        self.fish.draw(canvas,delta)



i = Interaction((CANVAS_WIDTH, CANVAS_HEIGHT))


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Game", CANVAS_WIDTH, CANVAS_HEIGHT,0)

frame.set_canvas_background("rgb(87,221,255)")
frame.set_draw_handler(i.draw)
# Start the frame animation
frame.start()
>>>>>>> 53936c6c7302082362127f3baa998e7f03ae0dcf
