from vect import Vector
class Score:
	def __init__(self,time,dim,die,frame):
		self.score = 0
		self.time = time
		self.maxtime = 99
		self.starttime = self.time.time()
		self.scoreh = 30
		self.timeh = 25
		self.padding = 5
		self.size = Vector(frame.get_canvas_textwidth("Score: "+'{:04d}'.format(self.score), self.scoreh)+self.padding*2,self.padding*2+self.scoreh+self.timeh)
		self.pos = Vector(((Vector(dim[0],dim[1]) - self.size)/2).x,0)
		self.die = die
		
	def timeleft(self):
		t = self.maxtime - (self.time.time() - self.starttime)
		if t <= 0:
			t = 0
			self.die.gameOver()
		return round(t)
	def resetScore(self):
		self.score = 0
	def incScore(self,score):
		self.score+= score
	def draw(self,canvas):
		canvas.draw_polygon((self.pos.get_p(),(self.pos+self.size.x*Vector(1,0)).get_p(),(self.pos+self.size).get_p(),(self.pos+self.size.y*Vector(0,1)).get_p()),1,"rgba(255,255,255,0)","rgba(100,100,100,0.5)")
		canvas.draw_text("Score: "+'{:04d}'.format(self.score), (self.pos+Vector(self.padding,self.scoreh+self.padding)).get_p(), self.scoreh, "orange")
		canvas.draw_text("time: "+'{:02d}'.format(self.timeleft()), (self.pos+Vector(self.padding,self.scoreh+self.padding+self.timeh)).get_p(), 25, "red")
